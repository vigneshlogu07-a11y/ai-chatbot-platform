"""
Pydantic schemas for request / response validation.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ── Auth ──────────────────────────────────────────────
class SignupRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── Chat ──────────────────────────────────────────────
class ChatCreate(BaseModel):
    title: Optional[str] = "New Chat"


class ChatResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ChatListResponse(BaseModel):
    chats: List[ChatResponse]


# ── Message ───────────────────────────────────────────
class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=10000)


class MessageResponse(BaseModel):
    id: int
    chat_id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class MessageListResponse(BaseModel):
    messages: List[MessageResponse]


# ── Document ─────────────────────────────────────────
class DocumentResponse(BaseModel):
    id: int
    filename: str
    original_name: str
    file_type: str
    file_size: int
    chat_id: Optional[int] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    documents: List[DocumentResponse]


# ── Feedback ─────────────────────────────────────────
class FeedbackRating(str, Enum):
    like = "like"
    dislike = "dislike"


class FeedbackCreate(BaseModel):
    message_id: int
    rating: FeedbackRating
    comment: Optional[str] = None


class FeedbackResponse(BaseModel):
    id: int
    message_id: int
    user_id: int
    rating: str
    comment: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
