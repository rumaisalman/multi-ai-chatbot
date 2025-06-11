import requests

response = requests.post(
    "http://127.0.0.1:8000/ask",
    headers={"Content-Type": "application/json"},
    json={
        "prompt": "Who is the founder of Pakistan?",
        "model": "google/gemini-2.5-flash-preview-05-20"
    }
)

print("Status Code:", response.status_code)
print("Response:", response.json())
