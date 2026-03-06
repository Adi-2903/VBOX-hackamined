import json
from pathlib import Path
from services.openrouter_client import call_llm

direction_library = Path("prompts/direction_library.txt").read_text(encoding="utf-8")


def generate_directions(idea: str):

    prompt = f"""
You are a short-form content strategist.

Based on the user idea, suggest 3 possible storytelling DIRECTIONS from the direction library.

User Idea:
{idea}

Direction Library:
{direction_library}

Return JSON only:

{{
  "suggested_directions": [
    {{
      "direction_name": "...",
      "category": "...",
      "why_it_fits": "..."
    }}
  ]
}}
"""

    response = call_llm(prompt)

    try:
        # Extract JSON if LLM included preamble
        start = response.find("{")
        end = response.rfind("}") + 1
        if start != -1 and end != -1:
            return json.loads(response[start:end])
        return json.loads(response)
    except Exception as e:
        return {"error": f"Direction parse failed: {str(e)}", "raw": response}