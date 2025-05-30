# utils/db.py

import pymysql
import os

def get_connection():
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        cursorclass=pymysql.cursors.DictCursor
    )

def add_subscriber(name, email):
    try:
        with get_connection() as conn:
            with conn.cursor() as c:
                c.execute("INSERT INTO subscribers (name, email) VALUES (%s, %s)", (name, email))
            conn.commit()
    except pymysql.err.IntegrityError as e:
        if "1062" in str(e):  # Duplicate email
            print(f"Duplicate email not added: {email}")
        else:
            raise

def subscriber_exists(email):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute("SELECT 1 FROM subscribers WHERE email = %s", (email,))
            return c.fetchone() is not None

def get_removal_emails():
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute("SELECT email FROM removals")
            return [row['email'] for row in c.fetchall()]

def remove_marked_subscribers():
    emails_to_remove = get_removal_emails()
    if not emails_to_remove:
        return 0
    with get_connection() as conn:
        with conn.cursor() as c:
            placeholders = ','.join(['%s'] * len(emails_to_remove))
            c.execute(f"DELETE FROM subscribers WHERE email IN ({placeholders})", emails_to_remove)
            removed_count = c.rowcount
            c.execute("DELETE FROM removals")
        conn.commit()
        return removed_count
