import streamlit as st
import database as db

st.set_page_config(page_title="برنامجك المخصص", layout="centered")

# إعداد قاعدة البيانات
db.init_db()

# شريط التقدم (Progress Bar)
if 'step' not in st.session_state: st.session_state['step'] = 0

def progress_bar():
    steps = [0, 25, 50, 75, 100]
    st.progress(steps[st.session_state['step']])

# --- القمع البيعي (Funnel) ---
st.title("⚡ احصل على خطتك التدريبية")
progress_bar()

if st.session_state['step'] == 0:
    st.subheader("ما هو هدفك الأساسي؟")
    goal = st.radio("", ["بناء عضلات", "خسارة دهون", "تحسين لياقة"])
    if st.button("التالي"):
        st.session_state['goal'] = goal
        st.session_state['step'] = 1
        st.rerun()

elif st.session_state['step'] == 1:
    st.subheader("كيف تصف جسمك الحالي؟")
    # هنا يمكنك إضافة صور توضيحية باستخدام st.image
    body = st.radio("", ["نحيف", "متوسط", "سمنة"])
    if st.button("التالي"):
        st.session_state['body'] = body
        st.session_state['step'] = 2
        st.rerun()

elif st.session_state['step'] == 2:
    st.subheader("مستوى نشاطك اليومي؟")
    activity = st.select_slider("", ["خامل", "نشيط", "رياضي جداً"])
    name = st.text_input("اسمك الكريم؟")
    if st.button("تجهيز خطتي المخصصة 🚀"):
        db.save_lead(name, st.session_state['goal'], st.session_state['body'], activity)
        st.session_state['step'] = 3
        st.rerun()

elif st.session_state['step'] == 3:
    st.balloons()
    st.success("تم تحليل بياناتك بنجاح!")
    st.write("### برنامجك المخصص جاهز الآن.")
    st.info("سجل دخولك بالكود الذي سيرسله لك المدرب للبدء.")
    if st.button("ابدأ من جديد"):
        st.session_state['step'] = 0
        st.rerun()
