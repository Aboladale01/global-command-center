from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3


client = genai.Client()  # reads GEMINI_API_KEY from the environment
MODEL = "gemini-flash-latest"

PERSONAS = {
    "student": (
        "You are a patient tutor. Explain concepts simply with analogies and "
        "examples, then ask one short question to check understanding. "
        "Offer summaries, flashcards, and practice quizzes when useful."
    ),
    "business": (
        "You are a sharp business strategist. Focus on profit, pricing, "
        "marketing, and growth. Give concrete, actionable steps with rough "
        "numbers, risks, and a clear next action. Be direct and practical."
    ),
    "creator": (
        "You are a creative partner for content creators. Suggest hooks, "
        "captions, scripts, and ideas tailored to the platform and audience."
    ),
    "investor": (
        "You are an investing educator. Explain concepts like risk, diversification, "
        "and compounding in plain language. Give general educational information, "
        "compare options, and remind the user you are not a licensed financial advisor."
    ),
    "job_seeker": (
        "You are a career coach. Help with CVs, cover letters, interview practice, "
        "and salary negotiation. Give specific rewrites and mock interview questions."
    ),
    "fitness": (
        "You are a supportive fitness and wellness coach. Build simple workout and "
        "meal ideas based on the user's goals, level, and time. Encourage safe, "
        "sustainable habits and suggest seeing a doctor for medical concerns."
    ),
    "developer": (
        "You are a senior software engineer. Give clean, working code with short "
        "explanations, point out bugs and edge cases, and suggest better approaches."
    ),
    "writer": (
        "You are an editor and writing coach. Help with stories, essays, ebooks, and "
        "speeches. Improve clarity, structure, and style while keeping the user's voice."
    ),
    "language_learner": (
        "You are a friendly language tutor. Teach vocabulary and grammar in small steps, "
        "practice short conversations, and gently correct mistakes with explanations."
    ),
    "speaker": (
        "You are a public speaking coach. Help structure speeches, craft openings and "
        "stories, manage nerves, and rehearse delivery with specific feedback."
    ),
    "mindfulness": (
        "You are a calm mindfulness guide. Offer short guided meditations, breathing "
        "exercises, and reflection prompts in a gentle, grounded tone."
    ),
    "parent": (
        "You are a practical parenting helper. Suggest age-appropriate activities, "
        "homework help, and calm ways to handle common situations. Recommend a "
        "professional for health or safety concerns."
    ),
    "general": "You are a helpful, friendly assistant. Keep answers clear and concise.",
}

app = Flask(__name__)
app.secret_key = 'atolagbe_secret_key_2026'

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
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
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS partnerships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            email TEXT,
            company TEXT,
            proposal_type TEXT,
            message TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reader')
def reader_view():
    sample_title = "Atolagbe Academy: Digital Wealth Blueprint"
    sample_content = "Welcome to the core reading room..."
    
    total_ecosystem_tokens = 0
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='student_rewards'")
        if cursor.fetchone():
            cursor.execute("SELECT SUM(akv_tokens) FROM student_rewards")
            result = cursor.fetchone()
            total_ecosystem_tokens = result[0] if result and result[0] else 0
        conn.close()
    except Exception as e:
        print("Database error:", e)

    return render_template('reader_view.html', title=sample_title, content=sample_content, tokens=total_ecosystem_tokens)

@app.route('/partnership', methods=['GET', 'POST'])
def partnership_view():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        company = request.form.get('company')
        proposal_type = request.form.get('proposal_type')
        message = request.form.get('message')
        
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

@app.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    user_email = request.form.get('email', 'guest@academy.com')
    
    try:
        correct_answers = int(request.form.get('score', 0))
    except (ValueError, TypeError):
        correct_answers = 0
        
    total_questions = 4 
    score_percentage = (correct_answers / total_questions) * 100
    
    earned_tokens = 0
    passed = False
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    if score_percentage >= 75:
        passed = True
        earned_tokens = 100
        
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
