#!/usr/bin/env python3
"""
Manual test runner
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_tests():
    try:
        from fastapi.testclient import TestClient
        from src.app import app

        client = TestClient(app)

        # Test 1: Get activities
        print("Test 1: Get activities")
        response = client.get("/activities")
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) > 0
        print("✓ PASSED")

        # Test 2: Signup
        print("Test 2: Signup")
        test_email = "test.student@mergington.edu"
        response = client.post("/activities/Chess Club/signup", params={"email": test_email})
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        print("✓ PASSED")

        # Test 3: Remove
        print("Test 3: Remove participant")
        response = client.delete("/activities/Chess Club/remove", params={"email": test_email})
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        print("✓ PASSED")

        # Test 4: Error cases
        print("Test 4: Error cases")
        # Activity not found
        response = client.post("/activities/NonExistent/signup", params={"email": test_email})
        assert response.status_code == 404
        print("✓ PASSED")

        print("\nAll tests passed! ✅")

    except ImportError as e:
        print(f"Import error: {e}")
        return False
    except Exception as e:
        print(f"Test failed: {e}")
        return False

    return True

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)