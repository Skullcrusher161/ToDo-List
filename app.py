"""
app.py — Hetarth's Neubrutalist To-Do App
==========================================
A B.Tech CSE project exploring Human-Computer Interaction (HCI)
principles through a bold, Pop-Art / Neubrutalist aesthetic.

Key concepts practiced:
  • Python File I/O  (JSON read / write without a database)
  • Flask routing    (HTTP GET + POST)
  • CRUD operations  (Create, Read, Update, Delete)
  • Jinja2 templates (passing Python data into HTML)
  • Post-Redirect-Get pattern (prevents duplicate form submissions)

Author: Hetarth Salat — 2nd Year B.Tech CSE
"""

import json
import os
import uuid

from flask import Flask, redirect, render_template, request, url_for

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = Flask(__name__)

# Path to the flat-file "database". Sitting next to app.py keeps things simple.
TASKS_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


# ---------------------------------------------------------------------------
# Persistence layer — manual save() and load() to show Python File I/O
# ---------------------------------------------------------------------------

def load():
    """
    Read tasks from the JSON file and return them as a Python list of dicts.

    Why not a database?
    ───────────────────
    For a small personal tool, a JSON file is perfectly fine and lets
    me practise Python's built-in `json` module. This is a common
    pattern for config files, CLI tools, and small web apps.
    """
    # Guard: if the file hasn't been created yet, return an empty list
    # so nothing downstream crashes on the very first run.
    if not os.path.exists(TASKS_FILE):
        return []

    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)          # JSON text → Python list
        except json.JSONDecodeError:
            # Corrupted or empty file — start fresh rather than crash
            return []


def save(tasks: list[dict]) -> None:
    """
    Overwrite the JSON file with the current in-memory task list.

    Opening in 'w' mode truncates (empties) the file first, so we
    always write the *complete* updated list — no risk of stale data.
    """
    # 'w' mode = overwrite; indent=2 keeps the file human-readable
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Routes — one function per CRUD action
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """
    READ — GET /
    ─────────────
    Load every task from disk, compute some stats, and pass everything
    to the Jinja2 template. The template does zero logic — Python handles it.
    """
    tasks     = load()
    total     = len(tasks)
    done      = sum(1 for t in tasks if t["done"])
    remaining = total - done

    return render_template(
        "index.html",
        tasks=tasks,
        total=total,
        done=done,
        remaining=remaining,
    )


@app.route("/add_task", methods=["POST"])
def add_task():
    """
    CREATE — POST /add_task
    ───────────────────────
    Flask reads the HTML form field called 'content' from the POST body.
    We validate it (can't be blank), build a dict, append it, and save.

    Using a UUID for the ID instead of a sequential integer prevents
    ID collisions after deletions — a common beginner bug to avoid.
    """
    content = request.form.get("content", "").strip()

    if not content:
        # Empty input: bounce back with an error flag the template can show
        return redirect(url_for("index", error="empty"))

    tasks = load()

    # Each task is a plain Python dict that maps directly to JSON
    new_task = {
        "id":      str(uuid.uuid4()),   # universally unique ID
        "content": content,
        "done":    False,               # all new tasks start as pending
    }

    tasks.append(new_task)
    save(tasks)

    # Post-Redirect-Get: redirect to GET / so pressing F5 doesn't
    # resubmit the form and accidentally create duplicate tasks.
    return redirect(url_for("index"))


@app.route("/complete_task/<task_id>", methods=["POST"])
def complete_task(task_id: str):
    """
    UPDATE — POST /complete_task/<id>
    ──────────────────────────────────
    Loop through tasks, find the matching ID, and flip the boolean.
    `not task["done"]` toggles True → False and False → True cleanly.
    """
    tasks = load()

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]   # toggle pending ↔ completed
            break                             # IDs are unique — stop early

    save(tasks)
    return redirect(url_for("index"))


@app.route("/delete_task/<task_id>", methods=["POST"])
def delete_task(task_id: str):
    """
    DELETE — POST /delete_task/<id>
    ────────────────────────────────
    Using list comprehension to filter out the deleted task.
    This returns a *new* list containing every task EXCEPT the one
    whose ID matches — clean, Pythonic, and easy to read.
    """
    tasks = load()

    # List comprehension: keep all tasks where the ID does NOT match
    tasks = [t for t in tasks if t["id"] != task_id]

    save(tasks)
    return redirect(url_for("index"))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # debug=True enables auto-reload while developing.
    # NEVER use debug=True in a production / public deployment.
    app.run(debug=True, port=5000)
