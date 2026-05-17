# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**Spendly** — a Flask expense tracker built step-by-step as a teaching project. Many routes in `app.py` are intentional stubs (`"coming in Step N"`) that students implement incrementally.

## Commands

```bash
# Activate virtualenv (required before any python/flask commands)
source venv/bin/activate

# Run the dev server (port 5001, debug mode)
python app.py

# Alternative via Flask CLI
flask --app app run --debug --port 5001

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run a single test file
pytest tests/test_auth.py

# Inspect the SQLite database
sqlite3 spendly.db ".tables"
sqlite3 spendly.db "SELECT * FROM users;"
```

## Architecture

**Stack**: Flask + raw `sqlite3` + Jinja2 templates + plain CSS/JS. No ORM, no frontend framework.

**Database layer** (`database/db.py`):
- `get_db()` — opens a connection to `spendly.db` with `row_factory = sqlite3.Row` and `PRAGMA foreign_keys = ON`. Call this in every route that needs DB access; close the connection when done.
- `init_db()` — creates tables idempotently on startup.
- `seed_db()` — inserts a demo user (`demo@spendly.com` / `demo123`) and 8 sample expenses on first run; no-ops if demo user already exists.

Both `init_db()` and `seed_db()` are called inside `with app.app_context()` at module load time in `app.py`.

**Templates**: `base.html` is the shared layout (navbar, footer, Google Fonts, `style.css`, `main.js`). All page templates extend it via `{% extends "base.html" %}` and fill `{% block content %}` / `{% block scripts %}`.

**Schema**:
- `users`: id, name, email (UNIQUE), password_hash, created_at
- `expenses`: id, user_id (FK → users.id), amount (REAL), category (TEXT), date (TEXT YYYY-MM-DD), description, created_at

**Fixed expense categories**: Food, Transport, Bills, Health, Entertainment, Shopping, Other.

## Constraints

- **No ORM** — use raw `sqlite3` only.
- **Parameterized queries always** — never use string formatting in SQL.
- **Password hashing** — use `werkzeug.security.generate_password_hash` / `check_password_hash`.
- **Every DB connection** must have `PRAGMA foreign_keys = ON` (guaranteed by always using `get_db()`).
- Amounts stored as `REAL`; dates as `TEXT` in `YYYY-MM-DD` format.

## Custom slash commands

| Command | Purpose |
|---|---|
| `/user-seed` | Inserts a single realistic dummy user |
| `/seed-expense <user_id> <count> <months>` | Seeds N expenses spread across M past months for a user |
