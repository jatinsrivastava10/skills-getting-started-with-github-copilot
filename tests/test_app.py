from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # basic sanity check for a known activity
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    test_email = "pytest-test@example.com"

    # Ensure clean start
    if test_email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(test_email)

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp.status_code == 200
    assert test_email in activities[activity]["participants"]

    # Unregister
    resp = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert resp.status_code == 200
    assert test_email not in activities[activity]["participants"]
