import streamlit as st
import database as db

# إعداد الصفحة
st.set_page_config(page_title="منصة Q-Fit الاحترافية", layout="wide", page_icon="⚡")

# تنسيق CSS مخصص للمظهر الاحترافي
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    div[data-testid="stMetricValue"] { color: #00ffcc; }
    .css-1r6slb0 { background-color: #161b22; border-radius: 10px; padding: 20px; }
    </style>
""", unsafe_allow_html=True)

db.init_db()

# القائمة الجانبية
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3043/3043233.png", width=100)
    st.title("لوحة تحكم Q-Fit")
    menu = st.radio("القائمة:", ["تسجيل الدخول", "إدارة المدرب"])

if menu == "إدارة المدرب":
    password = st.text_input("كلمة سر المدرب", type="password")
    if password == "ADMIN1":
        st.header("⚙️ إضافة متدرب جديد")
        with st.form("add_user"):
            c1, c2 = st.columns(2)
            name = c1.text_input("اسم المتدرب")
            code = c2.text_input("الكود")
            goal = st.text_input("الهدف")
            sat = st.text_input("تمارين السبت")
            submit = st.form_submit_button("إضافة")
            if submit:
                db.add_user(code, name, goal, sat, "", "", "", "", "", "")
                st.success("تم إضافة المتدرب!")
    else:
        st.warning("يرجى إدخال كلمة سر المدرب")

elif menu == "تسجيل الدخول":
    st.title("مرحباً بك في عالم الاحتراف")
    code = st.text_input("أدخل كودك الشخصي:")
    if st.button("دخول"):
        user = db.get_user(code)
        if user:
            # عرض البيانات كبطاقات مرتبة
            st.success(f"أهلاً {user[1]}")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("هدفك", user[2])
            with col2:
                st.info(f"تمرين اليوم: {user[3]}")
        else:
            st.error("كود غير صحيح")
