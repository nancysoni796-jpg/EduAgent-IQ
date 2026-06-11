import streamlit as st
from google import genai

api_key = st.secrets["GEMINI_API_KEY"]

st.write("API KEY LOADED:", bool(api_key))  # DEBUG LINE

client = genai.Client(api_key=api_key)

def ask_ai(prompt):
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )
    return response.text
