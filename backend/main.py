"""
FastAPI Application Entry Point
Toxic Comment Moderation System

Provides RESTful API endpoints for:
- JWT Authentication & Role Authorization (user & admin)
- Real-time Deep Learning Toxicity Prediction (Live Check)
- Mock Social Feed with Automatic Comment Moderation
- Administrative Moderation Queue (Approve / Delete / Override)
- Analytics Dashboard (Trends, Distributions, User Statistics, Word Frequencies)
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from collections import Counter

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from backend.database import engine, get_db, Base
from backend.models import User, Comment, ModerationLog
from backend.schemas import (
    UserRegister,
    UserLogin,
    UserOut,
    Token,
    PredictRequest,
    PredictResponse,
    CommentCreate,
    CommentOut,
    CommentActionUpdate,
    AdminAnalyticsResponse,
    CategoryCount,
    DailyTrend,
    FlaggedUserStat,
    TopToxicWord,
)
from backend.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    get_current_admin,
)
from backend.moderation import moderation_engine, LABELS
from backend.seed import seed_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes database tables, loads ML model, and runs seed data if empty."""
    print("[Server Startup] Ensuring database tables exist...")
    Base.metadata.create_all(bind=engine)

    print("[Server Startup] Loading Deep Learning model artifacts...")
    moderation_engine.load_artifacts()

    # Automatically seed database if empty
    print("[Server Startup] Checking database records...")
    seed_database(force=False)
    print("[Server Startup] Ready to accept requests.")
    yield
    print("[Server Shutdown] Cleaning up resources...")


