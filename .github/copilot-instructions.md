# AI Coding Guidelines for Mergington High School Activities API

## Project Overview
This is a FastAPI-based web application for students to view and sign up for extracurricular activities at Mergington High School. The backend serves a REST API while the frontend is built with vanilla HTML/CSS/JavaScript served as static files.

## Architecture
- **Backend**: FastAPI application in `src/app.py`
- **Frontend**: Static files in `src/static/` (HTML, CSS, JS)
- **Data Storage**: In-memory Python dictionaries (data resets on server restart)
- **API**: RESTful endpoints for activities management

## Key Patterns

### Data Model
Activities use activity names as string identifiers:
```python
activities = {
    "Chess Club": {
        "description": "...",
        "schedule": "...",
        "max_participants": 12,
        "participants": ["email@mergington.edu", ...]
    }
}
```
Students identified by email addresses (e.g., `student@mergington.edu`).

### API Endpoints
- `GET /activities` - Returns all activities with participant counts
- `POST /activities/{activity_name}/signup?email=student@mergington.edu` - Sign up for activity
- Root `/` redirects to `/static/index.html`

### File Structure
- `src/app.py` - Main FastAPI application
- `src/static/` - Frontend assets (HTML, CSS, JS)
- Static files mounted at `/static` path

### Development Workflow
- Run with: `uvicorn src.app:app --reload`
- API docs available at `http://localhost:8000/docs`
- VS Code debugger configured in `.vscode/launch.json`
- Dev container provides Python 3.13 environment

### Frontend Integration
JavaScript fetches from `/activities` endpoint and populates the UI dynamically. Form submissions use `encodeURIComponent()` for URL-safe activity names in POST requests.

### Code Style Notes
- Use meaningful string identifiers (activity names, emails)
- Handle HTTP exceptions for invalid activities
- Static file serving configured with `app.mount()`
- No database - all data is ephemeral</content>
<parameter name="filePath">/workspaces/web-exercise-ING201/.github/copilot-instructions.md