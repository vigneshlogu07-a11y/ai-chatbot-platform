"""
Feedback endpoints: like / dislike bot responses with optional comments.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Feedback, Message, User
from ..schemas import FeedbackCreate, FeedbackResponse
from ..auth import get_current_user

router = APIRouter(prefix="/api/feedback", tags=["Feedback"])


@router.post("/", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
def create_feedback(
    body: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verify message exists
    message = db.query(Message).filter(Message.id == body.message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    # Check for existing feedback (upsert)
    existing = (
        db.query(Feedback)
        .filter(Feedback.message_id == body.message_id, Feedback.user_id == current_user.id)
        .first()
    )
    if existing:
        existing.rating = body.rating.value
        existing.comment = body.comment
        db.commit()
        db.refresh(existing)
        return existing

    fb = Feedback(
        message_id=body.message_id,
        user_id=current_user.id,
        rating=body.rating.value,
        comment=body.comment,
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return fb


@router.get("/{message_id}", response_model=FeedbackResponse)
def get_feedback(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    fb = (
        db.query(Feedback)
        .filter(Feedback.message_id == message_id, Feedback.user_id == current_user.id)
        .first()
    )
    if not fb:
        raise HTTPException(status_code=404, detail="No feedback found")
    return fb
