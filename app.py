from datetime import datetime
import os

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = os.environ.get("atolagbe_vault_master_key_2026") #THIS IS THE MISSING INK!

# Security & Database Configuration
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', "atolagbe_vault_master_key_2026")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///empire.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Vault Data Storage
vault_data = {
    "revenue": 0,
    "expenses": 0
}

# ----------------------------------------------------
# DATABASE MODELS (THE MEMORY BANK)
# ----------------------------------------------------
# 1. User Model (Tracks Students & Secret King's Points)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    kings_points = db.Column(db.Integer, default=0)
    stage = db.Column(db.Integer, default=1)

# 2. QuizQuestion Model (Tracks Quiz Questions)
class QuizQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False, default="Manifestation")
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False) # 'A', 'B', 'C', or 'D'

    def repr(self):
        return f'<QuizQuestion {self.id}>'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    kings_points = db.Column(db.Integer, default=0)
    stage = db.Column(db.Integer, default=1)

# 2. Post Model (Tracks Daily Articles & Categories)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
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
    correct_option = db.Column(db.String(1), nullable=False)

# ----------------------------------------------------
# ROUTES
# ----------------------------------------------------


@app.route('/')
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

# ----------------------------------------------------
# ROUTES & SECURITY PERIMETER
# ----------------------------------------------------

# 1. THE FRONT DOOR (Catches anyone who just types the base URL)
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

# 2. THE CHECKPOINT
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # The CEO Access Check
        if username == "Boss" and password == "Empire2026":
            session['logged_in'] = True  # Grants the VIP Wristband
            return redirect(url_for('dashboard'))
        else:
            return "Access Denied: Incorrect Credentials"
            
    return render_template('login.html')

@app.route('/quiz')
def quiz():
    # 1. The engine opens the database filing cabinet
    questions = QuizQuestion.query.all()
    
    # 2. The engine sends the questions to the HTML kitchen to be cooked
    return render_template('quiz.html', questions=questions)

# 3. THE VAULT
@app.route('/dashboard')
def dashboard():
    # SECURITY BOUNCER: If they don't have the wristband, kick them to login!
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Calculate the dynamic profit
    profit = vault_data["revenue"] - vault_data["expenses"]
    
    return render_template(
        'dashboard.html',
        revenue=vault_data["revenue"],
        expenses=vault_data["expenses"],
        revenue_data=f"₦{vault_data['revenue']:,}",
        expenses_data=f"₦{vault_data['expenses']:,}",
        profit_data=f"₦{profit:,}",
        operations_data="All Systems Nominal",
        security_data="DEFCON 5 - Secure"
    )

# 4. THE EXIT
@app.route('/logout')
def logout():
    # SHREDS THE WRISTBAND
    session.pop('logged_in', None) 
    return redirect(url_for('login'))

@app.route('/update_finance', methods=['POST'])
def update_finance():
    # Catch the numbers the CEO typed into the form
    new_rev = request.form.get('new_revenue')
    new_exp = request.form.get('new_expenses')

    # Update the Vault Memory (Convert text to numbers)
    if new_rev and new_exp:
      vault_data['revenue'] = int(new_rev)
      vault_data['expenses'] = int(new_exp)

    # Teleport back to the dashboard to see the updated chart!
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)