'python'
import sqlite3
from datetime import datetime
import csv
import io
from flask import Flask, render_template, request, redirect, url_for, Response, session

app = Flask(__name__)
# The secret key is required to power the secure login sessions
app.secret_key = 'atolagbe_empire_master_key_2026'

failed_attempts = 0 

# --- THE VAULT SETUP ---
def init_db():
    conn = sqlite3.connect('empire.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS financials (id INTEGER PRIMARY KEY, revenue INTEGER, expenses INTEGER, operations TEXT, security TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS audit_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, action TEXT)')
    
    c.execute('SELECT * FROM financials WHERE id = 1')
    if c.fetchone() is None:
        c.execute('INSERT INTO financials (id, revenue, expenses, operations, security) VALUES (1, 50000000, 5000000, "All systems 100% operational.", "0 breaches. Vault is sealed.")')
        
    conn.commit()
    conn.close()

init_db()

def add_audit_log(action_text):
    conn = sqlite3.connect('empire.db')
    now = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    conn.execute('INSERT INTO audit_logs (timestamp, action) VALUES (?, ?)', (now, action_text))
    conn.commit()
    conn.close()

# --- THE PUBLIC LOBBY (New Front Door) ---
@app.route('/')
def home():
    return render_template('index.html')

# --- THE VAULT DOOR (Hidden Entrance) ---
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    global failed_attempts 
    
    if failed_attempts >= 3:
        return render_template('login.html', error="🚨 SYSTEM LOCKDOWN: Maximum attempts exceeded. Vault sealed.")

    username = request.form.get('username')
    password = request.form.get('password')

    if username == 'Boss' and password == 'Empire2026':
        failed_attempts = 0 
        session['is_logged_in'] = True  # Handing you the VIP Pass
        add_audit_log("CEO logged into the Command Center.")
        return redirect(url_for('dashboard'))
    else:
        failed_attempts += 1
        attempts_left = 3 - failed_attempts
        if attempts_left > 0:
            error_msg = f"❌ ACCESS DENIED. Incorrect credentials. {attempts_left} attempts remaining."
        else:
            error_msg = "🚨 SYSTEM LOCKDOWN: Maximum attempts exceeded. Vault sealed."
            add_audit_log("🚨 SECURITY ALERT: 3 failed login attempts. System locked.")
        return render_template('login.html', error=error_msg)

# --- THE COMMAND CENTER ---
@app.route('/dashboard')
def dashboard():
    # SECURITY CHECK: Bounces anyone who doesn't have the VIP Pass
    if not session.get('is_logged_in'):
        return redirect(url_for('login'))

    conn = sqlite3.connect('empire.db')
    c = conn.cursor()
    c.execute('SELECT revenue, expenses, operations, security FROM financials WHERE id = 1')
    data = c.fetchone()
    c.execute('SELECT timestamp, action FROM audit_logs ORDER BY id DESC LIMIT 5')
    logs = c.fetchall()
    conn.close()
    
    raw_revenue = data[0]
    raw_expenses = data[1]
    raw_profit = raw_revenue - raw_expenses

    return render_template('dashboard.html', 
                           revenue_data=f"${raw_revenue:,}", 
                           expenses_data=f"${raw_expenses:,}",
                           profit_data=f"${raw_profit:,}",
                           operations_data=data[2], 
                           security_data=data[3],
                           audit_logs=logs,
                           revenue=raw_revenue,  # Sent cleanly for the Circle Chart
                           expenses=raw_expenses) # Sent cleanly for the Circle Chart

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

# --- THE UPDATE BUTTONS ---
@app.route('/update_finance', methods=['POST'])
def update_finance():
    new_revenue = request.form.get('new_revenue')
    new_expenses = request.form.get('new_expenses')
    if new_revenue and new_expenses:
        clean_rev = int(new_revenue.replace('$', '').replace(',', ''))
        clean_exp = int(new_expenses.replace('$', '').replace(',', ''))
        conn = sqlite3.connect('empire.db')
        conn.execute('UPDATE financials SET revenue = ?, expenses = ? WHERE id = 1', (clean_rev, clean_exp))
        conn.commit()
        conn.close()
        add_audit_log(f"Ledger Updated: Revenue ${clean_rev:,} | Expenses ${clean_exp:,}")
    return redirect(url_for('dashboard'))

@app.route('/update_operations', methods=['POST'])
def update_operations():
    new_data = request.form.get('new_status')
    if new_data:
        conn = sqlite3.connect('empire.db')
        conn.execute('UPDATE financials SET operations = ? WHERE id = 1', (new_data,))
        conn.commit()
        add_audit_log(f"Operations Updated: {new_data}")
    return redirect(url_for('dashboard'))

@app.route('/update_security', methods=['POST'])
def update_security():
    new_data = request.form.get('new_status')
    if new_data:
        conn = sqlite3.connect('empire.db')
        conn.execute('UPDATE financials SET security = ? WHERE id = 1', (new_data,))
        conn.commit()
        add_audit_log(f"Security Updated: {new_data}")
    return redirect(url_for('dashboard'))

# --- DATA EXTRACTION PROTOCOL ---
@app.route('/export_data')
def export_data():
    conn = sqlite3.connect('empire.db')
    c = conn.cursor()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['--- ATOLAGBE KINGS VENTURE FINANCIAL LEDGER ---'])
    cw.writerow(['Database ID', 'Revenue', 'Expenses', 'Operations Status', 'Security Status'])
    c.execute('SELECT * FROM financials WHERE id = 1')
    cw.writerow(c.fetchone())
    cw.writerow([])
    cw.writerow(['--- COMPLETE SYSTEM AUDIT LOG ---'])     (['Log ID', 'Timestamp', 'Action Executed'])
    c.execute('SELECT * FROM audit_logs ORDER BY id DESC')
    logs = c.fetchall()
    for log in logs:
        cw.writerow(log)
    conn.close()
    output = Response(si.getvalue(), mimetype='text/csv')
    output.headers["Content-Disposition"] = "attachment; filename=Vault_Backup.csv"
    add_audit_log("CEO executed Data Extraction Protocol (CSV Export).")
    return output

# --- LOGOUT PROTOCOL ---
@app.route('/logout')
def logout():
    session.clear() # Shreds the VIP Pass so nobody can use the Back button!
    add_audit_log("CEO locked the vault and logged out.")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
