import sqlite3

def init_db():
    conn = sqlite3.connect('fitness_system.db')
    c = conn.cursor()
    # جدول التمارين
    c.execute('''CREATE TABLE IF NOT EXISTS exercises 
                 (id INTEGER PRIMARY KEY, category TEXT, name TEXT, video_url TEXT)''')
    # جدول المتدربين
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (code TEXT PRIMARY KEY, name TEXT)''')
    conn.commit()
    conn.close()

def add_exercise(category, name, video_url):
    conn = sqlite3.connect('fitness_system.db')
    c = conn.cursor()
    c.execute("INSERT INTO exercises (category, name, video_url) VALUES (?,?,?)", (category, name, video_url))
    conn.commit()
    conn.close()

def get_exercises_by_cat(category):
    conn = sqlite3.connect('fitness_system.db')
    c = conn.cursor()
    c.execute("SELECT * FROM exercises WHERE category = ?", (category,))
    data = c.fetchall()
    conn.close()
    return data
