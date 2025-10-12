import os
import re
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash

# Create app and folders (explicitly set folders)
app = Flask(__name__, template_folder='templates', static_folder='static')

# SECRET_KEY used for flash messages. In production, set an environment variable.
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-change-me')

# ---------- Helper functions ----------

def get_user():
    """Return your user/profile data used by templates."""
    return {
        "name": "Jollyrad Stephen Delima",
        "title": "Virtual Assistant & IT Professional",
        "description": "I'm learning web development and building a portfolio.",
        "image": "profile.jpg"  # file located at static/profile.jpg
    }

def data_path(filename):
    """Return absolute path to a data file stored in project root."""
    base = os.path.dirname(__file__)
    return os.path.join(base, filename)

def load_projects():
    """Load projects from projects.json. If missing, return defaults."""
    pfile = data_path('projects.json')
    try:
        with open(pfile, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        # fallback default projects
        return [
            {"title": "Portfolio Website", "description": "This site built with Flask and templates"},
            {"title": "Task Tracker", "description": "A simple CLI task manager"},
            {"title": "Data Entry Automation", "description": "Scripts to speed up Excel work"}
        ]

def save_message(entry):
    """Append a message to messages.json safely. Return True if saved."""
    mfile = data_path('messages.json')
    try:
        if os.path.exists(mfile):
            with open(mfile, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = []
        data.append(entry)
        with open(mfile, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        app.logger.exception("Failed to save message")
        return False

def valid_email(email):
    """Simple email validation (accepts normal addresses)."""
    return re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email) is not None

# ---------- Routes ----------

@app.route('/')
def home():
    user = get_user()
    projects = load_projects()
    return render_template('index.html', user=user, projects=projects, current_year=datetime.now().year)


@app.route('/about')
def about():
    user = get_user()
    return render_template('about.html', user=user, current_year=datetime.now().year)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    user = get_user()
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip()
        message = (request.form.get('message') or '').strip()

        errors = []
        if not name:
            errors.append("Please enter your name.")
        if not email or not valid_email(email):
            errors.append("Please enter a valid email address.")
        if not message or len(message) < 10:
            errors.append("Message must be at least 10 characters.")

        if errors:
            for e in errors:
                flash(e, 'error')
            # re-render form with previously typed data
            return render_template('contact.html', user=user, form={'name': name, 'email': email, 'message': message})
        else:
            entry = {
                "name": name,
                "email": email,
                "message": message,
                "timestamp": datetime.utcnow().isoformat()
            }
            ok = save_message(entry)
            if ok:
                flash("Thanks — your message was saved!", 'success')
            else:
                flash("Sorry, could not save your message. Try again.", 'error')
            return redirect(url_for('contact'))

    # GET
    return render_template('contact.html', user=user, form={})

# Optional: return projects as JSON (for API or deployment checks)
@app.route('/api/projects')
def api_projects():
    return {"projects": load_projects()}

def load_experiences():
    """Load experiences from experiences.json. If missing, return an empty list."""
    efile = data_path('experiences.json')
    try:
        with open(efile, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

@app.route('/experience')
def experience():
    user = get_user()
    experiences = load_experiences()
    return render_template('experiences.html', user=user, experiences=experiences, current_year=datetime.now().year)

# Run
if __name__ == '__main__':
    # debug=True helps during development
    app.run(debug=True)
