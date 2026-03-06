import json
import os
from pathlib import Path
from services.openrouter_client import call_llm

# Load config from env
LLAMA_KEY = os.getenv("LLAMA_KEY")
ANALYST_MODEL = os.getenv("ANALYST_MODEL")
FIXER_MODEL = os.getenv("FIXER_MODEL")

# Load prompt templates
ANALYST_PROMPT_TEMPLATE = Path("prompts/analyst_prompt.txt").read_text(encoding="utf-8")
FIXER_PROMPT_TEMPLATE = Path("prompts/fixer_prompt.txt").read_text(encoding="utf-8")


def analyze_and_fix_episode(episode_text: str, full_ml_json: dict):
    """
    Executes the two-step AI intelligence chain:
    1. Llama Analyst identifies issues based on ML scores.
    2. Mistral Fixer suggests specific script improvements.
    """
    
    # --- Step 1: Llama Analyst ---
    ml_json_str = json.dumps(full_ml_json, indent=2)
    analyst_prompt = ANALYST_PROMPT_TEMPLATE.replace("{episode_text}", episode_text)
    analyst_prompt = analyst_prompt.replace("{full_ml_json}", ml_json_str)
    
    print(f"Calling Analyst ({ANALYST_MODEL})...")
    analyst_response_raw = call_llm(analyst_prompt, model=ANALYST_MODEL, api_key=LLAMA_KEY)
    
    # Parse Analyst JSON
    try:
        start = analyst_response_raw.find("{")
        end = analyst_response_raw.rfind("}") + 1
        analyst_output = json.loads(analyst_response_raw[start:end])
    except Exception as e:
        analyst_output = {"error": f"Analyst JSON parse failed: {str(e)}", "raw": analyst_response_raw}
    
    if "error" in analyst_output:
        return {"analyst": analyst_output, "fixer": {"error": "Skipped due to analyst error"}}

    # --- Step 2: Mistral Fixer ---
    llama_output_str = json.dumps(analyst_output, indent=2)
    fixer_prompt = FIXER_PROMPT_TEMPLATE.replace("{episode_text}", episode_text)
    fixer_prompt = fixer_prompt.replace("{full_ml_json}", ml_json_str)
    fixer_prompt = fixer_prompt.replace("{llama_output_json}", llama_output_str)
    
    print(f"Calling Fixer ({FIXER_MODEL})...")
    fixer_response_raw = call_llm(fixer_prompt, model=FIXER_MODEL, api_key=LLAMA_KEY)
    
    # Parse Fixer JSON
    try:
        start = fixer_response_raw.find("{")
        end = fixer_response_raw.rfind("}") + 1
        fixer_output = json.loads(fixer_response_raw[start:end])
    except Exception as e:
        fixer_output = {"error": f"Fixer JSON parse failed: {str(e)}", "raw": fixer_response_raw}
        
    return {
        "analyst": analyst_output,
        "fixer": fixer_output
    }
