# CHANGES.md

## Major Issues Identified
- Poor code organization and file structure
- No input validation or error handling
- Insecure handling of sensitive data
- Hard-coded values and redundant logic

## Changes Made
- Refactored code into modular components
- Added error handling for all endpoints
- Implemented input validation using Pydantic
- Used environment variables for sensitive data
- Rewrote confusing logic for better readability

## Assumptions or Trade-Offs
- Assumed user authentication is out of scope
- Used SQLite for quick testing instead of PostgreSQL

## With More Time, I Would:
- Add full test coverage
- Migrate to PostgreSQL + Docker setup
- Implement logging and monitoring

## AI Usage
- Used ChatGPT to guide refactor structure and validate some fixes.
- All code was reviewed and customized as needed.
