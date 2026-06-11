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

    # ---------------- LOGIN ----------------
    with tab1:
        login_u = st.text_input("Username", key="login_user")
        login_p = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            if login_u and login_p:
                user = login(login_u, login_p)
                if user:
                    st.session_state.user = login_u
                    st.success("Login successful")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            else:
                st.warning("Enter username & password")

    # ---------------- REGISTER ----------------
    with tab2:
        reg_u = st.text_input("New Username", key="reg_user")
        reg_p = st.text_input("New Password", type="password", key="reg_pass")

        if st.button("Register"):
            if reg_u and reg_p:
                if register(reg_u, reg_p):
                    st.success("Account created")
                else:
                    st.error("User already exists")
            else:
                st.warning("Fill all fields")

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

        q = st.text_area("Ask your question")

        if st.button("Ask AI"):
            if q and q.strip():
                prompt = f"""
You are a helpful teacher.
Explain in simple language:

Question: {q}
"""
                answer = ask_ai(prompt)

                db.save_chat(st.session_state.user, q, answer)

                st.markdown("### Answer")
                st.write(answer)
            else:
                st.warning("Please enter a question")

    # ---------------- QUIZ ----------------
    elif page == "Quiz Generator":
        st.header("Quiz Generator")

        topic = st.text_input("Enter topic")

        if st.button("Generate Quiz"):
            if topic and topic.strip():
                prompt = f"Create 5 MCQs on {topic} with answers"
                st.write(ask_ai(prompt))
            else:
                st.warning("Enter topic")

    # ---------------- NOTES ----------------
    elif page == "Notes":
        st.header("Notes Generator")

        topic = st.text_input("Enter topic for notes")

        if st.button("Create Notes"):
            if topic and topic.strip():
                prompt = f"""
Create structured notes on {topic}:
- Key points
- Summary
- Important formulas
"""
                st.write(ask_ai(prompt))
            else:
                st.warning("Enter topic")

    # ---------------- HISTORY ----------------
    elif page == "History":
        st.header("Your Chat History")

        chats = db.get_chats(st.session_state.user)

        if chats:
            for q, a in chats:
                st.markdown("### Q:")
                st.write(q)
                st.markdown("### A:")
                st.write(a)
                st.divider()
        else:
            st.info("No chat history yet") 
                