# 📝 TaskCrush — Persistent Python Web-Task Manager

> **"This project focuses on Human-Computer Interaction (HCI) basics.
> I chose a bright, colorful palette to improve user mood and motivation
> while completing daily tasks."**

A B.Tech CSE portfolio project that evolves a console To-Do script into
a fully persistent, web-based task manager using Python, Flask, and a
bold Neubrutalist design language.

---

## 🎨 Design Philosophy — Why These Colors?

The UI deliberately applies **UX Color Psychology** principles:

| Color | Hex | Element | Psychological Effect |
|-------|-----|---------|----------------------|
| Cream | `#fef3c7` | Page background | Warm, non-fatiguing; easy on the eyes |
| Sunny Yellow | `#facc15` | Header + Add button | Energy, attention, optimism — draws the eye to the primary CTA |
| Sky Blue | `#38bdf8` | Task cards | Calm, focus, trust — reduces anxiety around large task lists |
| Lime Green | `#86efac` | Completed tasks | Success, growth — gives dopamine reward for finishing tasks |
| Coral | `#fb7185` | Delete button | Urgency, caution — naturally signals a destructive action |
| Orange | `#fb923c` | Validation error | Warning without panic — less alarming than red |

### The Neubrutalist "Paper" Effect

All containers use:
```css
border: 3px solid #0f172a;
box-shadow: 8px 8px 0px #0f172a;
```
The hard offset shadow mimics a physical object casting a shadow on a flat
surface — like a sticky note on a desk. It makes the UI feel **handmade**
and tactile rather than like a generic SaaS dashboard.

---

## 🎯 Learning Objectives

| Goal | Concept Practised |
|------|------------------|
| Store data without a database | Python File I/O — `json.load()` / `json.dump()` |
| Handle form submissions | Flask `request.form.get()`, POST requests |
| Prevent duplicate submissions | Post-Redirect-Get (PRG) pattern |
| Dynamic HTML from Python data | Jinja2 `{% for %}` loops, `{{ variables }}` |
| Server-side validation | Redirect with URL query param `?error=empty` |
| Responsive layout | CSS Flexbox — `justify-content: space-between` |
| Visual feedback | CSS Transitions, hover `transform: scale(1.02)` |
| Color psychology in UX | Deliberate palette mapped to user emotions |

---

## 📁 Project Structure

```
hetarth_todo/
├── app.py              # Flask backend — all routes and CRUD logic
├── tasks.json          # Auto-generated flat-file database (gitignored)
├── static/
│   └── style.css       # Neubrutalist CSS theme
├── templates/
│   └── index.html      # Jinja2 HTML template
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md           # This file
```

---

## 🚀 How to Run

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd hetarth_todo

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# 3. Install Flask
pip install -r requirements.txt

# 4. Start the server
python app.py

# 5. Open in browser
#    http://127.0.0.1:5000
```

---

## 🧠 Key Concepts Explained

### File Storage — Why JSON instead of a Database?

For a personal tool, a JSON file is a perfect lightweight storage
solution. It keeps the project dependency-free and makes the File I/O
concept the star of the show:

```python
def load():
    """Read tasks from disk into a Python list."""
    with open("tasks.json", "r") as f:
        return json.load(f)       # JSON text → Python list of dicts

def save(tasks):
    """Overwrite the JSON file with the current task list."""
    # 'w' mode truncates first — always writes the complete list
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=2)
```

### CRUD Route Map

```
CREATE → POST /add_task            → add_task()
READ   → GET  /                    → index()
UPDATE → POST /complete_task/<id>  → complete_task()
DELETE → POST /delete_task/<id>    → delete_task()
```

### Delete — List Comprehension

```python
# Using list comprehension to filter out the deleted task
tasks = [t for t in tasks if t["id"] != task_id]
```

### Validation — Server-Side Only, No JavaScript

```python
if not content:
    # Bounce back with an error flag in the URL query string
    return redirect(url_for("index", error="empty"))
```

The template then reads `request.args.get('error')` and shows
a styled orange banner if it equals `"empty"`.

---

## 🌱 My Learning Journey

**V1 (console):** `input()` prompts + `print()` in a loop — tasks lost on exit.

**V2 (this project):** Flask web server, `tasks.json` persistence, browser UI,
Neubrutalist design inspired by Figma community templates and HCI readings.

**What's next:** Add task categories, due dates, and maybe a local SQLite
database to replace the JSON file.

---

## 👤 Author

**Built with ❤️ and Python — Hetarth Salat**
*2nd Year B.Tech CSE Student*
*Persistent Python Web-Task Manager · HCI Design Project*
