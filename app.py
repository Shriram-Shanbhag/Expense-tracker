from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime, timedelta
import json
from collections import Counter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return User(user['id'], user['username'], user['password_hash'])
    return None

def get_db_connection():
    conn = sqlite3.connect('finance.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            user_obj = User(user['id'], user['username'], user['password_hash'])
            login_user(user_obj)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        existing_user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        if existing_user:
            flash('Username already exists')
            conn.close()
            return render_template('register.html')
        
        password_hash = generate_password_hash(password)
        conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get current month's expenses
    current_month = datetime.now().strftime('%Y-%m')
    conn = get_db_connection()
    
    # Get total expenses for current month
    total_expense = conn.execute('''
        SELECT SUM(amount) as total FROM expenses 
        WHERE user_id = ? AND date LIKE ?
    ''', (current_user.id, f'{current_month}%')).fetchone()['total'] or 0
    
    # Get expenses by category for current month
    category_expenses = conn.execute('''
        SELECT category, SUM(amount) as total FROM expenses 
        WHERE user_id = ? AND date LIKE ? 
        GROUP BY category
    ''', (current_user.id, f'{current_month}%')).fetchall()
    
    # Get recent expenses
    recent_expenses = conn.execute('''
        SELECT * FROM expenses 
        WHERE user_id = ? 
        ORDER BY date DESC, id DESC 
        LIMIT 10
    ''', (current_user.id,)).fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                         total_expense=total_expense,
                         category_expenses=category_expenses,
                         recent_expenses=recent_expenses)

@app.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        description = request.form['description']
        date = request.form['date']
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO expenses (user_id, amount, category, description, date) 
            VALUES (?, ?, ?, ?, ?)
        ''', (current_user.id, amount, category, description, date))
        conn.commit()
        conn.close()
        
        flash('Expense added successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('add_expense.html')

@app.route('/history')
@login_required
def history():
    # Get expenses for the last 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    conn = get_db_connection()
    expenses = conn.execute('''
        SELECT * FROM expenses 
        WHERE user_id = ? AND date BETWEEN ? AND ?
        ORDER BY date DESC
    ''', (current_user.id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))).fetchall()
    
    # Group by month and calculate totals
    monthly_expenses = {}
    monthly_stats = {}
    total_spent = 0
    total_transactions = 0
    
    for expense in expenses:
        month = expense['date'][:7]  # YYYY-MM
        if month not in monthly_expenses:
            monthly_expenses[month] = []
        monthly_expenses[month].append(expense)
        total_spent += expense['amount']
        total_transactions += 1
    
    # Calculate stats for each month
    for month, exps in monthly_expenses.items():
        amounts = [e['amount'] for e in exps]
        categories = [e['category'] for e in exps]
        monthly_stats[month] = {
            'total': sum(amounts),
            'average_per_day': sum(amounts) / 30 if amounts else 0,
            'largest': max(amounts) if amounts else 0,
            'most_used_category': Counter(categories).most_common(1)[0][0] if categories else ''
        }
    
    conn.close()
    
    return render_template('history.html', 
                         monthly_expenses=monthly_expenses,
                         monthly_stats=monthly_stats,
                         total_spent=total_spent,
                         total_transactions=total_transactions)

@app.route('/analytics')
@login_required
def analytics():
    # Get current month's data
    current_month = datetime.now().strftime('%Y-%m')
    
    conn = get_db_connection()
    
    # Get category breakdown for current month
    category_data = conn.execute('''
        SELECT category, SUM(amount) as total, COUNT(*) as count 
        FROM expenses 
        WHERE user_id = ? AND date LIKE ?
        GROUP BY category
        ORDER BY total DESC
    ''', (current_user.id, f'{current_month}%')).fetchall()
    
    # Get daily spending for current month
    daily_data = conn.execute('''
        SELECT date, SUM(amount) as total 
        FROM expenses 
        WHERE user_id = ? AND date LIKE ?
        GROUP BY date
        ORDER BY date
    ''', (current_user.id, f'{current_month}%')).fetchall()
    
    # Get monthly comparison (last 6 months)
    monthly_comparison = []
    for i in range(6):
        month_date = datetime.now() - timedelta(days=30*i)
        month_str = month_date.strftime('%Y-%m')
        total = conn.execute('''
            SELECT SUM(amount) as total FROM expenses 
            WHERE user_id = ? AND date LIKE ?
        ''', (current_user.id, f'{month_str}%')).fetchone()['total'] or 0
        monthly_comparison.append({
            'month': month_date.strftime('%B %Y'),
            'total': total
        })
    
    conn.close()
    
    return render_template('analytics.html', 
                         category_data=category_data,
                         daily_data=daily_data,
                         monthly_comparison=monthly_comparison)

@app.route('/api/expenses')
@login_required
def api_expenses():
    conn = get_db_connection()
    expenses = conn.execute('''
        SELECT * FROM expenses 
        WHERE user_id = ? 
        ORDER BY date DESC
    ''', (current_user.id,)).fetchall()
    conn.close()
    
    return jsonify([dict(expense) for expense in expenses])

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000) 