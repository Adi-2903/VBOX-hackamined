import json
from pathlib import Path
from services.openrouter_client import call_llm

hook_library = Path("prompts/hook_library.txt").read_text(encoding="utf-8")
direction_library = Path("prompts/direction_library.txt").read_text(encoding="utf-8")
story_prompt_template = Path("prompts/story_prompt.txt").read_text(encoding="utf-8")


def generate_story(idea, audience, episodes, direction):

    # Use manual replacement to avoid KeyError with literal braces in JSON part of template
    prompt = story_prompt_template
    prompt = prompt.replace("{idea}", str(idea))
    prompt = prompt.replace("{audience}", str(audience))
    prompt = prompt.replace("{episodes}", str(episodes))
    prompt = prompt.replace("{hook_library}", str(hook_library))
    prompt = prompt.replace("{direction_library}", str(direction_library))
    prompt = prompt.replace("{direction}", str(direction))

    response = call_llm(prompt)

    try:
        start = response.find("{")
        end = response.rfind("}") + 1
        if start != -1 and end != -1:
            return json.loads(response[start:end])
        return json.loads(response)
    except Exception as e:
        return {"error": f"Story parse failed: {str(e)}", "raw_response": response}