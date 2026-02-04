# Tests

This directory contains tests for the Mergington High School Activities API.

## Running Tests

### Prerequisites

Make sure you have the required dependencies installed:

```bash
pip install -r requirements.txt
```

### Run Tests

To run the tests using pytest:

```bash
pytest tests/ -v
```

Or using python module:

```bash
python -m pytest tests/ -v
```

### Manual Test Runner

You can also run a simple manual test:

```bash
python run_manual_tests.py
```

## Test Coverage

The tests cover:

- **GET /activities**: Retrieve all activities
- **POST /activities/{activity_name}/signup**: Sign up for activities
- **DELETE /activities/{activity_name}/remove**: Remove participants from activities
- **Error handling**: Invalid activities, already registered students, full activities, etc.

## Test Structure

- `test_main.py`: Main test file with comprehensive API tests
- `run_manual_tests.py`: Simple manual test runner for basic validation