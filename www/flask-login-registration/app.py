from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import hashlib
import os

# Define the path to the outer folder where index.html is located
app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'www'))
#app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flash messages

# Database helper function to connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('users.db')  # Connect to the SQLite DB (create it if it doesn't exist)
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn

# Route to home page (will render the login page)
@app.route('/')
def home():
    return render_template('index.html')

# Route for login functionality (POST request for login)
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    
    if user:
        stored_password = user['password']
        # Compare hashed password with the stored one
        if hashlib.sha256(password.encode()).hexdigest() == stored_password:
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Redirect to home or dashboard after successful login
        else:
            flash('Invalid password', 'danger')
    else:
        flash('Username not found', 'danger')
    
    return redirect(url_for('home'))  # Go back to the login page if authentication fails

# Route for registration functionality (POST request for registration)
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirmPassword']
    
    if password != confirm_password:
        flash('Passwords do not match!', 'danger')
        return redirect(url_for('home'))  # Go back to the registration page
    
    conn = get_db_connection()
    existing_user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    
    if existing_user:
        flash('Username already exists', 'danger')
    else:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hash the password
        conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                     (username, email, hashed_password))
        conn.commit()
        flash('Registration successful! You can now log in.', 'success')

    conn.close()
    return redirect(url_for('home'))  # Redirect back to the login page after registration

# Route to create the database (run once to set up the DB)
@app.route('/create_db')
def create_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL)''')
    conn.commit()
    conn.close()
    return 'Database created and ready!'

if __name__ == '__main__':
    app.run(debug=True)
