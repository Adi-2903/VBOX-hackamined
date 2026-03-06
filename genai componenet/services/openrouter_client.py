import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PROMPT_GEN_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL")
MODEL = os.getenv("MODEL_NAME")


def call_llm(prompt: str):

    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]