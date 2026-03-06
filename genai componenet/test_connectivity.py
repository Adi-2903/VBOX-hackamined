import os
from dotenv import load_dotenv
from services.openrouter_client import call_llm

def test_connectivity():
    load_dotenv()
    
    api_key = os.getenv("PROMPT_GEN_API_KEY")
    base_url = os.getenv("OPENROUTER_BASE_URL")
    model_name = os.getenv("MODEL_NAME")
    
    print(f"API Key: {api_key[:10]}...")
    print(f"Base URL: {base_url}")
    print(f"Model Name: {model_name}")
    
    if not api_key or not base_url or not model_name:
        print("Error: Missing environment variables.")
        return

    print("\nTesting LLM call...")
    try:
        response = call_llm("Hello, return 'OK' if you can hear me.")
        print(f"Response: {response}")
        if "OK" in response.upper():
            print("\nConnectivity Test: SUCCESS")
        else:
            print("\nConnectivity Test: PARTIAL SUCCESS (Got response but not 'OK')")
    except Exception as e:
        print(f"\nConnectivity Test: FAILED - {e}")

if __name__ == "__main__":
    test_connectivity()
