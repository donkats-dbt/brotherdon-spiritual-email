# utils/db.py

import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def add_subscriber(name, email):
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("INSERT INTO subscribers (name, email) VALUES (%s, %s)", (name, email))
            conn.commit()
    except mysql.connector.IntegrityError as e:
        if "1062" in str(e):
            print(f"Duplicate email not added: {email}")
        else:
            raise

def subscriber_exists(email):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT 1 FROM subscribers WHERE email = %s", (email,))
        return c.fetchone() is not None

def get_removal_emails():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT email FROM removals")
        return [row[0] for row in c.fetchall()]

def remove_marked_subscribers():
    emails_to_remove = get_removal_emails()
    if not emails_to_remove:
        return 0
    with get_connection() as conn:
        c = conn.cursor()
        placeholders = ','.join(['%s'] * len(emails_to_remove))
        c.execute(f"DELETE FROM subscribers WHERE email IN ({placeholders})", emails_to_remove)
        removed_count = c.rowcount
        c.execute("DELETE FROM removals")
        conn.commit()
        return removed_count
