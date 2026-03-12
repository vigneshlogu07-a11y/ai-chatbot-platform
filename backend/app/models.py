"""
SQLAlchemy ORM models for LexRam.AI
"""

from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, TIMESTAMP, func,
)
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    username      = Column(String(50), unique=True, nullable=False)
    email         = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at    = Column(TIMESTAMP, server_default=func.now())

    chats     = relationship("Chat", back_populates="user", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")


class Chat(Base):
    __tablename__ = "chats"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    user_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title      = Column(String(200), default="New Chat")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user      = relationship("User", back_populates="chats")
    messages  = relationship("Message", back_populates="chat", cascade="all, delete-orphan", order_by="Message.created_at")
    documents = relationship("Document", back_populates="chat")


class Message(Base):
    __tablename__ = "messages"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    chat_id    = Column(Integer, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False, index=True)
    role       = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content    = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    chat      = relationship("Chat", back_populates="messages")
    feedbacks = relationship("Feedback", back_populates="message", cascade="all, delete-orphan")


class Document(Base):
    __tablename__ = "documents"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    user_id       = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    chat_id       = Column(Integer, ForeignKey("chats.id", ondelete="SET NULL"), nullable=True)
    filename      = Column(String(255), nullable=False)
    original_name = Column(String(255), nullable=False)
    file_type     = Column(String(50), nullable=False)
    file_size     = Column(Integer, nullable=False)
    uploaded_at   = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="documents")
    chat = relationship("Chat", back_populates="documents")


class Feedback(Base):
    __tablename__ = "feedback"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey("messages.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    rating     = Column(String(20), nullable=False)  # 'like' or 'dislike'
    comment    = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    message = relationship("Message", back_populates="feedbacks")
    user    = relationship("User", back_populates="feedbacks")
