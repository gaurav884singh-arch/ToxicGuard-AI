"""
Database Seeder for Toxic Comment Moderation System
Seeds 350+ realistic comments, user accounts, and moderation logs
so the admin analytics and moderation dashboards are rich and functional on initial run.
"""

import os
import sys
import random
from datetime import datetime, timedelta

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from sqlalchemy.orm import Session
from backend.database import SessionLocal, Base, engine
from backend.models import User, Comment, ModerationLog
from backend.auth import get_password_hash
from backend.moderation import moderation_engine, LABELS

SAMPLE_USERS = [
    ("admin", "admin@moderation.ai", "admin"),
    ("moderator_sarah", "sarah@moderation.ai", "admin"),
    ("alex_coder", "alex@dev.io", "user"),
    ("cyber_david", "david@web.net", "user"),
    ("elena_r", "elena@tech.org", "user"),
    ("marcus_99", "marcus@mail.com", "user"),
    ("sophia_art", "sophia@design.com", "user"),
    ("troll_hunter", "hunter@gaming.io", "user"),
    ("anonymous_user", "anon@proton.me", "user"),
    ("jordan_k", "jordan@social.com", "user"),
    ("toxic_spammer", "toxic123@throwaway.com", "user"),
    ("regular_user", "user@social.com", "user"),
]

CLEAN_SAMPLE_TEXTS = [
    "This open source project is really impressive! Kudos to the maintainers for their hard work.",
    "Can anyone explain how backpropagation handles vanishing gradients in deep recurrent nets?",
    "I really enjoyed the latest research paper on attention mechanisms in transformer models.",
    "Could we please add a section on API authentication best practices in the documentation?",
    "Great explanation! That clarified my doubt regarding database indexing and query plans.",
    "Looking forward to the upcoming tech meetup next Saturday in the community hall.",
    "Make sure to unit test your code before opening a pull request to the main branch.",
    "The dataset cleaning pipeline handled null values and slang normalization smoothly.",
    "I appreciate your constructive feedback on my pull request. I will make the requested updates.",
    "Does anyone have recommendations for high-throughput ASGI servers in production?",
    "Happy to collaborate with anyone interested in natural language processing and computer vision.",
    "The React 19 concurrent features look promising for frontend performance optimizations.",
    "Thank you for reviewing my article draft. I added the two historical citations you suggested.",
    "Tailwind CSS utility classes make responsive UI development much more enjoyable.",
    "Let us schedule a quick sync meeting tomorrow morning to finalize the sprint deliverables.",
    "Clean code and comprehensive docstrings save so much debugging time down the road.",
    "The visualization charts clearly display the multi-label class imbalance distribution.",
    "I found a minor typo in the README setup instructions under step 3. Fixed in my branch.",
    "What are the best hyperparameter tuning strategies for convolutional text classifiers?",
    "The user interface feels fast and fluid. Great work on the dark mode design palette!"
]

FLAGGED_SAMPLE_TEXTS = [
    "What the hell are you even talking about? That makes no sense whatsoever.",
    "Stop wasting everybody's time with these useless and lazy questions.",
    "Are you blind or can you just not read the documentation right in front of you?",
    "Your code is total garbage and whoever wrote this should be embarrassed.",
    "Why does every single decision by this moderation team feel completely incompetent?",
    "You clowns have ruined this platform with your ridiculous arbitrary rules.",
    "Get your facts straight before lecturing everyone like a pretentious know-it-all.",
    "I am sick and tired of these spammy posts cluttering up my feed every morning.",
    "This tutorial is absolute garbage, don't waste your time reading it.",
    "You have no idea what you are doing, please step down from being a moderator."
]

BLOCKED_SAMPLE_TEXTS = [
    "Fuck you and your stupid bullshit rules, get the fuck out of here.",
    "I will track your IP address and come find you, you are dead meat scumbag.",
    "You are a pathetic worthless moron and everybody hates you, kys idiot.",
    "Shut your fucking mouth stfu bitch, nobody asked for your garbage opinion.",
    "People from your disgusting religion are parasites who should be wiped out.",
    "I swear to god I will hunt you down and beat the living hell out of you.",
    "You complete piece of shit motherfucker, get lost before I destroy you.",
    "Go back to your own country you illegal immigrant trash, nobody wants you here.",
    "I hope you suffer and die a painful death, you useless clown.",
    "Watch your back because I know where you live and I am coming for your family."
]


