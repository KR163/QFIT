import sqlite3

def init_db():
    conn = sqlite3.connect('fitness_system.db')
    c = conn.cursor()
    # جدول المستخدمين مع كود الجهاز لضمان عدم التكرار
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (code TEXT PRIMARY KEY, name TEXT, goal TEXT, 
                  sat TEXT, sun TEXT, mon TEXT, tue TEXT, wed TEXT, thu TEXT, fri TEXT)''')
    conn.commit()
    conn.close()

def get_user(code):
    conn = sqlite3.connect('fitness_system.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE code = ?", (code,))
    data = c.fetchone()
    conn.close()
    return data
