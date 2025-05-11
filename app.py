from flask import Flask, render_template, redirect, url_for, request, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DB_NAME = 'users.db'

def init_db():
    if not os.path.exists(DB_NAME):
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            with sqlite3.connect(DB_NAME) as conn:
                conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                flash("Реєстрація успішна! Тепер увійдіть.")
                return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Користувач уже існує.")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cur.fetchone()
            if user:
                session['user'] = username
                return redirect(url_for('dashboard'))
            else:
                flash("Невірні дані для входу.")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', username=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
