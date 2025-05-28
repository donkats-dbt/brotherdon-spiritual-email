# utils/db.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "subscribers.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_db():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS removals (
            email TEXT UNIQUE NOT NULL
        )
        """)
        conn.commit()


def add_subscriber(name, email):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO subscribers (name, email) VALUES (?, ?)", (name, email))
        conn.commit()


def subscriber_exists(email):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT 1 FROM subscribers WHERE email = ?", (email,))
        return c.fetchone() is not None


def get_removal_emails():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT email FROM removals")
        return [row[0] for row in c.fetchall()]


def remove_marked_subscribers():
    emails_to_remove = get_removal_emails()
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM subscribers WHERE email IN ({})".format(
            ", ".join(["?"] * len(emails_to_remove))
        ), emails_to_remove)
        removed_count = c.rowcount
        c.execute("DELETE FROM removals")
        conn.commit()
        return removed_count
