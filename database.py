import sqlite3
import random
import string
from datetime import datetime

DB_NAME = "core_fitness.db"

def init_db():
    """Initializes the database and creates tables with standard schemas."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        # Users Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                access_code TEXT UNIQUE NOT NULL,
                role TEXT NOT NULL, -- 'admin' or 'client'
                name TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        
        # Fitness Plans Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS plans (
                client_code TEXT PRIMARY KEY,
                goal TEXT NOT NULL,
                training_split TEXT NOT NULL,
                nutrition_macros TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(client_code) REFERENCES users(access_code) ON DELETE CASCADE
            )
        """)
        
        # Insert Default Coach Account if not exists
        cursor.execute("SELECT * FROM users WHERE role='admin'")
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO users (access_code, role, name, created_at) 
                VALUES ('COACH123', 'admin', 'Head Coach', ?)
            """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
            
        conn.commit()

def verify_user(access_code):
    """Fetches user details and their plan if they are a client."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.role, u.name, p.goal, p.training_split, p.nutrition_macros 
            FROM users u
            LEFT JOIN plans p ON u.access_code = p.client_code
            WHERE u.access_code = ?
        """, (access_code.strip().upper(),))
        return cursor.fetchone()

def create_client(name, goal, training, nutrition):
    """Generates a secure unique access code and stores the client data."""
    # Generate random 6-character alphanumeric code
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (access_code, role, name, created_at) 
                VALUES (?, 'client', ?, ?)
            """, (code, name, timestamp))
            
            cursor.execute("""
                INSERT INTO plans (client_code, goal, training_split, nutrition_macros, updated_at) 
                VALUES (?, ?, ?, ?, ?)
            """, (code, goal, training, nutrition, timestamp))
            
            conn.commit()
            return code
        except sqlite3.IntegrityError:
            return create_client(name, goal, training, nutrition)

def fetch_all_clients():
    """Retrieves all registered clients for the coach panel view."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.access_code, u.name, p.goal, p.training_split, p.nutrition_macros, u.created_at
            FROM users u
            JOIN plans p ON u.access_code = p.client_code
            WHERE u.role = 'client'
            ORDER BY u.id DESC
        """)
        return cursor.fetchall()
