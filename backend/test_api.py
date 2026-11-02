"""
Automated Test Suite for Backend FastAPI Application
Toxic Comment Moderation System
"""

import os
import sys
from fastapi.testclient import TestClient

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.main import app

client = TestClient(app)


def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    print(" [PASS] Health Check")


def test_auth_login_admin():
    res = client.post("/api/auth/login", json={
        "username_or_email": "admin@moderation.ai",
        "password": "Admin@1234"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["user"]["role"] == "admin"
    print(" [PASS] Admin Login & JWT Issuance")
    return data["access_token"]


def test_auth_login_regular():
    res = client.post("/api/auth/login", json={
        "username_or_email": "user@social.com",
        "password": "User@1234"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["user"]["role"] == "user"
    print(" [PASS] Regular User Login")
    return data["access_token"]


def test_predict_clean_and_toxic():
    # Clean comment
    res_clean = client.post("/api/predict", json={
        "text": "Thank you for the helpful code review and clear suggestions!"
    })
    assert res_clean.status_code == 200
    d_clean = res_clean.json()
    assert d_clean["status"] == "approved"
    assert "Clean" in d_clean["verdict"]

    # Abusive comment
    res_toxic = client.post("/api/predict", json={
        "text": "WTF you stupid moron, stfu and get the fuck out of here!"
    })
    assert res_toxic.status_code == 200
    d_toxic = res_toxic.json()
    assert d_toxic["is_toxic"] is True
    assert d_toxic["status"] in ["flagged", "blocked"]
    print(" [PASS] Real-time Deep Learning Toxicity Prediction (Clean vs Toxic)")


def test_create_and_fetch_comments(user_token):
    # Post comment
    res = client.post(
        "/api/comments",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"text": "Collaborating on this machine learning capstone project has been great."}
    )
    assert res.status_code == 201
    c_data = res.json()
    assert c_data["status"] == "approved"

    # Fetch feed
    feed_res = client.get("/api/comments?status_filter=approved&limit=10")
    assert feed_res.status_code == 200
    feed = feed_res.json()
    assert len(feed) > 0
    print(" [PASS] Comment Submission & Feed Retrieval with Auto-Moderation")


def test_admin_flagged_queue_and_moderation(admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    queue_res = client.get("/api/admin/flagged", headers=headers)
    assert queue_res.status_code == 200
    queue = queue_res.json()
    print(f" [PASS] Admin Flagged Queue (Found {len(queue)} items for review)")

    if queue:
        target_id = queue[0]["id"]
        mod_res = client.put(
            f"/api/admin/comments/{target_id}",
            headers=headers,
            json={"action": "approve", "notes": "Approved by supervisor after review."}
        )
        assert mod_res.status_code == 200
        assert mod_res.json()["status"] == "approved"
        print(" [PASS] Admin Moderation Override Action")


def test_admin_analytics(admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    res = client.get("/api/admin/analytics", headers=headers)
    assert res.status_code == 200
    analytics = res.json()
    assert analytics["total_comments"] >= 300
    assert len(analytics["category_distribution"]) == 6
    assert len(analytics["daily_trends"]) > 0
    print(f" [PASS] Admin Analytics Dashboard (Total Comments: {analytics['total_comments']})")


def test_models_comparison_api():
    res = client.get("/api/models/comparison")
    assert res.status_code == 200
    data = res.json()
    assert "benchmark_results" in data
    assert len(data["benchmark_results"]) >= 6
    print(" [PASS] Model Benchmark Comparison API")


if __name__ == "__main__":
    print("\n========================================================")
    print("RUNNING BACKEND FASTAPI TEST SUITE")
    print("========================================================")
    test_health()
    admin_token = test_auth_login_admin()
    user_token = test_auth_login_regular()
    test_predict_clean_and_toxic()
    test_create_and_fetch_comments(user_token)
    test_admin_flagged_queue_and_moderation(admin_token)
    test_admin_analytics(admin_token)
    test_models_comparison_api()
    print("========================================================")
    print("ALL BACKEND ENDPOINTS VERIFIED & PASSING!")
    print("========================================================\n")
