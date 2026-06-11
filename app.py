import streamlit as st
from auth import register, login
from db import Database
from ai import ask_ai

db = Database()

st.set_page_config(page_title="EduAgent SaaS", layout="wide")

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ================= LOGIN =================
if not st.session_state.user:
    st.title("🎓 EduAgent SaaS Login")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login(u, p)
            if user:
                st.session_state.user = u
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        u = st.text_input("New Username")
        p = st.text_input("New Password", type="password")

        if st.button("Register"):
            if register(u, p):
                st.success("Account created")
            else:
                st.error("User already exists")

# ================= DASHBOARD =================
else:
    st.sidebar.title(f"Welcome {st.session_state.user}")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    page = st.sidebar.selectbox(
        "Menu",
        ["AI Tutor", "Quiz Generator", "Notes", "History"]
    )

    # ---------------- AI TUTOR ----------------
    if page == "AI Tutor":
        st.header("AI Study Tutor")

        q = st.text_area("Ask anything")

        if st.button("Ask AI"):
            if q.strip():
                prompt = f"Explain for student: {q}"
                answer = ask_ai(prompt)

                db.save_chat(st.session_state.user, q, answer)

                st.markdown(answer)

    # ---------------- QUIZ ----------------
    elif page == "Quiz Generator":
        st.header("Quiz Generator")

        topic = st.text_input("Topic")

        if st.button("Generate"):
            if topic.strip():
                prompt = f"Create 5 MCQs on {topic} with answers"
                st.markdown(ask_ai(prompt))

    # ---------------- NOTES ----------------
    elif page == "Notes":
        st.header("Notes Generator")

        topic = st.text_input("Topic")

        if st.button("Create Notes"):
            if topic.strip():
                prompt = f"""
Create structured notes on {topic}:
- Key points
- Summary
- Revision tips
"""
                st.markdown(ask_ai(prompt))

    # ---------------- HISTORY ----------------
    elif page == "History":
        st.header("Your Chat History")

        chats = db.get_chats(st.session_state.user)

        for q, a in chats:
            st.markdown(f"**Q:** {q}")
            st.markdown(a)
            st.divider()