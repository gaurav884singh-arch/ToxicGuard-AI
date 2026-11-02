"""
Database Configuration & SQLAlchemy Session Management
Toxic Comment Moderation System
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "toxic_moderation.db"))
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# Thread-safe SQLite engine with WAL mode for high concurrency
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency that yields a request-scoped database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
