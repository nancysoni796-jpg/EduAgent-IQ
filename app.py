
import streamlit as st
from auth import register, login
from db import Database
from ai import ask_ai

db = Database()

st.set_page_config(page_title="EduAgent SaaS", layout="wide")

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ================= LOGIN / REGISTER =================
if not st.session_state.user:
    st.title("🎓 EduAgent SaaS")

    st.markdown("### Login to continue")

    tab1, tab2 = st.tabs(["Login", "Register"])

    # -------- LOGIN --------
    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            user = login(username, password)
            if user:
                st.session_state.user = username
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

    # -------- REGISTER --------
    with tab2:
        new_user = st.text_input("New Username", key="reg_user")
        new_pass = st.text_input("New Password", type="password", key="reg_pass")

        if st.button("Register"):
            if register(new_user, new_pass):
                st.success("Account created successfully")
            else:
                st.error("User already exists")

# ---------------- QUIZ ----------------
    elif menu == "Quiz Generator":
        st.header("📚 Quiz Generator")

        topic = st.text_input("Enter topic")

        if st.button("Generate Quiz"):
            if topic.strip():
                prompt = f"Create 5 multiple choice questions on {topic} with answers."
                st.write(ask_ai(prompt))
            else:
                st.warning("Enter a topic")

    # ---------------- NOTES ----------------
    elif menu == "Notes Generator":
        st.header("📝 Notes Generator")

        topic = st.text_input("Enter topic")

        if st.button("Generate Notes"):
            if topic.strip():
                prompt = f"""
Create simple study notes on {topic}:
- Key points
- Important facts
- Short summary
"""
                st.write(ask_ai(prompt))
            else:
                st.warning("Enter a topic")

    # ---------------- COMPARE CONCEPTS ----------------
    elif menu == "Compare Concepts":
        st.header("⚖️ Compare Concepts")

        concept1 = st.text_input("First Concept")
        concept2 = st.text_input("Second Concept")

        if st.button("Compare"):
            if concept1 and concept2:
                prompt = f"""
Compare {concept1} and {concept2}

Include:
- Definition
- Key Differences
- Advantages
- Disadvantages
- Which is better and when
"""
                st.write(ask_ai(prompt))
            else:
                st.warning("Enter both concepts")

    # ---------------- LEARNING TIPS ----------------
    elif menu == "Learning Tips":
        st.header("🎯 Learning Tips")

        topic = st.text_input("Enter Topic")

        if st.button("Get Tips"):
            if topic:
                prompt = f"""
Give study tips for learning {topic}

Include:
- Best learning strategy
- Common mistakes
- Revision plan
- Exam preparation tips
"""
                st.write(ask_ai(prompt))
            else:
                st.warning("Enter a topic")

    # ---------------- HISTORY ----------------
    elif menu == "History":
        st.header("📊 Your Chat History")

        chats = db.get_chats(st.session_state.user)

        if chats:
            for q, a in chats:
                st.markdown("### ❓ Question")
                st.write(q)

                st.markdown("### 💡 Answer")
                st.write(a)

                st.divider()
        else:
            st.info("No history found yet")

