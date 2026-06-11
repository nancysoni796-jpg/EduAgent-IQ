
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
# ================= DASHBOARD =================
else:
    st.sidebar.title(f"👋 Welcome {st.session_state.user}")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    st.title("🎓 EduAgent AI Learning Hub")

    learning_level = st.selectbox(
        "📚 Select Learning Level",
        ["School", "Intermediate", "College"]
    )

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🤖 AI Tutor",
        "📚 Quiz",
        "📝 Notes",
        "⚖️ Compare",
        "🎯 Tips",
        "📊 History"
    ])

    # ---------- AI TUTOR ----------
    with tab1:
        st.header("🤖 AI Study Tutor")

        question = st.text_area("Ask your question")

        if st.button("Get Answer"):
            if question.strip():

                prompt = f"""
Answer for a {learning_level} student.

Question:
{question}

Explain clearly with examples.
"""

                answer = ask_ai(prompt)

                db.save_chat(
                    st.session_state.user,
                    question,
                    answer
                )

                st.subheader("Answer")
                st.write(answer)

    # ---------- QUIZ ----------
    with tab2:
        st.header("📚 Quiz Generator")

        topic = st.text_input("Quiz Topic")

        if st.button("Generate Quiz"):
            if topic:

                prompt = f"""
Create 5 multiple choice questions on {topic}.

Include:
- 4 options
- Correct answer
"""

                st.write(ask_ai(prompt))

    # ---------- NOTES ----------
    with tab3:
        st.header("📝 Notes Generator")

        topic = st.text_input("Notes Topic")

        if st.button("Generate Notes"):
            if topic:

                prompt = f"""
Create study notes on {topic}

Include:
- Key Points
- Important Facts
- Summary
"""

                st.write(ask_ai(prompt))

    # ---------- COMPARE ----------
    with tab4:
        st.header("⚖️ Compare Concepts")

        concept1 = st.text_input("First Concept")
        concept2 = st.text_input("Second Concept")

        if st.button("Compare Concepts"):
            if concept1 and concept2:

                prompt = f"""
Compare {concept1} and {concept2}

Include:
- Definition
- Differences
- Advantages
- Disadvantages
- Best Use Cases
"""

                st.write(ask_ai(prompt))

    # ---------- LEARNING TIPS ----------
    with tab5:
        st.header("🎯 Learning Tips")

        topic = st.text_input("Topic for Tips")

        if st.button("Get Learning Tips"):
            if topic:

                prompt = f"""
Give learning tips for {topic}

Include:
- Study Strategy
- Common Mistakes
- Revision Plan
- Exam Tips
"""

                st.write(ask_ai(prompt))

    # ---------- HISTORY ----------
    with tab6:
        st.header("📊 Chat History")

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


    