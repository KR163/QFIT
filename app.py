import streamlit as st
import database as db
import coach_utils as cu

st.set_page_config(layout="wide", page_title="Q-Fit Platform")
db.init_db()

# تنسيق بصري
st.markdown("""
    <style>
    .stApp { background-color: #0f111a; color: white; }
    </style>
""", unsafe_allow_html=True)

menu = st.sidebar.selectbox("الدخول كـ", ["متدرب", "مدرب"])

if menu == "مدرب":
    cu.render_coach_panel()
else:
    st.title("⚡ منصة التدريب الذكية")
    code = st.text_input("أدخل كودك الشخصي")
    if st.button("دخول"):
        st.success("مرحباً بك! هذه تمارينك:")
        cats = ["ظهر", "أرجل", "صدر", "بطن", "أكتاف", "بايسبس", "ترايسبس"]
        
        for cat in cats:
            exercises = db.get_exercises_by_cat(cat)
            if exercises:
                st.subheader(f"🏷️ {cat}")
                cols = st.columns(3)
                for i, ex in enumerate(exercises):
                    with cols[i % 3].container(border=True):
                        st.write(f"### {ex[2]}")
                        st.video(ex[3])
                        if st.checkbox(f"تم الإنجاز {ex[0]}"):
                            st.success("عاش يا بطل! 🔥")
