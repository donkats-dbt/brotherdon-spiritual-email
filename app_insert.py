# app_insert.py

from flask import Flask, render_template, request, redirect
from utils.db import subscriber_exists, add_subscriber

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        action = request.form.get("action")

        if action == "add":
            if subscriber_exists(email):
                message = f"{email} is already subscribed."
            else:
                try:
                    add_subscriber(name, email)
                    message = f"{email} added to the list."
                except Exception as e:
                    message = f"Error adding {email}: {e}"

        # Optional: redirect to avoid form resubmission on refresh
        return render_template("insert_form.html", message=message)

    return redirect("/", code=303)

if __name__ == "__main__":
    app.run(debug=True)
