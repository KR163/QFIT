import streamlit as st
import sqlite3
import random
import string
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Quantum PT", layout="centered", initial_sidebar_state="collapsed")

# --- PREMIUM CSS STYLING ---
st.markdown("""
    <style>
    /* Hide Default Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Global App Styling */
    .stApp {
        background-color: #0b0f19;
        color: #f8fafc;
    }
    
    /* Styled Containers (Cards) */
    div[data-testid="stVerticalBlock"] > div > div > div > div[data-testid="stVerticalBlock"] {
        background: linear-gradient(145deg, #161b22, #1a202c);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #2d3748;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        margin-bottom: 15px;
    }
    
    /* Headers & Text */
    h1, h2, h3 { color: #ffffff !important; font-family: 'Helvetica Neue', sans-serif; }
    p { color: #94a3b8; }
    
    /* Checkbox Styling */
    .stCheckbox label { font-weight: bold; color: #10b981; }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('fitness_system.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS exercises 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, name TEXT, video_url TEXT)''')
    
    # Drop table to apply the new advanced multi-day scheduling system safely
    c.execute('DROP TABLE IF EXISTS users')
    c.execute('''CREATE TABLE users 
                 (code TEXT PRIMARY KEY, name TEXT, 
                  Sunday TEXT, Monday TEXT, Tuesday TEXT, Wednesday TEXT, Thursday TEXT, Friday TEXT, Saturday TEXT)''')
    conn.commit()
    conn.close()

def execute_query(query, params=()):
    conn = sqlite3.connect('fitness_system.db')
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    conn.close()

def fetch_query(query, params=()):
    conn = sqlite3.connect('fitness_system.db')
    c = conn.cursor()
    c.execute(query, params)
    data = c.fetchall()
    conn.close()
    return data

init_db()

# --- CONSTANTS ---
DAYS_OF_WEEK = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
CATEGORIES = ["Back", "Legs", "Chest", "Core", "Shoulders", "Biceps", "Triceps"]

# --- APP ROUTING ---
if 'view' not in st.session_state:
    st.session_state['view'] = 'login'

def switch_view(view_name):
    st.session_state['view'] = view_name
    st.rerun()

# --- VIEWS ---
if st.session_state['view'] == 'login':
    st.markdown("<h1 style='text-align: center; color: #3b82f6;'>⚡ QUANTUM PT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Next-Gen Training Platform</p>", unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    with st.container(border=True):
        st.subheader("Secure Login")
        code_input = st.text_input("Enter Access Code:", type="password")
        
        if st.button("Authenticate", use_container_width=True, type="primary"):
            if code_input == "ADMIN":
                switch_view("coach_dashboard")
            else:
                user = fetch_query("SELECT * FROM users WHERE code = ?", (code_input,))
                if user:
                    st.session_state['current_user_code'] = code_input
                    st.session_state['current_user_name'] = user[0][1]
                    switch_view("client_dashboard")
                else:
                    st.error("Invalid Access Code.")

elif st.session_state['view'] == 'coach_dashboard':
    st.title("⚙️ Coach Command Center")
    if st.button("Log Out", type="secondary"): switch_view('login')
    
    st.divider()
    
    tab_ex, tab_users = st.tabs(["➕ Add Exercises to Library", "👥 Manage & Schedule Clients"])
    
    with tab_ex:
        with st.container(border=True):
            st.subheader("Exercise Registration")
            c1, c2 = st.columns(2)
            cat = c1.selectbox("Target Muscle Group (Category)", CATEGORIES)
            name = c2.text_input("Exercise Nomenclature")
            url = st.text_input("YouTube Video URL")
            if st.button("Save to Library", type="primary"):
                execute_query("INSERT INTO exercises (category, name, video_url) VALUES (?,?,?)", (cat, name, url))
                st.success(f"[{name}] successfully added to the database!")

    with tab_users:
        with st.container(border=True):
            st.subheader("Client Provisioning & Scheduling")
            client_name = st.text_input("Client Full Name")
            
            # Fetch all stored exercises from library for multi-select assignment
            all_exercises = fetch_query("SELECT id, name, category FROM exercises")
            exercise_options = {f"{ex[1]} ({ex[2]})": ex[0] for ex in all_exercises}
            
            st.write("")
            st.markdown("##### Assign Specific Exercises per Day:")
            
            schedule_data = {}
            for day in DAYS_OF_WEEK:
                selected_items = st.multiselect(f"Schedule for {day}:", list(exercise_options.keys()), key=f"select_{day}")
                # Extract database row IDs as a comma-separated string
                ids_string = ",".join([str(exercise_options[item]) for item in selected_items])
                schedule_data[day] = ids_string
            
            st.write("")
            if st.button("Generate Secure Profile & Schedule", type="primary", use_container_width=True):
                if client_name:
                    new_code = ''.join(random.choices(string.digits, k=4))
                    execute_query("""
                        INSERT INTO users (code, name, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """, (new_code, client_name, schedule_data["Sunday"], schedule_data["Monday"], 
                          schedule_data["Tuesday"], schedule_data["Wednesday"], schedule_data["Thursday"], 
                          schedule_data["Friday"], schedule_data["Saturday"]))
                    st.success(f"Profile created for {client_name}! Access Code: {new_code}")
                else:
                    st.error("Please insert a valid Client Name.")

elif st.session_state['view'] == 'client_dashboard':
    current_day = datetime.now().strftime("%A")
    st.title(f"Welcome, {st.session_state['current_user_name']} 👋")
    st.markdown(f"<p style='font-size:18px;'>Today is <b style='color:#3b82f6;'>{current_day}</b>. Here is your target protocol:</p>", unsafe_allow_html=True)
    
    if st.button("Log Out", type="secondary"): switch_view('login')
    st.divider()
    
    # Query user row dynamic column based on today's day name
    user_schedule = fetch_query(f"SELECT {current_day} FROM users WHERE code = ?", (st.session_state['current_user_code'],))
    
    if user_schedule and user_schedule[0][0]:
        exercise_ids = user_schedule[0][0].split(",")
        
        # Render each assigned exercise for the current day
        for ex_id in exercise_ids:
            if ex_id:
                ex_details = fetch_query("SELECT name, category, video_url FROM exercises WHERE id = ?", (int(ex_id),))
                if ex_details:
                    name, cat, url = ex_details[0]
                    with st.container(border=True):
                        st.markdown(f"### {name} <span style='font-size:14px; color:#3b82f6;'>[{cat}]</span>", unsafe_allow_html=True)
                        if url:
                            try:
                                st.video(url)
                            except:
                                st.write(f"🔗 [Watch Video Protocol]({url})")
                        
                        if st.checkbox("MARK AS COMPLETED", key=f"today_check_{ex_id}"):
                            st.success("Target muscle activated. Excellent execution! 🔥")
    else:
        st.info("No training protocols assigned for today. Enjoy your rest day! 🧘‍♂️")
