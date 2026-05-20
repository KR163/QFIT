import streamlit as st
import pandas as pd
import database as db

# --- CUSTOM CSS INJECTION FOR PREMIUM LOOK ---
def inject_custom_styles():
    st.markdown("""
        <style>
            .reportview-container { background: #0f172a; }
            .metric-box {
                background-color: #1e293b;
                padding: 24px;
                border-radius: 16px;
                border-left: 6px solid #3b82f6;
                box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
                margin-bottom: 20px;
            }
            .metric-box.nutrition { border-left-color: #f59e0b; }
            .metric-box.training { border-left-color: #10b981; }
            .metric-title {
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 0.1em;
                color: #94a3b8;
                font-weight: 600;
                margin-bottom: 8px;
            }
            .metric-value {
                font-size: 18px;
                color: #f8fafc;
                white-space: pre-line;
                line-height: 1.6;
            }
            .stButton>button { border-radius: 8px; font-weight: 600; }
        </style>
    """, unsafe_allow_html=True)

# --- LOGIN VIEW ---
def render_login():
    inject_custom_styles()
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<div style='text-align: center; margin-top: 50px;'><h1 style='font-size: 2.5rem;'>⚡ QUANTUM FITNESS</h1><p style='color: #94a3b8;'>Next-Generation Personal Training Portal</p></div>", unsafe_allow_html=True)
        st.write("")
        with st.container(border=True):
            st.subheader("Secure Access Gateway")
            code_input = st.text_input("Enter Portal Access Code", type="password", placeholder="••••••••")
            if st.button("Authenticate", use_container_width=True, type="primary"):
                user_data = db.verify_user(code_input)
                if user_data:
                    st.session_state['authenticated'] = True
                    st.session_state['role'] = user_data[0]
                    st.session_state['name'] = user_data[1]
                    st.session_state['goal'] = user_data[2]
                    st.session_state['training'] = user_data[3]
                    st.session_state['nutrition'] = user_data[4]
                    st.rerun()
                else:
                    st.error("Access denied. Invalid token code.")
        st.markdown("<p style='text-align: center; color: #475569; font-size: 12px; margin-top: 20px;'>Demo Codes: COACH123</p>", unsafe_allow_html=True)

# --- COACH VIEW ---
def render_coach_dashboard():
    inject_custom_styles()
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("⚙️ Management Console")
        st.write(f"Authenticated Session: **Coach {st.session_state['name']}**")
    with col2:
        st.write("")
        if st.button("Terminate Session", type="secondary", use_container_width=True):
            st.session_state.clear()
            st.rerun()
            
    st.divider()
    tab_enroll, tab_records = st.tabs(["➕ Enroll New Client", "📂 Active Client Records"])
    
    with tab_enroll:
        st.subheader("Client Provisioning Profile")
        with st.form("client_generation_form", clear_on_submit=True):
            c_name = st.text_input("Full Name", placeholder="John Doe")
            c_goal = st.selectbox("Strategic Metric Goal", ["Muscle Hypertrophy", "Body Fat Reduction", "Absolute Strength", "Athletic Conditioning"])
            c_training = st.text_area("Custom Training Protocol Architecture", placeholder="e.g., 4-Day Upper/Lower Split Focus...")
            c_nutrition = st.text_area("Macro Nutritional Mapping", placeholder="e.g., 180g Protein, 250g Carbs...")
            
            submit = st.form_submit_button("Generate Client Portal Account", type="primary")
            if submit:
                if c_name.strip() and c_training.strip():
                    generated_token = db.create_client(c_name, c_goal, c_training, c_nutrition)
                    st.success(f"Account Provisioned! Secure Entry Code for {c_name}:")
                    st.code(generated_token, language="text")
                else:
                    st.error("Validation Error: Client Name and Training Protocol fields are mandatory.")
                    
    with tab_records:
        st.subheader("System Database Logs")
        raw_data = db.fetch_all_clients()
        if raw_data:
            df = pd.DataFrame(raw_data, columns=["Access Code", "Client Name", "Target Goal", "Training Protocol", "Nutrition Blueprint", "Enrollment Date"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("System memory empty. No clients currently registered under this coach database.")

# --- CLIENT VIEW ---
def render_client_dashboard():
    inject_custom_styles()
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title(f"Welcome Back, {st.session_state['name']} 👋")
        st.write("Your real-time personalized performance and nutritional roadmap.")
    with col2:
        st.write("")
        if st.button("Exit Portal", type="secondary", use_container_width=True):
            st.session_state.clear()
            st.rerun()
            
    st.divider()
    
    st.markdown(f"<div class='metric-box'><div class='metric-title'>🎯 Target Objective</div><div class='metric-value'>{st.session_state['goal']}</div></div>", unsafe_allow_html=True)
    left_col, right_col = st.columns(2)
    with left_col:
        st.markdown(f"<div class='metric-box training'><div class='metric-title'>🏋️‍♂️ Assigned Training Protocol</div><div class='metric-value'>{st.session_state['training']}</div></div>", unsafe_allow_html=True)
    with right_col:
        st.markdown(f"<div class='metric-box nutrition'><div class='metric-title'>🍏 Macro Nutritional Blueprint</div><div class='metric-value'>{st.session_state['nutrition']}</div></div>", unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Quantum PT Platform", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")
    db.init_db()
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if not st.session_state['authenticated']:
        render_login()
    else:
        if st.session_state['role'] == 'admin':
            render_coach_dashboard()
        else:
            render_client_dashboard()

if __name__ == "__main__":
    main()
