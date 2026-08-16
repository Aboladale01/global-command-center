import os
from datetime import datetime

# pyright: reportMissingImports=false
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Security & Database Configuration
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'atolagbe_empire_master_key_2026')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///empire.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----------------------------------------------------
# DATABASE MODELS (THE MEMORY BANK)
# ----------------------------------------------------

# 1. User Model (Tracks Students & Secret King's Points)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    kings_points = db.Column(db.Integer, default=0) # Secret AKV tracker
    stage = db.Column(db.Integer, default=1)        # Ascension Funnel stage

# 2. Post Model (Tracks Daily Articles & Categories)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False) # e.g., Mindful Monday
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

# 3. Quiz Model (Gamification)
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    question = db.Column(db.String(300), nullable=False)
    option_a = db.Column(db.String(100), nullable=False)
    option_b = db.Column(db.String(100), nullable=False)
    option_c = db.Column(db.String(100), nullable=False)
    option_d = db.Column(db.String(100), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False) # 'A', 'B', 'C', or 'D'

# ----------------------------------------------------
# ROUTES
# ----------------------------------------------------

@app.route('/')
def home():
    # This grabs all your posts and shows the newest ones first!
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # This physically creates the empire.db file
    app.run(debug=True)
