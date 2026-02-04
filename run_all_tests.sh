#!/bin/bash
# Test runner script

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running pytest tests..."
python -m pytest tests/ -v

echo "Running manual tests..."
python run_manual_tests.py

echo "Running direct tests..."
python test_runner.py