# Spec: Registration

## Overview

Implement working user registration so new visitors can create a Spendly account. This step wires up the existing `GET /register` stub into a full `GET + POST` flow: render the form, validate input server-side, hash the password, insert the user, and redirect to login on success. It is the first step that writes user-generated data to the database and sets the pattern (validate → query → redirect) that login and all later write routes will follow.

## Depends on

- Step 01 — Database Setup (users table must exist; `get_db()` must work)

## Routes

- `GET /register` — render the registration form — public
- `POST /register` — validate form data, insert user, redirect to login — public

## Database changes

No database changes — the `users` table already exists with the correct schema (`id`, `name`, `email`, `password_hash`, `created_at`).

## Templates

**Modify:**
- `templates/register.html` — add `<form method="POST">` with fields for name, email, password, confirm password; display flashed error/success messages

**Modify (optional but recommended):**
- `templates/base.html` — add a flash message block so all pages can display `flash()` output

## Files to change

- `app.py` — convert `register()` to handle GET and POST; add `secret_key`; import `request`, `redirect`, `url_for`, `flash` from flask; import `generate_password_hash` from werkzeug
- `templates/register.html` — real form with POST action, validation error display
- `templates/base.html` — flash message rendering block (if not already present)

## Files to create

No new files.

## New dependencies

No new dependencies — Flask and `werkzeug.security` are already installed.

## Rules for implementation

- No SQLAlchemy or ORMs — raw `sqlite3` via `get_db()` only
- Parameterised queries only — never string-format SQL
- Hash passwords with `werkzeug.security.generate_password_hash`; never store plaintext
- `app.secret_key` must be set (use a hardcoded dev string for now, e.g. `"dev-secret-key"`)
- Validate all fields server-side before touching the database:
  - name, email, password, confirm_password must all be non-empty
  - password and confirm_password must match
  - email must not already exist in `users` (catch the UNIQUE constraint or pre-check with SELECT)
- On validation failure: `flash()` the error and re-render the form (do not redirect)
- On success: `flash()` a success message and `redirect(url_for("login"))`
- Use CSS variables — never hardcode hex colours
- All templates extend `base.html`
- Close every DB connection after use

## Definition of done

- [ ] Visiting `/register` shows a form with name, email, password, and confirm-password fields
- [ ] Submitting the form with all valid fields creates a new row in `users` with a hashed password
- [ ] Submitting with any empty field shows an error message and does not insert a row
- [ ] Submitting with mismatched passwords shows an error and does not insert a row
- [ ] Submitting with an already-registered email shows an error and does not insert a row
- [ ] Successful registration redirects to `/login`
- [ ] The new user can be confirmed in the DB: `sqlite3 spendly.db "SELECT id, name, email FROM users;"`
- [ ] Password column contains a hash, not plaintext
- [ ] App starts without errors after changes to `app.py`
