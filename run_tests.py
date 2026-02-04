#!/usr/bin/env python3
"""
Script to run tests
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import pytest
    print("pytest is available")
    # Run the tests
    sys.exit(pytest.main(["-v", "tests/"]))
except ImportError as e:
    print(f"Import error: {e}")
    print("Installing dependencies...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    # Try again
    try:
        import pytest
        sys.exit(pytest.main(["-v", "tests/"]))
    except ImportError:
        print("Failed to install dependencies")
        sys.exit(1)