import streamlit as st
import requests

def ask_ai(prompt):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        response = requests.post(url, json=payload)

        if response.status_code == 200:
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"API Error: {response.text}"

    except Exception as e:
        return f"Error: {str(e)}"

