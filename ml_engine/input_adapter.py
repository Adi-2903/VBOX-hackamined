"""
Input Adapter for Gen AI Episode Format
Converts Gen AI JSON format to ML pipeline input format
"""


def parse_genai_episode(episode_data: dict) -> dict:
    """
    Parse Gen AI episode format and prepare for ML analysis.
    
    Args:
        episode_data: Dict with keys:
            - episode_number: int
            - title: str
            - hook: str (provided by Gen AI)
            - story: str (main content)
            - cliffhanger: str (provided by Gen AI)
            - text_overlays_suggestions: list[str]
    
    Returns:
        {
            "full_text": str,  # Combined text for analysis
            "hook_text": str,  # Provided hook
            "story_text": str,  # Main story
            "cliffhanger_text": str,  # Provided cliffhanger
            "metadata": dict  # Episode metadata
        }
    """
    hook = episode_data.get("hook", "")
    story = episode_data.get("story", "")
    cliffhanger = episode_data.get("cliffhanger", "")
    
    # Combine all text for full analysis
    full_text = f"{hook} {story} {cliffhanger}"
    
    return {
        "full_text": full_text,
        "hook_text": hook,
        "story_text": story,
        "cliffhanger_text": cliffhanger,
        "metadata": {
            "episode_number": episode_data.get("episode_number"),
            "title": episode_data.get("title", ""),
            "text_overlays": episode_data.get("text_overlays_suggestions", []),
        }
    }


def parse_genai_series(series_data: dict) -> list[dict]:
    """
    Parse Gen AI series format (multiple episodes).
    
    Args:
        series_data: Dict with keys:
            - category: str
            - direction: str
            - hook: str (series-level hook)
            - episodes: list[dict]
    
    Returns:
        List of parsed episode dicts
    """
    episodes = series_data.get("episodes", [])
    return [parse_genai_episode(ep) for ep in episodes]


def extract_hook_cliffhanger_features(parsed_episode: dict) -> dict:
    """
    Extract features from provided hook and cliffhanger.
    
    Since Gen AI already provides hook and cliffhanger,
    we can analyze them separately for quality.
    
    Args:
        parsed_episode: Output from parse_genai_episode
    
    Returns:
        {
            "hook_length": int,
            "hook_word_count": int,
            "cliffhanger_length": int,
            "cliffhanger_word_count": int,
            "has_question_hook": bool,
            "has_ellipsis_cliffhanger": bool,
        }
    """
    hook = parsed_episode["hook_text"]
    cliffhanger = parsed_episode["cliffhanger_text"]
    
    return {
        "hook_length": len(hook),
        "hook_word_count": len(hook.split()),
        "cliffhanger_length": len(cliffhanger),
        "cliffhanger_word_count": len(cliffhanger.split()),
        "has_question_hook": "?" in hook,
        "has_ellipsis_cliffhanger": "..." in cliffhanger or "\u2026" in cliffhanger,
        "has_number_hook": any(char.isdigit() for char in hook),
        "has_number_cliffhanger": any(char.isdigit() for char in cliffhanger),
    }
