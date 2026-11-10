from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'atolagbe_secret_key_2026' # Required for flashing messages

# --- DATABASE SETUP FUNCTION ---
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Create leads table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS student_rewards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        akv_tokens INTEGER DEFAULT 0,
        quizzes_passed INTEGER DEFAULT 0,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
@app.route('/reader')
def reader_view():
    sample_title = "Atolagbe Academy: Digital Wealth Blueprint"
    sample_content = "Welcome to the core reading room..."
    
    total_ecosystem_tokens = 0
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Check if table exists first to prevent crashing
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='student_rewards'")
        if cursor.fetchone():
            cursor.execute("SELECT SUM(akv_tokens) FROM student_rewards")
            result = cursor.fetchone()
            total_ecosystem_tokens = result[0] if result and result[0] else 0
        conn.close()
    except Exception as e:
        print("Database error:", e)

    return render_template('reader_view.html', title=sample_title, content=sample_content, tokens=total_ecosystem_tokens)

    # Create partnerships table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS partnerships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            company TEXT,
            proposal_type TEXT NOT NULL,
            message TEXT NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Run the database setup on start
init_db()

@app.route('/partnership', methods=['GET', 'POST'])
def partnership_view():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        company = request.form.get('company')
        proposal_type = request.form.get('proposal_type')
        message = request.form.get('message')
        
        # Save to database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO partnerships (full_name, email, company, proposal_type, message)
            VALUES (?, ?, ?, ?, ?)
        ''', (full_name, email, company, proposal_type, message))
        conn.commit()
        conn.close()
        
        return render_template('partnership_success.html', name=full_name)
        
    return render_template('partnership.html')

@app.route('/quiz')
def quiz_view():
    return render_template('quiz.html')

@app.route('/reader')
def reader_view():
    sample_title = "Atolagbe Academy: Digital Wealth Blueprint"
    sample_content = "Welcome to the core reading room. Here you can read your modules, guides, and code strategies live on the screen..."
    return render_template('reader_view.html', title=sample_title, content=sample_content)
@app.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    user_email = request.form.get('email', 'guest@academy.com')
    
    # Example scoring calculation (assuming 4 total questions)
    correct_answers = int(request.form.get('score', 0))
    total_questions = 4 
    score_percentage = (correct_answers / total_questions) * 100
    
    earned_tokens = 0
    passed = False
    
    # The 75% Threshold Rule
    if score_percentage >= 75:
        passed = True
        earned_tokens = 100  # Reward for passing mastery level
        
        # Save or update rewards in database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Check if student exists in rewards table
        cursor.execute("SELECT akv_tokens FROM student_rewards WHERE email = ?", (user_email,))
        row = cursor.fetchone()
        
        if row:
            cursor.execute("UPDATE student_rewards SET akv_tokens = akv_tokens + ?, quizzes_passed = quizzes_passed + 1 WHERE email = ?", (earned_tokens, user_email))
        else:
            cursor.execute("INSERT INTO student_rewards (email, akv_tokens, quizzes_passed) VALUES (?, ?, 1)", (user_email, earned_tokens))
            
        conn.commit()
        conn.close()

    return render_template('quiz_result.html', percentage=score_percentage, passed=passed, tokens=earned_tokens)

@app.route('/download-ebook-1')
def download_ebook_1():
    return "Downloading Ebook 1..."

@app.route('/download-ebook-2')
def download_ebook_2():
    return "Downloading Ebook 2..."

@app.route('/download-ebook-3')
def download_ebook_3():
    return "Downloading Ebook 3..."

@app.route('/download-ebook-4')
def download_ebook_4():
    return "Downloading Ebook 4..."

@app.route('/download-ebook-5')
def download_ebook_5():
    return "Downloading Ebook 5..."

@app.route('/download-ebook-6')
def download_ebook_6():
    return "Downloading Ebook 6..."

# --- CAPTURE EMAIL & SAVE TO DATABASE ---
@app.route('/send-download', methods=['POST'])
def send_download():
    user_email = request.form.get('user_email')
    
    if user_email:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO leads (email) VALUES (?)", (user_email,))
        conn.commit()
        conn.close()
        flash(f"Success! The download link has been securely dispatched to {user_email}.", "success")
    else:
        flash("Please enter a valid email address.", "error")
        
    return redirect(url_for('reader_view'))

# --- SECURE CEO LEAD VIEWER DASHBOARD ---
@app.route('/ceo/leads')
def ceo_leads():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email, timestamp FROM leads ORDER BY timestamp DESC")
    leads = cursor.fetchall()
    conn.close()
    
    return render_template('ceo_leads.html', leads=leads)

@app.route('/sandbox')
def sandbox_view():
    return render_template('sandbox.html')

if __name__ == '__main__':
    app.run(debug=True)

