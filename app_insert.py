# app_insert.py

from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

SUBSCRIBERS_FILE = "subscribers.json"

def load_subscribers():
    if os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, "r") as f:
            data = json.load(f)
            return data.get("subscribers", [])  # extracts the list
    return []

def save_subscribers(subscribers):
    with open(SUBSCRIBERS_FILE, "w") as f:
        json.dump({"subscribers": subscribers}, f, indent=2)  # writes back in same structure


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        action = request.form["action"]

        subscribers = load_subscribers()

        if action == "add":
            if any(s["email"] == email for s in subscribers):
                message = f"{email} is already subscribed."
            else:
                subscribers.append({"name": name, "email": email})
                save_subscribers(subscribers)
                message = f"{email} added to the list."

    return render_template("form_insert.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)

