from google import genai
import os

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def ask_ai(prompt):
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )
    return response.text