def seed_database(force: bool = False) -> None:
    """Populates the database with users, comments, and moderation logs."""
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        user_count = db.query(User).count()
        if user_count > 0 and not force:
            print(f"[Database Seeder] Database already populated with {user_count} users. Skipping.")
            return

        print("[Database Seeder] Initializing database seeding...")
        moderation_engine.load_artifacts()

        # 1. Create Users
        created_users = []
        for username, email, role in SAMPLE_USERS:
            user = User(
                username=username,
                email=email,
                hashed_password=get_password_hash("Admin@1234" if role == "admin" else "User@1234"),
                role=role,
                created_at=datetime.utcnow() - timedelta(days=random.randint(30, 90)),
            )
            db.add(user)
            created_users.append(user)

        db.commit()
        for u in created_users:
            db.refresh(u)

        admin_user = next(u for u in created_users if u.role == "admin")
        regular_users = [u for u in created_users if u.role == "user"]

        print(f"[Database Seeder] Created {len(created_users)} users.")

        # 2. Seed 350+ Comments across the past 30 days
        comments_to_create = 350
        print(f"[Database Seeder] Generating {comments_to_create} realistic comments...")

        now = datetime.utcnow()

        for i in range(comments_to_create):
            author = random.choice(regular_users)
            days_ago = random.randint(0, 29)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            comment_date = now - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)

            # 75% clean, 15% flagged, 10% blocked
            rand_val = random.random()
            if rand_val < 0.75:
                text = random.choice(CLEAN_SAMPLE_TEXTS)
                if random.random() < 0.3:
                    text += " " + random.choice(["Really appreciate it!", "Good luck with the release.", "Thanks!"])
            elif rand_val < 0.90:
                text = random.choice(FLAGGED_SAMPLE_TEXTS)
            else:
                text = random.choice(BLOCKED_SAMPLE_TEXTS)

            pred = moderation_engine.predict(text)
            scores = pred["scores"]

            comment = Comment(
                user_id=author.id,
                text=text,
                toxic=scores["toxic"],
                severe_toxic=scores["severe_toxic"],
                obscene=scores["obscene"],
                threat=scores["threat"],
                insult=scores["insult"],
                identity_hate=scores["identity_hate"],
                max_score=pred["max_score"],
                status=pred["status"],
                created_at=comment_date,
            )
            db.add(comment)
            db.flush()

            # Create moderation log
            action_name = (
                "auto_approve"
                if pred["status"] == "approved"
                else "auto_flag"
                if pred["status"] == "flagged"
                else "auto_block"
            )
            log = ModerationLog(
                comment_id=comment.id,
                action=action_name,
                admin_id=None,
                notes=f"Automated policy verdict: {pred['verdict']}",
                timestamp=comment_date,
            )
            db.add(log)

            # Randomly simulate admin review on some flagged comments
            if pred["status"] == "flagged" and random.random() < 0.40:
                admin_action = "admin_approve" if random.random() < 0.50 else "admin_delete"
                comment.status = "approved" if admin_action == "admin_approve" else "blocked"
                review_log = ModerationLog(
                    comment_id=comment.id,
                    action=admin_action,
                    admin_id=admin_user.id,
                    notes="Reviewed and resolved by human moderator.",
                    timestamp=comment_date + timedelta(minutes=random.randint(5, 120)),
                )
                db.add(review_log)

        db.commit()
        total_comments = db.query(Comment).count()
        total_logs = db.query(ModerationLog).count()
        print(f"[Database Seeder] Successfully seeded {total_comments} comments and {total_logs} moderation logs.")

    except Exception as e:
        db.rollback()
        print(f"[Database Seeder] Error during database seeding: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed_database(force=True)
