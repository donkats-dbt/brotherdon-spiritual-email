import os, random
from flask import Flask, render_template, request
from utils.db import get_connection, get_removal_emails, remove_marked_subscribers, subscriber_exists, add_subscriber

app = Flask(__name__)

def get_current_message():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT category, reference, class FROM current_message ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if row:
            return {"category": row[0], "reference": row[1], "class": row[2]}
        return None

def pick_new_message():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT id, category, reference, class FROM message_inventory")
        messages = cursor.fetchall()
        if not messages:
            return {"category": "No messages", "reference": "No message inventory available.", "class": ""}

        selected = random.choice(messages)
        msg_id, category, reference, msg_class = selected

        cursor.execute("""
            INSERT INTO current_message (id, category, reference, class)
            VALUES (?, ?, ?, ?)
        """, (msg_id, category, reference, msg_class))
        conn.commit()

        return {"category": category, "reference": reference, "class": msg_class}

@app.route("/reset")
def reset():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM current_message")
        conn.commit()
    return "Current message cleared."

@app.route("/send")
def send():
    message = get_current_message() or pick_new_message()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, email FROM subscribers")
        subs = cursor.fetchall()

    log = [f"Sent to {name} <{email}> — {message['category']}" for name, email in subs]
    return "<br>".join(log)

@app.route("/unsubscribe")
def unsubscribe():
    email = request.args.get("email", "").lower()
    if not email:
        return "No email provided."

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO removals (email) VALUES (?)", (email,))
        conn.commit()
    return f"{email} has been marked for removal."

@app.route("/")
def landing():
    message = get_current_message() or pick_new_message()
    return render_template("landing.html", **message)

if __name__ == "__main__":
    app.run(debug=True)
