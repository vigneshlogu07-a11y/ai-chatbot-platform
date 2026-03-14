"""
Message endpoints + SSE streaming for AI responses.
"""

import asyncio
import json
import random

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Chat, Message, User
from ..schemas import MessageCreate, MessageResponse, MessageListResponse
from ..auth import get_current_user
from ..config import settings

router = APIRouter(prefix="/api/chats", tags=["Messages"])

# ── NEW: google-genai client setup ───────────────────
from google import genai
from google.genai import types

gemini_client = None
if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here":
    gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)


# ── Simulated AI response generator (fallback) ──────
KNOWLEDGE_RESPONSES = [
    "That's a great question! Let me break it down for you. ",
    "I'd be happy to help with that. Here's what I know: ",
    "Interesting topic! Let me share my thoughts on this. ",
    "Based on my understanding, here's a comprehensive answer: ",
    "Let me analyze this step by step. ",
]

FOLLOW_UP_PARTS = [
    "The key concept here is that software systems are built in layers, each with its own responsibility. ",
    "When designing architectures, it's important to consider scalability, maintainability, and security. ",
    "Modern web applications typically use a client-server model with RESTful APIs for communication. ",
    "Database design is crucial — proper normalization and indexing can significantly impact performance. ",
    "Authentication and authorization are fundamental security concerns in any web application. ",
    "Testing is essential at every level: unit tests, integration tests, and end-to-end tests. ",
    "Error handling should be comprehensive — always plan for edge cases and provide meaningful messages. ",
    "Documentation is often overlooked but is vital for team collaboration and future maintenance. ",
    "Performance optimization should be data-driven — profile before optimizing to avoid premature changes. ",
    "Clean code principles like SOLID, DRY, and KISS help maintain long-term code quality. ",
]


def generate_ai_response(user_message: str) -> str:
    """Build a simulated AI response based on the user message."""
    opener = random.choice(KNOWLEDGE_RESPONSES)
    num_parts = random.randint(2, 4)
    body = "".join(random.sample(FOLLOW_UP_PARTS, num_parts))
    closer = f"\n\nIs there anything else you'd like to know about \"{user_message[:60]}\"?"
    return opener + body + closer


async def stream_tokens(text: str):
    """Yield the text token-by-token as SSE events."""
    words = text.split(" ")
    for i, word in enumerate(words):
        token = word + (" " if i < len(words) - 1 else "")
        yield f"data: {json.dumps({'token': token})}\n\n"
        await asyncio.sleep(random.uniform(0.02, 0.08))
    yield "data: [DONE]\n\n"


# ── Endpoints ─────────────────────────────────────────
@router.post(
    "/{chat_id}/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def send_message(
    chat_id: int,
    body: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    user_msg = Message(chat_id=chat_id, role="user", content=body.content)
    db.add(user_msg)

    ai_text = generate_ai_response(body.content)
    assistant_msg = Message(chat_id=chat_id, role="assistant", content=ai_text)
    db.add(assistant_msg)

    msg_count = db.query(Message).filter(Message.chat_id == chat_id).count()
    if msg_count == 0:
        chat.title = body.content[:80] if len(body.content) > 0 else "New Chat"

    db.commit()
    db.refresh(assistant_msg)
    return assistant_msg


@router.get("/{chat_id}/messages", response_model=MessageListResponse)
def get_messages(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    messages = (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.created_at.asc())
        .all()
    )
    return MessageListResponse(messages=messages)


@router.get("/{chat_id}/stream")
async def stream_response(
    chat_id: int,
    message: str = Query(..., min_length=1),
    token: str = Query(...),
    db: Session = Depends(get_db),
):
    from ..auth import decode_access_token

    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    # ── Build Gemini-compatible history ───────────────
    history_records = (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.created_at.asc())
        .limit(20)
        .all()
    )

    contents = []
    for doc in history_records:
        role = "user" if doc.role == "user" else "model"
        if doc.content:
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part(text=doc.content)],
                )
            )
    # Append the new user message
    contents.append(
        types.Content(role="user", parts=[types.Part(text=message)])
    )

    # Save user message
    user_msg = Message(chat_id=chat_id, role="user", content=message)
    db.add(user_msg)

    # Update chat title on first message
    msg_count = db.query(Message).filter(Message.chat_id == chat_id).count()
    if msg_count == 1:
        chat.title = message[:80] if len(message) > 0 else "New Chat"

    # Create empty assistant message placeholder
    assistant_msg = Message(chat_id=chat_id, role="assistant", content="")
    db.add(assistant_msg)
    db.commit()
    db.refresh(assistant_msg)

    async def event_generator():
        # Send message ID so frontend can reference it
        yield f"data: {json.dumps({'msg_id': assistant_msg.id})}\n\n"

        ai_text = ""

        # ── Fallback: no API key → simulated response ─
        if gemini_client is None:
            ai_text = generate_ai_response(message)
            async for chunk in stream_tokens(ai_text):
                yield chunk
            # ── google-genai streaming ────────────
            try:
                # ✅ FIX: await first, then iterate
                stream = await gemini_client.aio.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=contents,
                )
                async for chunk in stream:
                    if chunk.text:
                        ai_text += chunk.text
                        yield f"data: {json.dumps({'token': chunk.text})}\n\n"

            except Exception as e:
                error_msg = f" [Error generating response: {str(e)}]"
                ai_text += error_msg
                yield f"data: {json.dumps({'token': error_msg})}\n\n"

        yield "data: [DONE]\n\n"

        # Save the full generated text
        assistant_msg.content = ai_text
        db.commit()

    return StreamingResponse(event_generator(), media_type="text/event-stream")
