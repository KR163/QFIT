import sqlite3

def init_db():
    conn = sqlite3.connect('fitness_system.db')
    c = conn.cursor()
    # الهيكل الجديد ليدعم البيانات والتمارين
    c.execute('DROP TABLE IF EXISTS users')
    c.execute('''CREATE TABLE users 
                 (code TEXT PRIMARY KEY, name TEXT, goal TEXT, 
                  sat TEXT, sun TEXT, mon TEXT, tue TEXT, wed TEXT, thu TEXT, fri TEXT)''')
    conn.commit()
    conn.close()

def add_user(code, name, goal, sat, sun, mon, tue, wed, thu, fri):
    conn = sqlite3.connect('fitness_system.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users VALUES (?,?,?,?,?,?,?,?,?,?)", 
              (code, name, goal, sat, sun, mon, tue, wed, thu, fri))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect('fitness_system.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    data = c.fetchall()
    conn.close()
    return data

def get_user(code):
    conn = sqlite3.connect('fitness_system.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE code = ?", (code,))
    data = c.fetchone()
    conn.close()
    return data
