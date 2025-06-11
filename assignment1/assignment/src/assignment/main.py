import os
import json
import requests
from dotenv import load_dotenv
import streamlit as st

st.markdown(
    """
    <style>
    /* Main background */
    .stApp {
        background-color: #670D2F;
    }
    </style>
    """,
    unsafe_allow_html=True
)



load_dotenv(dotenv_path="C:/Users/Tesla Laptops/Desktop/rumaisa/class assignments/assignment1/assignment/src/assignment/.env")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("OPENROUTER_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

MODELS = {
    "GPT-3.5 Turbo": "openai/gpt-3.5-turbo",
    "Qwen":"qwen/qwen3-14b:free",
    "DeepSeek": "deepseek/deepseek-r1-0528:free",
    "LLaMA 3 70B": "meta-llama/llama-3-70b-instruct",
    "Google Gemma": "google/gemma-3-12b-it:free"
}

st.title("🤖 Multi-AI Chatbot")

# Model selection dropdown
model_name = st.selectbox("Choose an AI model:", list(MODELS.keys()), key="model_selector")
model = MODELS[model_name]

# Prompt input
prompt = st.text_input("Enter your prompt:")

# Submit button
if st.button("Get Answer"):
    if not API_KEY:
        st.error("API key not loaded. Check your .env file.")
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
