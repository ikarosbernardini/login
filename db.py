import sqlite3

def init_db(): # Initialize the database and create tables if they don't exist
    conn = sqlite3.connect("data/anvdata.db") # Connect to SQLite database
    c = conn.cursor() 
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''') # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            action TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''') # Create history table
    conn.commit() # Commit changes and close connection
    conn.close() # Close the database connection

