python
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

@app.route('/')
def home():
    return render_template('index.html')

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
```
