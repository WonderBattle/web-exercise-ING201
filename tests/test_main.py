"""
Tests for Mergington High School Activities API
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


class TestActivitiesAPI:
    """Test cases for the Activities API"""

    def test_get_activities(self, client):
        """Test getting all activities"""
        response = client.get("/activities")

        assert response.status_code == 200
        activities = response.json()

        # Check that we get a dictionary
        assert isinstance(activities, dict)

        # Check that we have some activities
        assert len(activities) > 0

        # Check structure of first activity
        first_activity = next(iter(activities.values()))
        required_fields = ["description", "schedule", "max_participants", "participants"]
        for field in required_fields:
            assert field in first_activity

        # Check that participants is a list
        assert isinstance(first_activity["participants"], list)

    def test_get_activities_contains_expected_data(self, client):
        """Test that activities contain expected data"""
        response = client.get("/activities")
        activities = response.json()

        # Check that Chess Club exists and has expected data
        assert "Chess Club" in activities
        chess_club = activities["Chess Club"]

        assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
        assert chess_club["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
        assert chess_club["max_participants"] == 12
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]

    def test_signup_successful(self, client):
        """Test successful signup for an activity"""
        # Use an email that shouldn't exist
        test_email = "test.student@mergington.edu"
        activity_name = "Chess Club"

        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )

        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert test_email in result["message"]
        assert activity_name in result["message"]

        # Verify the student was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert test_email in activities[activity_name]["participants"]

    def test_signup_already_registered(self, client):
        """Test signup when student is already registered"""
        test_email = "existing.student@mergington.edu"
        activity_name = "Chess Club"

        # First signup
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )

        # Second signup should fail
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )

        assert response.status_code == 400
        result = response.json()
        assert "detail" in result
        assert "already signed up" in result["detail"].lower()

    def test_signup_activity_full(self, client):
        """Test signup when activity is full"""
        activity_name = "Tennis Club"  # Only has 1 participant, max is 16
        test_email = "test.student@mergington.edu"

        # Fill up the activity
        for i in range(15):  # Max 16, already has 1, so add 15 more
            client.post(
                f"/activities/{activity_name}/signup",
                params={"email": f"student{i}@mergington.edu"}
            )

        # This should fail because activity is full
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )

        assert response.status_code == 400
        result = response.json()
        assert "detail" in result
        assert "full" in result["detail"].lower()

    def test_signup_activity_not_found(self, client):
        """Test signup for non-existent activity"""
        test_email = "test.student@mergington.edu"
        activity_name = "NonExistent Activity"

        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )

        assert response.status_code == 404
        result = response.json()
        assert "detail" in result
        assert "not found" in result["detail"].lower()

    def test_remove_participant_successful(self, client):
        """Test successful removal of a participant"""
        test_email = "test.student@mergington.edu"
        activity_name = "Programming Class"

        # First add the student
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )

        # Now remove them
        response = client.delete(
            f"/activities/{activity_name}/remove",
            params={"email": test_email}
        )

        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert test_email in result["message"]
        assert activity_name in result["message"]

        # Verify the student was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert test_email not in activities[activity_name]["participants"]

    def test_remove_participant_not_registered(self, client):
        """Test removing a participant who is not registered"""
        test_email = "not.registered@mergington.edu"
        activity_name = "Chess Club"

        response = client.delete(
            f"/activities/{activity_name}/remove",
            params={"email": test_email}
        )

        assert response.status_code == 400
        result = response.json()
        assert "detail" in result
        assert "not signed up" in result["detail"].lower()

    def test_remove_participant_activity_not_found(self, client):
        """Test removing from non-existent activity"""
        test_email = "test.student@mergington.edu"
        activity_name = "NonExistent Activity"

        response = client.delete(
            f"/activities/{activity_name}/remove",
            params={"email": test_email}
        )

        assert response.status_code == 404
        result = response.json()
        assert "detail" in result
        assert "not found" in result["detail"].lower()

    def test_root_redirect(self, client):
        """Test that root path redirects to static files"""
        response = client.get("/")

        assert response.status_code == 200
        # Since we're using TestClient, it should serve the static file
        # In a real server this would redirect, but TestClient handles static files differently

    def test_static_files_served(self, client):
        """Test that static files are served"""
        response = client.get("/static/index.html")

        assert response.status_code == 200
        assert "Mergington High School" in response.text