"""
Pydantic Schemas for Input Validation & Serialization
Toxic Comment Moderation System
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ============================================================================
# Auth Schemas
# ============================================================================
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=5, max_length=100)
    password: str = Field(..., min_length=6)
    role: Optional[str] = "user"


class UserLogin(BaseModel):
    username_or_email: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ============================================================================
# Prediction & Moderation Schemas
# ============================================================================
class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


class ToxicityScores(BaseModel):
    toxic: float
    severe_toxic: float
    obscene: float
    threat: float
    insult: float
    identity_hate: float


class PredictResponse(BaseModel):
    text: str
    cleaned_text: str
    scores: ToxicityScores
    max_score: float
    is_toxic: bool
    status: str  # 'approved' | 'flagged' | 'blocked'
    verdict: str  # 'Clean (Approved)' | 'Potentially Toxic (Flagged)' | 'Toxic (Blocked)'
    flagged_categories: List[str]


# ============================================================================
# Comment Schemas
# ============================================================================
class CommentCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


class CommentOut(BaseModel):
    id: int
    text: str
    author: UserOut
    toxic: float
    severe_toxic: float
    obscene: float
    threat: float
    insult: float
    identity_hate: float
    max_score: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class CommentActionUpdate(BaseModel):
    action: str = Field(..., description="'approve' | 'delete' | 'block'")
    notes: Optional[str] = None


# ============================================================================
# Admin Analytics Schemas
# ============================================================================
class CategoryCount(BaseModel):
    category: str
    count: int


class DailyTrend(BaseModel):
    date: str
    total: int
    clean: int
    flagged: int
    blocked: int


class FlaggedUserStat(BaseModel):
    username: str
    violations_count: int


class TopToxicWord(BaseModel):
    text: str
    value: int


class AdminAnalyticsResponse(BaseModel):
    total_comments: int
    approved_comments: int
    flagged_comments: int
    blocked_comments: int
    toxic_rate_percentage: float
    category_distribution: List[CategoryCount]
    daily_trends: List[DailyTrend]
    top_flagged_users: List[FlaggedUserStat]
    top_toxic_words: List[TopToxicWord]
    confidence_histogram: List[Dict[str, Any]]
