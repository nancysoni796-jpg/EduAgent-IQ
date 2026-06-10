import streamlit as st
import google.generativeai as genai
import os

# Page configuration
st.set_page_config(
    page_title="EduAgent-IQ",
    page_icon="🎓",
    layout="wide"
)

# App Title & Description
st.title("🎓 EduAgent-IQ")
st.markdown("### Smart Study with AI Reasoning, Concept Comparison, Study Notes, and Instant Quizzes.")
st.write("Welcome! This AI agent uses advanced reasoning to answer your study questions with precise citations and generate instant quizzes to test your knowledge.")

# Sidebar for API Key configuration
st.sidebar.header("EduAgent Settings")
api_key = st.secrets["GEMINI_API_KEY"]
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
if api_key:
    genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")
learning_level = st.selectbox(
    "Select Learning Level",
    ["School", "Intermediate", "College"]
)
tab1, tab2, tab3, tab4, tab5 = st.tabs(
["📚 Cited Q&A", "📝 Instant Quiz", "⚖️ Compare Concepts", "📒 Study Notes", "🎯 Learning Tips"]
)

with tab1:
    st.header("Ask Your Study Question")
    user_query = st.text_area("Enter your question or paste your study material text here:", placeholder="e.g., Explain photosynthesis and provide sources/citations.")
    
    if st.button("Analyze & Answer"):
        if not api_key:
            st.error("Please provide an API Key first!")
        elif not user_query:
            st.warning("Please enter a question.")
        else:
            with st.spinner("AI Agent is reasoning and searching for verified facts..."):
                try:
                    prompt = f"""
Provide a detailed and factually accurate answer for a {learning_level} student.

Question:
{user_query}

Explain according to the selected learning level.
Use simple language for School level and more technical detail for College level.
Include examples when helpful.
"""
                    response = model.generate_content(prompt)
                    st.success("Analysis Complete!")
                    st.markdown("#### Verified Answer with Citations:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

with tab2:
    st.header("Generate an Instant Quiz")
    topic = st.text_input("Enter a topic or subject for the quiz:", placeholder="e.g., Indian Constitution, Basic Physics")
    num_questions = st.slider("Number of questions:", min_value=3, max_value=10, value=5)
    
    if st.button("Generate Quiz"):
        if not api_key:
            st.error("Please provide an API Key first!")
        elif not topic:
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Creating your custom quiz..."):
                try:
                    quiz_prompt = f"Create a multiple-choice quiz with {num_questions} questions on the topic: {topic}. Include options (A, B, C, D) and provide the correct answers at the very end."
                    quiz_response = model.generate_content(quiz_prompt)
                    st.success("Quiz Generated successfully!")
                    st.markdown(quiz_response.text)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
with tab3:
    st.header("Compare Two Concepts")

    concept1 = st.text_input("First Concept")
    concept2 = st.text_input("Second Concept")

    if st.button("Compare Concepts"):
        if not api_key:
            st.error("Please provide an API Key first!")
        elif not concept1 or not concept2:
            st.warning("Enter both concepts.")
        else:
            compare_prompt = f"""
            Compare {concept1} and {concept2}.

            Include:
            1. Definition
            2. Key Differences
            3. Advantages
            4. Disadvantages
            5. Which is better and when
            """

            response = model.generate_content(compare_prompt)

            st.markdown(response.text)
                  
with tab4:
    st.header("Generate Study Notes")

    notes_topic = st.text_input(
        "Enter Topic for Notes"
    )

    if st.button("Create Notes"):
        if not api_key:
            st.error("Please provide an API Key first!")
        elif not notes_topic:
            st.warning("Enter a topic.")
        else:
            notes_prompt = f"""
            Create concise study notes on:
            {notes_topic}

            Include:
            - Key Concepts
            - Important Facts
            - Quick Revision Points
            - Summary
            """

            notes = model.generate_content(
                notes_prompt
            )

            st.markdown(notes.text)
with tab5:
    st.header("AI Learning Tips")

    topic = st.text_input("Enter Topic for Learning Tips")

    if st.button("Get Learning Tips"):
        if not api_key:
            st.error("Please provide an API Key first!")
        elif not topic:
            st.warning("Enter a topic.")
        else:
            tips_prompt = f"""
            Give study tips for learning:
            {topic}

            Include:
            - Best way to learn
            - Common mistakes
            - Revision strategy
            - Exam preparation tips
            """

            tips = model.generate_content(tips_prompt)

            st.markdown(tips.text)