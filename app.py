from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re
import os

app = Flask(__name__)

# 1. SECRET VARIABLE (Secures your browser sessions)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'kingventure-super-secret-key-2026')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kingventure_secure.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 3. SQL INJECTION PREVENTION (Strict column typing)
    email = db.Column(db.String(120), unique=True, nullable=False)

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_msg = db.Column(db.String(500), nullable=False)
    bot_msg = db.Column(db.String(500), nullable=False)

with app.app_context():
    db.create_all()

# 2. INPUT VALIDATION (Checks if an email is real before saving)
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    # Safe JSON fetching prevents bad scripts
    data = request.get_json() or {}
    user_input = data.get("msg", "").strip()
    
    if not user_input:
        return jsonify({"response": "I'm listening! Tell me what's on your mind. 👑"})

    # Simple clean response logic
    msg_lower = user_input.lower()
    reply = "I am Kingventure, your marketing and meditation guide. 👑"
    if "stress" in msg_lower or "breathe" in msg_lower:
        reply = "Take a deep breath. Inhale peace, exhale tension. ❤️"
    elif "marketing" in msg_lower or "money" in msg_lower:
        reply = "Kingventure Rule #1: Consistency beats talent. Keep creating value! 💰"

    # Safe Database Insertion
    new_chat = ChatHistory(user_msg=user_input, bot_msg=reply)
    db.session.add(new_chat)
    db.session.commit()
    
    return jsonify({"response": reply})

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    email = data.get("email", "").strip()

    # Input Validation Check
    if not email or not is_valid_email(email):
        return jsonify({"status": "error", "message": "Please enter a valid email address! ❌"})

    try:
        # Parameterized insertion (stops SQL Injection)
        new_subscriber = Newsletter(email=email)
        db.session.add(new_subscriber)
        db.session.commit()
        return jsonify({"status": "success", "message": "Welcome to the Kingventure Inner Circle! 📧👑"})
    except:
        db.session.rollback()
        return jsonify({"status": "error", "message": "That email is already on our royal list! ✨"})

     if __name__==__main__
         port = int(os.environ.get("PORT", 5000))
         app.run(host="0.0.0.0", port=port)
     ```
