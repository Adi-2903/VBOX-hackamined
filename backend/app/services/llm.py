import os
import json
import logging
import httpx
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

from app.services.prompts import (
    DIRECTION_LIBRARY,
    HOOK_LIBRARY,
    STORY_PROMPT_TEMPLATE,
    ML_EPISODE_ANALYSIS_PROMPT
)

logger = logging.getLogger(__name__)

API_KEY = os.getenv("PROMPT_GEN_API_KEY", "").strip()
BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").strip()
MODEL = os.getenv("MODEL_NAME", "qwen/qwen3.5-flash-02-23").strip()

async def call_llm_async(prompt: str) -> str:
    if not API_KEY:
        logger.warning("PROMPT_GEN_API_KEY not set. Ensure .env is loaded.")
        raise ValueError("Missing LLM API Key")

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
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
    except Exception as e:
        logger.error(f"LLM Call failed: {str(e)}")
        raise

def _extract_json(text: str) -> dict:
    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end != -1:
        return json.loads(text[start:end])
    return json.loads(text)

async def generate_directions_async(concept: str) -> Dict[str, Any]:
    prompt = f"""You are a short-form content strategist.
Based on the user idea, suggest 3 possible storytelling DIRECTIONS from the direction library.

User Idea:
{concept}

Direction Library:
{DIRECTION_LIBRARY}

Return JSON only:
{{
  "suggested_directions": [
    {{
      "direction_name": "...",
      "category": "...",
      "why_it_fits": "..."
    }}
  ]
}}"""
    try:
        response = await call_llm_async(prompt)
        return _extract_json(response)
    except Exception as e:
        logger.error(f"Direction parse or LLM call failed: {e}")
        # Default fallback
        from app.dummy_data import generate_dummy_directions
        return generate_dummy_directions(concept)

async def generate_series_async(concept: str, num_episodes: int, genres: list[str], audience: str, direction: str) -> Dict[str, Any]:
    prompt = STORY_PROMPT_TEMPLATE.replace("{idea}", str(concept))
    prompt = prompt.replace("{audience}", str(audience))
    prompt = prompt.replace("{episodes}", str(num_episodes))
    prompt = prompt.replace("{hook_library}", HOOK_LIBRARY)
    prompt = prompt.replace("{direction_library}", DIRECTION_LIBRARY)
    prompt = prompt.replace("{direction}", str(direction))

    try:
        response = await call_llm_async(prompt)
        return _extract_json(response)
    except Exception as e:
        logger.error(f"Story parse or LLM call failed: {e}")
        # Default fallback
        from app.dummy_data import generate_dummy_series
        return generate_dummy_series(concept, num_episodes, direction, audience)

async def analyze_episode_async(text: str, category: str) -> Dict[str, Any]:
    cat = category or "drama"
    prompt = ML_EPISODE_ANALYSIS_PROMPT.replace("{text}", str(text)).replace("{category}", cat)

    try:
        response = await call_llm_async(prompt)
        return _extract_json(response)
    except Exception as e:
        logger.error(f"Analysis parse or LLM call failed: {e}")
        from app.dummy_data import analyze_dummy_episode
        return analyze_dummy_episode(text=text, category=cat)

async def analyze_series_async(episodes: list[dict], category: str) -> Dict[str, Any]:
    # Analyze each episode concurrently using the LLM (or sequentially if rate limits apply)
    # To be safe against basic OpenRouter rate limits, we'll do sequentially
    analyses = []
    for ep in episodes:
        ep_text = ep.get("story", "")
        ep_title = ep.get("title", "Untitled")
        ep_num = ep.get("episode_number", 1)
        
        # Call the LLM analyzer
        analysis_data = await analyze_episode_async(ep_text, category)
        
        analyses.append({
            "episode_number": ep_num,
            "title": ep_title,
            "analysis": analysis_data
        })
    
    # Generate series insights
    scores = [a["analysis"]["summary"]["overall_score"] for a in analyses]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0
    weakest = min(range(len(scores)), key=lambda i: scores[i]) + 1 if scores else 1
    strongest = max(range(len(scores)), key=lambda i: scores[i]) + 1 if scores else 1

    if len(scores) >= 3:
        first_half = sum(scores[:len(scores) // 2]) / (len(scores) // 2)
        second_half = sum(scores[len(scores) // 2:]) / (len(scores) - len(scores) // 2)
        trend = "improving" if second_half > first_half + 3 else ("declining" if first_half > second_half + 3 else "stable")
    else:
        trend = "stable"
        
    return {
        "episodes": analyses,
        "series_insights": {
            "avg_overall_score": avg_score,
            "trend": trend,
            "consistency_score": round(1.0 - (max(scores) - min(scores)) / 100, 2) if scores else 1.0,
            "weakest_episode": weakest,
            "strongest_episode": strongest,
            "improvement_areas": ["Enhance cliffhangers further", "Tighten setup hooks"]
        }
    }
