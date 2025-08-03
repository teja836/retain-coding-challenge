# CHANGES.md

## Major Issues Identified
- SQL injection vulnerabilities due to string interpolation in SQL queries.
- No input validation or sanitization.
- Poor error handling and unclear responses.
- Improper HTTP status codes (always 200 OK).
- All logic in a single file, no separation of concerns.
- No use of Flask best practices (e.g., per-request DB connection).
- Sensitive data (DB path) hardcoded.
- No automated tests.

## Changes Made
- All SQL queries now use parameterized statements to prevent SQL injection.
- Input validation added for all endpoints (e.g., email format, required fields).
- Error handling and proper HTTP status codes implemented.
- Flask's `g` is used for per-request DB connections and teardown.
- Responses are now JSON for API consistency.
- Added docstrings for clarity.
- Kept all logic in one file for simplicity, but improved organization and readability.
- Added a minimal test file (`test_app.py`) for critical endpoints.

## Assumptions & Trade-offs
- Passwords are still stored in plaintext for simplicity (should be hashed in production).
- Did not implement user authentication/session management.
- Did not split into multiple modules to keep migration simple and setup minimal.
- Did not add logging or configuration files due to time constraints.

## With More Time
- Use SQLAlchemy ORM for better DB abstraction and migrations.
- Hash and salt passwords.
- Add more comprehensive tests and CI setup.
- Split code into blueprints/modules for scalability.
- Add environment-based configuration and logging.
- Add input/output schemas using Marshmallow or Pydantic.

## AI Usage
- Used GitHub Copilot to identify issues, refactor code, and generate tests.
- All code changes were reviewed and adjusted for clarity and correctness.
