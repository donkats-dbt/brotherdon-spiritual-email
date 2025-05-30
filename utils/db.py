# utils/db.py

import sqlite3
import os

# Get full path to the database file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, '..', 'brotherdon.db')

def get_connection():
    return sqlite3.connect(DB_FILE)

def add_subscriber(name, email):
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("INSERT INTO subscribers (name, email) VALUES (?, ?)", (name, email))
            conn.commit()
    except sqlite3.IntegrityError:
        print(f"Duplicate email not added: {email}")

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
    emails = get_removal_emails()
    if not emails:
        return 0
    with get_connection() as conn:
        c = conn.cursor()
        placeholders = ','.join(['?'] * len(emails))
        c.execute(f"DELETE FROM subscribers WHERE email IN ({placeholders})", emails)
        c.execute("DELETE FROM removals")
        conn.commit()
        return c.rowcount
