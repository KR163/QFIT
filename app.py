import streamlit as st
import pandas as pd
from datetime import datetime
import database as db

# إعداد الصفحة
st.set_page_config(page_title="منصة التدريب الاحترافية", layout="wide")

# تهيئة قاعدة البيانات
db.init_db()

# --- دالة التحقق من الجهاز ---
def is_session_valid(code):
    if 'active_code' not in st.session_state:
        st.session_state['active_code'] = None
    
    if st.session_state['active_code'] is None:
        st.session_state['active_code'] = code
        return True
    return st.session_state['active_code'] == code

# --- الواجهة ---
st.title("⚡ منصة التدريب الشخصي")

code_input = st.text_input("أدخل كود الوصول الخاص بك", type="password")

if st.button("دخول"):
    user_data = db.get_user(code_input)
    if user_data and is_session_valid(code_input):
        st.session_state['user'] = user_data
    else:
        st.error("كود خاطئ أو مستخدم بالفعل على جهاز آخر!")

if 'user' in st.session_state:
    user = st.session_state['user']
    today = datetime.now().strftime("%A") # جلب اليوم الحالي
    
    # خريطة الأيام
    days = {"Saturday": user[3], "Sunday": user[4], "Monday": user[5], 
            "Tuesday": user[6], "Wednesday": user[7], "Thursday": user[8], "Friday": user[9]}
    
    st.subheader(f"مرحباً {user[1]}، جدولك اليوم ({today}) هو:")
    st.info(days.get(today, "يوم راحة"))
    
    # قسم التمارين مع الفيديو
    st.divider()
    st.subheader("فيديو تعليمي للتمرين")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # ضع رابط تمرينك هنا
    
    # حاسبة الماكروز
    st.divider()
    st.header("🧮 حاسبة الاحتياج اليومي")
    weight = st.number_input("الوزن (كجم)", 40, 150)
    if st.button("احسب"):
        st.success(f"احتياجك للبروتين: {weight * 2} جرام")
        st.write("ملاحظة: هذا تقدير تقريبي.")
