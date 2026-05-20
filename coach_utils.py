import streamlit as st
import database as db

def render_coach_panel():
    st.sidebar.title("⚙️ لوحة تحكم المدرب")
    action = st.sidebar.radio("العمليات", ["إضافة تمرين", "إدارة المتدربين"])
    
    if action == "إضافة تمرين":
        st.header("➕ إضافة تمرين جديد للمكتبة")
        cats = ["ظهر", "أرجل", "صدر", "بطن", "أكتاف", "بايسبس", "ترايسبس"]
        cat = st.selectbox("الكاتيجوري", cats)
        name = st.text_input("اسم التمرين")
        url = st.text_input("رابط الفيديو (YouTube)")
        if st.button("حفظ التمرين"):
            db.add_exercise(cat, name, url)
            st.success("تمت الإضافة بنجاح!")
