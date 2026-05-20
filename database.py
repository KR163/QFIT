import sqlite3

def init_db():
    conn = sqlite3.connect('fitness_system.db')
    c = conn.cursor()
    # جدول المستخدمين
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (code TEXT PRIMARY KEY, name TEXT, goal TEXT)''')
    conn.commit()
    conn.close()

def add_user(code, name, goal):
    conn = sqlite3.connect('fitness_system.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users VALUES (?, ?, ?)", (code, name, goal))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect('fitness_system.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    data = c.fetchall()
    conn.close()
    return data
