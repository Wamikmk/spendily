import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = "spendly.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    existing = conn.execute(
        "SELECT id FROM users WHERE email = ?", ("demo@spendly.com",)
    ).fetchone()
    if existing:
        conn.close()
        return

    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
    )
    user_id = cursor.lastrowid

    sample_expenses = [
        (user_id, 12.50,  "Food",          "2025-05-01", "Lunch at cafe"),
        (user_id, 35.00,  "Transport",     "2025-05-02", "Monthly bus pass"),
        (user_id, 120.00, "Bills",         "2025-05-03", "Electricity bill"),
        (user_id, 45.00,  "Health",        "2025-05-04", "Pharmacy"),
        (user_id, 20.00,  "Entertainment", "2025-05-05", "Movie ticket"),
        (user_id, 80.00,  "Shopping",      "2025-05-06", "Clothing"),
        (user_id, 9.99,   "Other",         "2025-05-07", "Miscellaneous"),
        (user_id, 25.00,  "Food",          "2025-05-08", "Groceries"),
    ]
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        sample_expenses,
    )
    conn.commit()
    conn.close()
