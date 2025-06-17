import os
import json
import requests
from dotenv import load_dotenv
import streamlit as st

# Load API key from Streamlit secrets (for deployment)
try:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
except KeyError:
    # Fallback: load from .env file (for local testing)
    load_dotenv(dotenv_path="C:/Users/Tesla Laptops/Desktop/rumaisa/class assignments/assignment1/assignment/src/assignment/.env")
    API_KEY = os.getenv("OPENROUTER_API_KEY")

# Streamlit styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #670D2F;
    }
    </style>
    """,
    unsafe_allow_html=True
)

API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://multi-ai-chatbot-t.streamlit.app/",  # your app's URL
    "X-Title": "Multi-AI Chatbot"
}

MODELS = {
    "GPT-3.5 Turbo": "openai/gpt-3.5-turbo",
    "Qwen": "qwen/qwen3-14b:free",
    "DeepSeek": "deepseek/deepseek-r1-0528:free",
    "LLaMA 3 70B": "meta-llama/llama-3-70b-instruct",
    "Google Gemma": "google/gemma-3-12b-it:free"
}

st.title("🤖 Multi-AI Chatbot")

model_name = st.selectbox("Choose an AI model:", list(MODELS.keys()), key="model_selector")
model = MODELS[model_name]

prompt = st.text_input("Enter your prompt:")

if st.button("Get Answer"):
    if not API_KEY:
        st.error("API key not loaded. Check your secrets or .env file.")
    elif not prompt:
        st.warning("Please enter a prompt.")
    else:
        st.info("Fetching response...")
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload)
            data = response.json()

            if "choices" in data and data["choices"]:
                content = data["choices"][0]["message"]["content"]
            else:
                content = str(data)

            st.subheader(f"Response from {model_name}")
            st.write(content)

        except Exception as e:
            st.error(f"Error from {model_name}: {str(e)}")
