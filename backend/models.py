"""
SQLAlchemy ORM Data Models
Toxic Comment Moderation System

Tables:
- users: User profiles with role-based access ('user' vs 'admin')
- comments: Post comments with multi-label toxicity scores and moderation status
- moderation_logs: Audit trail of automated actions and admin interventions
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="user", nullable=False)  # 'user' | 'admin'
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    moderated_actions = relationship("ModerationLog", back_populates="admin")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    text = Column(Text, nullable=False)

    # Multi-label probability scores [0.0, 1.0]
    toxic = Column(Float, default=0.0, nullable=False)
    severe_toxic = Column(Float, default=0.0, nullable=False)
    obscene = Column(Float, default=0.0, nullable=False)
    threat = Column(Float, default=0.0, nullable=False)
    insult = Column(Float, default=0.0, nullable=False)
    identity_hate = Column(Float, default=0.0, nullable=False)

    max_score = Column(Float, default=0.0, nullable=False)
    # Status: 'approved' (visible in feed) | 'flagged' (under review) | 'blocked' (rejected)
    status = Column(String(20), default="approved", index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True, nullable=False)

    author = relationship("User", back_populates="comments")
    logs = relationship("ModerationLog", back_populates="comment", cascade="all, delete-orphan")


class ModerationLog(Base):
    __tablename__ = "moderation_logs"

    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=False)
    action = Column(String(50), nullable=False)  # 'auto_approve' | 'auto_flag' | 'auto_block' | 'admin_approve' | 'admin_delete' | 'admin_override'
    admin_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    notes = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    comment = relationship("Comment", back_populates="logs")
    admin = relationship("User", back_populates="moderated_actions")
