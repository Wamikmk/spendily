# Spec: Login and Logout

## Overview

Implement working session-based login and logout so registered users can authenticate with Spendly. This step upgrades the existing `GET /login` stub into a full `GET + POST` flow: render the form, validate credentials against the database, compare the hashed password, set a Flask session on success, and redirect to the landing page. It also wires up the `/logout` stub to clear the session and redirect to landing. This is the first step that writes to `flask.session` and establishes the authentication pattern (query → check hash → set session) that all future protected routes will build on.

## Depends on

- Step 01 — Database Setup (`users` table must exist; `get_db()` must work)
- Step 02 — Registration (at least one user must exist to test login)

## Routes

- `GET /login` — render the login form — public
- `POST /login` — validate credentials, set session, redirect to landing — public
- `GET /logout` — clear session, redirect to landing — public (no login guard needed; safe to call when already logged out)

## Database changes

No database changes — the `users` table already has all required columns (`id`, `email`, `password_hash`).

## Templates

**Modify:**
- `templates/login.html` — add `<form method="POST">` with email and password fields; display flashed error/success messages
- `templates/base.html` — update the navbar to show Login/Register links when logged out and a Logout link when logged in (use `session.get("user_id")` in the template context)

## Files to change

- `app.py` — convert `login()` to handle GET and POST; import `session`, `check_password_hash`; implement `logout()` to call `session.clear()` and redirect
- `templates/login.html` — real form with POST action and error display
- `templates/base.html` — conditional navbar links based on session state

## Files to create

No new files.

## New dependencies

No new dependencies — Flask sessions and `werkzeug.security` are already installed.

## Rules for implementation

- No SQLAlchemy or ORMs — raw `sqlite3` via `get_db()` only
- Parameterised queries only — never string-format SQL
- Check passwords with `werkzeug.security.check_password_hash`; never compare plaintext
- Import `session` from `flask`; store `session["user_id"]` and `session["user_name"]` on successful login
- Validate server-side before touching the database:
  - Both email and password fields must be non-empty
  - Email must exist in `users`
  - `check_password_hash` must return `True`
- On any failure (empty fields, unknown email, wrong password): show a single generic error `"Invalid email or password."` — do not reveal which field was wrong
- On success: `flash()` a welcome message, then `redirect(url_for("landing"))`
- Logout must call `session.clear()` (not just `session.pop`), then redirect to `url_for("landing")`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Close every DB connection after use

## Definition of done

- [ ] Visiting `/login` shows a form with email and password fields
- [ ] Submitting with a correct email + password sets a session and redirects to `/`
- [ ] After login, `session["user_id"]` contains the logged-in user's integer ID
- [ ] Submitting with an empty field shows `"Invalid email or password."` and does not set a session
- [ ] Submitting with an unknown email shows the generic error and does not set a session
- [ ] Submitting with a wrong password shows the generic error and does not set a session
- [ ] Visiting `/logout` clears the session and redirects to `/`
- [ ] After logout, `session.get("user_id")` returns `None`
- [ ] The navbar shows Login/Register when logged out and Logout when logged in
- [ ] The demo user (`demo@spendly.com` / `demo123`) can log in successfully
- [ ] App starts without errors after changes to `app.py`
