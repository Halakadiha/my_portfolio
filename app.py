import os
import re
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

# ---------- Flask-Mail Configuration ----------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'aseijuro20@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'epiyvwbndsrdioke')
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

mail = Mail(app)

# ---------- Helper Functions ----------

def get_user():
    return {
        "name": "Jollyrad Stephen Delima",
        "title": "Virtual Assistant & IT Professional",
        "description": "I'm learning web development and building a portfolio.",
        "image": "profile.jpg"
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
        return [
            {"title": "Portfolio Website", "description": "This site built with Flask and templates"},
            {"title": "Task Tracker", "description": "A simple CLI task manager"},
            {"title": "Data Entry Automation", "description": "Scripts to speed up Excel work"}
        ]

def save_message(entry):
    """Append a message to messages.json safely."""
    mfile = data_path('messages.json')
    try:
        data = []
        if os.path.exists(mfile):
            with open(mfile, 'r', encoding='utf-8') as f:
                data = json.load(f)
        data.append(entry)
        with open(mfile, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        app.logger.exception("Failed to save message")
        return False

def valid_email(email):
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
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

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
            return render_template('contact.html', user=user, form={'name': name, 'email': email, 'message': message})

        # Save message to JSON
        entry = {"name": name, "email": email, "message": message, "timestamp": datetime.utcnow().isoformat()}
        save_message(entry)

        # Send email to your Gmail
        try:
            msg = Message(
                subject=f"New message from {name}",
                sender=app.config['MAIL_DEFAULT_SENDER'],
                recipients=[app.config['MAIL_USERNAME']],
                body=f"From: {name} <{email}>\n\nMessage:\n{message}"
            )
            mail.send(msg)
            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            app.logger.error(f"Email sending failed: {e}")
            flash("Message saved, but email sending failed.", "warning")

        return redirect(url_for('contact'))

    return render_template('contact.html', user=user, form={})

@app.route('/api/projects')
def api_projects():
    return {"projects": load_projects()}

@app.route('/experiences')
def experiences():
    try:
        with open('experiences.json', 'r', encoding='utf-8') as f:
            experiences = json.load(f)
    except Exception:
        experiences = []
    return render_template('experiences.html', experiences=experiences)

@app.route('/projects')
def projects_page():
    projects = load_projects()
    return render_template('projects.html', projects=projects, current_year=datetime.now().year)

@app.route('/project_test')
def project_test():
    user = get_user()
    projects = load_projects()
    return render_template('project_test.html', user=user, projects=projects, current_year=datetime.now().year)

@app.route('/test-mail')
def test_mail():
    try:
        msg = Message('Hello from Flask', recipients=[app.config['MAIL_USERNAME']])
        msg.body = 'This is a test email sent from your Flask app!'
        mail.send(msg)
        return 'Mail sent successfully!'
    except Exception as e:
        return f'Failed to send mail: {e}'

@app.context_processor
def inject_user():
    return dict(user=get_user())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


# ---------- Run App ----------
if __name__ == '__main__':
    app.run(debug=True)