app = FastAPI(
    title="Toxic Comment Moderation System API",
    description="Multi-label deep learning toxicity analysis and automated social media content moderation.",
    version="1.0.0",
    lifespan=lifespan,
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# 1. AUTHENTICATION ENDPOINTS
# ============================================================================
@app.post("/api/auth/register", response_model=Token, status_code=status.HTTP_201_CREATED, tags=["Auth"])
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    """Registers a new user account with hashed credentials."""
    existing_user = db.query(User).filter(
        (User.username == user_in.username) | (User.email == user_in.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered.",
        )

    # Allow setting admin only if specified and role is 'admin', else default 'user'
    role = "admin" if user_in.role == "admin" else "user"

    new_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": str(new_user.id), "role": new_user.role})
    return {"access_token": token, "token_type": "bearer", "user": new_user}


@app.post("/api/auth/login", response_model=Token, tags=["Auth"])
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """Authenticates credentials and returns a Bearer JWT token."""
    user = db.query(User).filter(
        (User.username == login_data.username_or_email)
        | (User.email == login_data.username_or_email)
    ).first()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials. Please verify your username/password.",
        )

    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer", "user": user}


@app.get("/api/auth/me", response_model=UserOut, tags=["Auth"])
def get_current_profile(current_user: User = Depends(get_current_user)):
    """Returns profile information for the authenticated user."""
    return current_user


# ============================================================================
# 2. REAL-TIME PREDICTION (LIVE CHECK)
# ============================================================================
@app.post("/api/predict", response_model=PredictResponse, tags=["Inference"])
def predict_toxicity(req: PredictRequest):
    """
    Analyzes raw text input against the production Deep Learning model.
    Returns 6 label probabilities and automated moderation verdict.
    """
    result = moderation_engine.predict(req.text)
    return result


# ============================================================================
# 3. COMMENTS & SOCIAL FEED
# ============================================================================
@app.post("/api/comments", response_model=CommentOut, status_code=status.HTTP_201_CREATED, tags=["Comments"])
def create_comment(
    comment_in: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Creates a new comment, passes it through the deep learning moderation engine,
    and automatically assigns status ('approved', 'flagged', or 'blocked').
    """
    pred = moderation_engine.predict(comment_in.text)
    scores = pred["scores"]

    new_comment = Comment(
        user_id=current_user.id,
        text=comment_in.text,
        toxic=scores["toxic"],
        severe_toxic=scores["severe_toxic"],
        obscene=scores["obscene"],
        threat=scores["threat"],
        insult=scores["insult"],
        identity_hate=scores["identity_hate"],
        max_score=pred["max_score"],
        status=pred["status"],
        created_at=datetime.utcnow(),
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    # Log the automated moderation verdict
    action_type = (
        "auto_approve"
        if pred["status"] == "approved"
        else "auto_flag"
        if pred["status"] == "flagged"
        else "auto_block"
    )
    log = ModerationLog(
        comment_id=new_comment.id,
        action=action_type,
        admin_id=None,
        notes=f"Automated verdict: {pred['verdict']}. Highest Category Score: {pred['max_score']}",
        timestamp=datetime.utcnow(),
    )
    db.add(log)
    db.commit()

    return new_comment


@app.get("/api/comments", response_model=List[CommentOut], tags=["Comments"])
def get_comments_feed(
    status_filter: Optional[str] = Query("approved", description="'approved' | 'all' | 'flagged' | 'blocked'"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """Returns social feed comments with pagination and status filtering."""
    query = db.query(Comment)
    if status_filter != "all":
        query = query.filter(Comment.status == status_filter)

    comments = query.order_by(desc(Comment.created_at)).offset(offset).limit(limit).all()
    return comments


# ============================================================================
# 4. ADMIN MODERATION QUEUE & CONTROLS
# ============================================================================
@app.get("/api/admin/flagged", response_model=List[CommentOut], tags=["Admin"])
def get_flagged_queue(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Returns queue of comments flagged by AI awaiting manual admin review."""
    flagged = (
        db.query(Comment)
        .filter(Comment.status == "flagged")
        .order_by(desc(Comment.created_at))
        .all()
    )
    return flagged


@app.put("/api/admin/comments/{comment_id}", response_model=CommentOut, tags=["Admin"])
def moderate_comment(
    comment_id: int,
    action_in: CommentActionUpdate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin endpoint to approve, block, or delete an AI-flagged comment."""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found.")

    valid_actions = {"approve", "delete", "block"}
    if action_in.action not in valid_actions:
        raise HTTPException(status_code=400, detail=f"Action must be one of: {valid_actions}")

    if action_in.action == "approve":
        comment.status = "approved"
        log_action = "admin_approve"
    elif action_in.action == "block":
        comment.status = "blocked"
        log_action = "admin_block"
    else:  # delete
        comment.status = "blocked"
        log_action = "admin_delete"

    log = ModerationLog(
        comment_id=comment.id,
        action=log_action,
        admin_id=current_admin.id,
        notes=action_in.notes or f"Manual moderator intervention: {action_in.action}",
        timestamp=datetime.utcnow(),
    )
    db.add(log)
    db.commit()
    db.refresh(comment)
    return comment


# ============================================================================
# 5. ADMIN ANALYTICS DASHBOARD
# ============================================================================
@app.get("/api/admin/analytics", response_model=AdminAnalyticsResponse, tags=["Admin"])
def get_admin_analytics(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Aggregates platform moderation metrics, trendlines, and violation statistics."""
    total = db.query(Comment).count()
    approved = db.query(Comment).filter(Comment.status == "approved").count()
    flagged = db.query(Comment).filter(Comment.status == "flagged").count()
    blocked = db.query(Comment).filter(Comment.status == "blocked").count()

    toxic_rate = round(((flagged + blocked) / max(total, 1)) * 100, 2)

    # Category distribution (comments with score >= 0.35 per category)
    cat_dist = []
    for lbl in LABELS:
        count = db.query(Comment).filter(getattr(Comment, lbl) >= 0.35).count()
        cat_dist.append(CategoryCount(category=lbl.replace("_", " ").title(), count=count))

    # Daily trends for the last 14 days
    fourteen_days_ago = datetime.utcnow() - timedelta(days=14)
    recent_comments = (
        db.query(Comment)
        .filter(Comment.created_at >= fourteen_days_ago)
        .order_by(Comment.created_at)
        .all()
    )

    trend_map: Dict[str, Dict[str, int]] = {}
    for c in recent_comments:
        day_str = c.created_at.strftime("%Y-%m-%d")
        if day_str not in trend_map:
            trend_map[day_str] = {"total": 0, "clean": 0, "flagged": 0, "blocked": 0}
        trend_map[day_str]["total"] += 1
        if c.status == "approved":
            trend_map[day_str]["clean"] += 1
        elif c.status == "flagged":
            trend_map[day_str]["flagged"] += 1
        else:
            trend_map[day_str]["blocked"] += 1

    daily_trends = [
        DailyTrend(
            date=d,
            total=v["total"],
            clean=v["clean"],
            flagged=v["flagged"],
            blocked=v["blocked"],
        )
        for d, v in sorted(trend_map.items())
    ]

    # Top Flagged Users
    flagged_users_query = (
        db.query(User.username, func.count(Comment.id).label("violations"))
        .join(Comment, Comment.user_id == User.id)
        .filter(Comment.status.in_(["flagged", "blocked"]))
        .group_by(User.id)
        .order_by(desc("violations"))
        .limit(5)
        .all()
    )
    top_flagged_users = [
        FlaggedUserStat(username=u, violations_count=cnt) for u, cnt in flagged_users_query
    ]

    # Top Toxic Words extraction
    toxic_comments = (
        db.query(Comment.text)
        .filter(Comment.status.in_(["flagged", "blocked"]))
        .limit(200)
        .all()
    )
    word_counter: Counter = Counter()
    stopwords = {"the", "and", "a", "to", "is", "in", "it", "of", "you", "that", "this", "my", "your", "are", "i", "for", "on"}
    for (t,) in toxic_comments:
        words = [
            w.lower().strip(".,!?\"'")
            for w in t.split()
            if len(w) > 2 and w.lower() not in stopwords
        ]
        word_counter.update(words)

    top_toxic_words = [
        TopToxicWord(text=w, value=c) for w, c in word_counter.most_common(12)
    ]

    # Model Confidence Histogram
    histogram_bins = [
        {"bin": "0.0 - 0.2", "count": db.query(Comment).filter(Comment.max_score < 0.2).count()},
        {"bin": "0.2 - 0.4", "count": db.query(Comment).filter(Comment.max_score >= 0.2, Comment.max_score < 0.4).count()},
        {"bin": "0.4 - 0.6", "count": db.query(Comment).filter(Comment.max_score >= 0.4, Comment.max_score < 0.6).count()},
        {"bin": "0.6 - 0.8", "count": db.query(Comment).filter(Comment.max_score >= 0.6, Comment.max_score < 0.8).count()},
        {"bin": "0.8 - 1.0", "count": db.query(Comment).filter(Comment.max_score >= 0.8).count()},
    ]

    return AdminAnalyticsResponse(
        total_comments=total,
        approved_comments=approved,
        flagged_comments=flagged,
        blocked_comments=blocked,
        toxic_rate_percentage=toxic_rate,
        category_distribution=cat_dist,
        daily_trends=daily_trends,
        top_flagged_users=top_flagged_users,
        top_toxic_words=top_toxic_words,
        confidence_histogram=histogram_bins,
    )


# ============================================================================
# 6. MODEL COMPARISON ARTIFACTS
# ============================================================================
@app.get("/api/models/comparison", tags=["Model Evaluation"])
def get_model_comparison_data():
    """Returns Phase 2 benchmarking metrics and comparison table."""
    metrics_path = os.path.join(PROJECT_ROOT, "models", "metrics.json")
    if not os.path.exists(metrics_path):
        raise HTTPException(status_code=404, detail="Benchmark metrics not found.")

    with open(metrics_path, "r") as f:
        data = json.load(f)
    return data


@app.get("/api/health", tags=["System"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "model_loaded": moderation_engine.is_loaded,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
