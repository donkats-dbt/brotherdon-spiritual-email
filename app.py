import os, json, random
from flask import Flask, render_template, request
from utils.db import get_removal_emails, remove_marked_subscribers, subscriber_exists, add_subscriber

app = Flask(__name__)

CURRENT = "current_message.json"
INVENTORY = "message_inventory.json"

def get_current_message():
    if os.path.exists(CURRENT):
        with open(CURRENT) as f:
            return json.load(f)
    return None

def pick_new_message():
    with open(INVENTORY) as f:
        messages = json.load(f)["messages"]
    selected = random.choice(messages)
    with open(CURRENT, "w") as f:
        json.dump(selected, f, indent=2)
    return selected

@app.route("/reset")
def reset():
    if os.path.exists(CURRENT):
        os.remove(CURRENT)
    return "Current message cleared."

@app.route("/send")
def send():
    message = get_current_message() or pick_new_message()

    # Fetch subscribers from database
    import mysql.connector
    from utils.db import get_connection

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, email FROM subscribers")
        subs = cursor.fetchall()

    log = [f"Sent to {name} <{email}>" for name, email in subs]
    return "<br>".join(log)

@app.route("/unsubscribe")
def unsubscribe():
    email = request.args.get("email", "").lower()
    if not email:
        return "No email provided."

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO removals (email) VALUES (%s)", (email,))
        conn.commit()
    return f"{email} has been marked for removal."

@app.route("/")
def landing():
    message = get_current_message() or pick_new_message()
    return render_template("landing.html", **message)

if __name__ == "__main__":
    app.run(debug=True)
