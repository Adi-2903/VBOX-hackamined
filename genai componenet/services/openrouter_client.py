import os
import requests
from dotenv import load_dotenv

load_dotenv()

DEFAULT_API_KEY = os.getenv("PROMPT_GEN_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL")
DEFAULT_MODEL = os.getenv("MODEL_NAME")


def call_llm(prompt: str, model: str = None, api_key: str = None):
    """
    Calls an LLM via OpenRouter.
    Allows overriding the model and API key.
    """
    target_model = model or DEFAULT_MODEL
    target_api_key = api_key or DEFAULT_API_KEY

    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {target_api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": target_model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]