import streamlit as st
from google import genai

# Page configuration
st.set_page_config(
    page_title="EduAgent-IQ",
    page_icon="🎓",
    layout="wide"
)

# Title
st.title("🎓 EduAgent-IQ")
st.markdown("### Smart Study AI Assistant for Q&A, Quizzes, Notes & Comparisons")

# API Key
api_key = st.secrets.get("GEMINI_API_KEY", None)

if not api_key:
    st.error("❌ GEMINI_API_KEY missing in secrets.toml")
    st.stop()

# Gemini Client (NEW SDK)
client = genai.Client(api_key=api_key)

# Sidebar
st.sidebar.header("EduAgent Settings")

learning_level = st.sidebar.selectbox(
    "Learning Level",
    ["School", "Intermediate", "College"]
)

subject = st.sidebar.selectbox(
    "Subject",
    ["Science", "Mathematics", "Computer Science", "English", "General Knowledge"]
)

answer_style = st.sidebar.selectbox(
    "Answer Style",
    ["Simple", "Detailed", "Exam-Oriented"]
)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📚 Cited Q&A", "📝 Instant Quiz", "⚖️ Compare Concepts", "📒 Study Notes", "🎯 Learning Tips"]
)

# ================= TAB 1 =================
with tab1:
    st.header("Ask Your Study Question")

    user_query = st.text_area("Enter your question")

    if st.button("Analyze & Answer", key="qa"):
        if not user_query:
            st.warning("Please enter a question.")
        else:
            try:
                prompt = f"""
You are a helpful teacher for {learning_level} students.

Question:
{user_query}

Explain in a {answer_style} style.
Include examples if needed.
"""

                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt
                )

                st.success("Answer Generated")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Error: {e}")


# ================= TAB 2 =================
with tab2:
    st.header("Generate Quiz")

    topic = st.text_input("Quiz Topic")
    num_questions = st.slider("Number of questions", 3, 10, 5)

    if st.button("Generate Quiz", key="quiz"):
        if not topic:
            st.warning("Enter topic")
        else:
            try:
                quiz_prompt = f"""
Create a multiple-choice quiz on {topic}.
Make {num_questions} questions.
Include options A, B, C, D and answers at end.
"""

                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=quiz_prompt
                )

                st.markdown(response.text)

            except Exception as e:
                st.error(f"Error: {e}")


# ================= TAB 3 =================
with tab3:
    st.header("Compare Concepts")

    c1 = st.text_input("First Concept")
    c2 = st.text_input("Second Concept")

    if st.button("Compare", key="compare"):
        if not c1 or not c2:
            st.warning("Enter both concepts")
        else:
            try:
                prompt = f"""
Compare {c1} and {c2}:
- Definition
- Differences
- Advantages
- Disadvantages
- Use cases
"""

                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )

                st.markdown(response.text)

            except Exception as e:
                st.error(f"Error: {e}")


# ================= TAB 4 =================
with tab4:
    st.header("Study Notes")

    topic = st.text_input("Topic for Notes")

    if st.button("Create Notes", key="notes"):
        if not topic:
            st.warning("Enter topic")
        else:
            try:
                prompt = f"""
Create short study notes on {topic}:
- Key concepts
- Important facts
- Revision points
- Summary
"""

                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )

                st.markdown(response.text)

            except Exception as e:
                st.error(f"Error: {e}")


# ================= TAB 5 =================
with tab5:
    st.header("Learning Tips")

    topic = st.text_input("Topic for tips")

    if st.button("Get Tips", key="tips"):
        if not topic:
            st.warning("Enter topic")
        else:
            try:
                prompt = f"""
Give study tips for {topic}:
- Best learning method
- Common mistakes
- Revision strategy
- Exam tips
"""

                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )

                st.markdown(response.text)

            except Exception as e:
                st.error(f"Error: {e}")