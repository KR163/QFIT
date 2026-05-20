import streamlit as st
import database as db

db.init_db()

st.title("⚡ نظام إدارة التدريب")

# كلمة سر المدرب
ADMIN_CODE = "ADMIN1"

password = st.text_input("كود الدخول:", type="password")

if password == ADMIN_CODE:
    st.header("⚙️ لوحة تحكم المدرب")
    
    # نموذج إضافة متدرب جديد
    with st.form("add_user_form"):
        name = st.text_input("اسم المتدرب")
        code = st.text_input("كود المتدرب (مثال: 6381)")
        goal = st.text_input("الهدف")
        submit = st.form_submit_button("إضافة المتدرب")
        
        if submit:
            db.add_user(code, name, goal)
            st.success(f"تم إضافة {name} بنجاح!")

    # عرض قائمة المتدربين
    st.subheader("قائمة المتدربين الحاليين")
    users = db.get_all_users()
    for u in users:
        st.write(f"👤 **{u[1]}** | 🔑 كود: `{u[0]}` | 🎯 هدف: {u[2]}")

elif password != "" and password != ADMIN_CODE:
    # هنا يدخل المتدرب (نواف مثلاً)
    user_data = db.get_user(password) # استدعاء من قاعدة البيانات
    if user_data:
        st.success(f"أهلاً بك يا {user_data[1]}! كودك: {user_data[0]}")
        st.write(f"هدفنا الحالي: {user_data[2]}")
    else:
        st.error("كود غير صحيح!")
