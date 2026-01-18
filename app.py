from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)

# Essential for sessions and security - keep this private
app.secret_key = os.urandom(24)

# --- ROUTES ---

@app.route('/')
def index():
    # If user is already logged in, send them to home
    if 'user' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # Upgrade: Basic validation logic
    if not username or not email or not password:
        flash("All fields are required!", "error")
        return redirect(url_for('index'))

    # Upgrade: Logic to store user in 'session'
    # In a full app, you would verify against a database here
    session['user'] = username
    flash(f"Welcome back, {username}!", "success")
    return redirect(url_for('home'))

@app.route('/home')
def home():
    # Security Check: If user isn't logged in, kick them back to login
    if 'user' not in session:
        flash("Please login first.", "error")
        return redirect(url_for('index'))
    
    return render_template('home.html', user=session['user'])

@app.route('/logout')
def logout():
    # Clear the session data
    session.pop('user', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
