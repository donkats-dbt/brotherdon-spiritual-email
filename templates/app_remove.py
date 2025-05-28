import json
import os

SUBSCRIBERS_FILE = "subscribers.json"
REMOVE_FILE = "remove_message.json"

def load_subscribers():
    if os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, "r") as f:
            return json.load(f)
    return {"subscribers": []}

def load_removals():
    if os.path.exists(REMOVE_FILE):
        with open(REMOVE_FILE, "r") as f:
            return json.load(f).get("removals", [])
    return []

def save_subscribers(subscribers):
    with open(SUBSCRIBERS_FILE, "w") as f:
        json.dump({"subscribers": subscribers}, f, indent=2)

def remove_subscribers():
    subscribers_data = load_subscribers()
    removal_emails = load_removals()

    original_count = len(subscribers_data["subscribers"])
    updated_subscribers = [
        s for s in subscribers_data["subscribers"]
        if s["email"].lower() not in [e.lower() for e in removal_emails]
    ]
    save_subscribers(updated_subscribers)

    print(f"Removed {original_count - len(updated_subscribers)} subscribers.")
    return original_count, len(updated_subscribers)

if __name__ == "__main__":
    remove_subscribers()
