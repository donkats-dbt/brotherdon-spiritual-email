import os, json, random
from flask import Flask, render_template

app = Flask(__name__)

CURRENT = "current_message.json"
INVENTORY = "message_inventory.json"
SUBSCRIBERS = "subscribers.json"

def get_current_message():
    if os.path.exists(CURRENT):
        with open(CURRENT) as f:
            return json.load(f)
    else:
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
    with open(SUBSCRIBERS) as f:
        subs = json.load(f)["subscribers"]
    log = [f"Sent to {s['name']} <{s['email']}>" for s in subs]
    return "<br>".join(log)

@app.route("/unsubscribe")
def unsubscribe():
    email = request.args.get("email", "").lower()
    subscribers = load_subscribers()
    updated = [s for s in subscribers if s["email"] != email]
    save_subscribers(updated)
    return f"{email} has been unsubscribed."

@app.route("/")
def landing():
    message = get_current_message() or pick_new_message()
    return render_template("landing.html", **message)

if __name__ == "__main__":
    app.run(debug=True)