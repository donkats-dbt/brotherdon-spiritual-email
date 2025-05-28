# Project Structure Scaffold

# /DailyMessages/
# ├── app_insert.py         ← Flask: subscriber form (add)
# ├── app_remove.py         ← Flask: unsubscribe form (remove)
# ├── apps.py               ← Flask: render/send message
# ├── utils/
# │   ├── storage.py       ← JSON read/write helpers
# │   ├── message_picker.py ← Pick random or weekly message
# │   └── email_sender.py    ← SendGrid or SMTP logic
# ├── templates/
# │   ├── form_insert.html
# │   ├── form_remove.html
# │   └── email_template.html
# ├── subscribers.json
# ├── remove_message.json
# ├── daily_message.json
# └── requirements.txt

# Shared utils/storage.py
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..')


def load_json(file):
    path = os.path.join(DATA_DIR, file)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}


def save_json(file, data):
    path = os.path.join(DATA_DIR, file)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


# app_insert.py (subscriber add)
from flask import Flask, render_template, request
from utils.storage import load_json, save_json

app = Flask(__name__)

@app.route("/subscribe", methods=["GET", "POST"])
def subscribe():
    message = ""
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()

        data = load_json("subscribers.json")
        subscribers = data.get("subscribers", [])

        if any(s["email"] == email for s in subscribers):
            message = f"{email} is already subscribed."
        else:
            subscribers.append({"name": name, "email": email})
            save_json("subscribers.json", {"subscribers": subscribers})
            message = f"{email} added to the list."

    return render_template("form_insert.html", message=message)


# app_remove.py (unsubscribe)
from flask import Flask, render_template, request
from utils.storage import load_json, save_json

app = Flask(__name__)

@app.route("/unsubscribe", methods=["GET", "POST"])
def unsubscribe():
    message = ""
    if request.method == "POST":
        email = request.form["email"].strip().lower()

        removal_data = load_json("remove_message.json")
        removal_list = removal_data.get("removals", [])

        if email not in removal_list:
            removal_list.append(email)
            save_json("remove_message.json", {"removals": removal_list})
            message = f"{email} has been marked for removal."
        else:
            message = f"{email} is already marked for removal."

    return render_template("form_remove.html", message=message)


# apps.py (send weekly message and clean removals)
from utils.storage import load_json, save_json


def remove_subscribers():
    subs = load_json("subscribers.json").get("subscribers", [])
    removals = load_json("remove_message.json").get("removals", [])
    new_subs = [s for s in subs if s["email"] not in removals]
    save_json("subscribers.json", {"subscribers": new_subs})
    print(f"Removed {len(subs) - len(new_subs)} subscribers.")


def send_weekly():
    # Placeholder for actual email sending
    from utils.message_picker import pick_random
    from utils.email_sender import send_email

    subs = load_json("subscribers.json").get("subscribers", [])
    message = pick_random()

    for s in subs:
        send_email(s["email"], message)


if __name__ == "__main__":
    remove_subscribers()
    send_weekly()
