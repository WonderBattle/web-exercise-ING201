#!/usr/bin/env python3
"""
Direct test execution script
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def run_basic_tests():
    """Run basic API tests"""
    print("Running basic API tests...")

    try:
        from fastapi.testclient import TestClient
        from src.app import app

        client = TestClient(app)

        # Test 1: Get activities
        print("1. Testing GET /activities...")
        response = client.get("/activities")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        activities = response.json()
        assert isinstance(activities, dict), "Activities should be a dict"
        assert len(activities) > 0, "Should have activities"

        print(f"   ✓ Found {len(activities)} activities")

        # Test 2: Signup
        print("2. Testing POST /activities/Chess Club/signup...")
        test_email = "pytest.test@mergington.edu"
        response = client.post("/activities/Chess Club/signup", params={"email": test_email})
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        result = response.json()
        assert "message" in result, "Should have message in response"

        print(f"   ✓ Signup successful: {result['message']}")

        # Verify signup worked
        response = client.get("/activities")
        activities = response.json()
        assert test_email in activities["Chess Club"]["participants"], "Email should be in participants"

        print("   ✓ Signup verified in activities list")

        # Test 3: Remove
        print("3. Testing DELETE /activities/Chess Club/remove...")
        response = client.delete("/activities/Chess Club/remove", params={"email": test_email})
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        result = response.json()
        assert "message" in result, "Should have message in response"

        print(f"   ✓ Remove successful: {result['message']}")

        # Verify removal worked
        response = client.get("/activities")
        activities = response.json()
        assert test_email not in activities["Chess Club"]["participants"], "Email should not be in participants"

        print("   ✓ Removal verified in activities list")

        # Test 4: Error cases
        print("4. Testing error cases...")

        # Activity not found
        response = client.post("/activities/NonExistent/signup", params={"email": test_email})
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        print("   ✓ Activity not found error handled")

        # Already signed up
        response = client.post("/activities/Chess Club/signup", params={"email": "michael@mergington.edu"})
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        print("   ✓ Already signed up error handled")

        print("\n🎉 All tests passed successfully!")

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure dependencies are installed: pip install -r requirements.txt")
        return False
    except AssertionError as e:
        print(f"❌ Test assertion failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_basic_tests()
    sys.exit(0 if success else 1)