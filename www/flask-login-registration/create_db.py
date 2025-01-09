import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create users table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Commit and close the connection
conn.commit()
conn.close()

print("Database and table created successfully.")
