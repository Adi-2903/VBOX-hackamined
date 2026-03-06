"""
Text Processor Module
Handles sentence segmentation, text cleaning, and linguistic feature extraction.
Uses spaCy when available, falls back to regex-based processing for Python 3.14+ compatibility.
"""

import re

# Try to load spaCy, fall back gracefully
_nlp = None
_SPACY_AVAILABLE = False

try:
    import spacy
    try:
        _nlp = spacy.load("en_core_web_sm")
        _SPACY_AVAILABLE = True
    except OSError:
        try:
            from spacy.cli import download
            download("en_core_web_sm")
            _nlp = spacy.load("en_core_web_sm")
            _SPACY_AVAILABLE = True
        except Exception:
            _SPACY_AVAILABLE = False
except Exception:
    _SPACY_AVAILABLE = False


# --- Common action verbs for fallback POS tagging ---
ACTION_VERB_LIST = {
    "run", "ran", "jump", "jumped", "fight", "fought", "search", "searched",
    "grab", "grabbed", "pull", "pulled", "push", "pushed", "throw", "threw",
    "catch", "caught", "hit", "kick", "kicked", "climb", "climbed", "swim",
    "swam", "drive", "drove", "fly", "flew", "chase", "chased", "escape",
    "escaped", "attack", "attacked", "defend", "defended", "shoot", "shot",
    "scream", "screamed", "cry", "cried", "laugh", "laughed", "whisper",
    "whispered", "shout", "shouted", "walk", "walked", "arrive", "arrived",
    "leave", "left", "enter", "entered", "open", "opened", "close", "closed",
    "lock", "locked", "break", "broke", "build", "built", "create", "created",
    "destroy", "destroyed", "find", "found", "lose", "lost", "steal", "stole",
    "hide", "hid", "reveal", "revealed", "discover", "discovered", "explore",
    "explored", "travel", "traveled", "move", "moved", "start", "started",
    "stop", "stopped", "begin", "began", "end", "ended", "turn", "turned",
    "follow", "followed", "lead", "led", "approach", "approached", "disappear",
    "disappeared", "appear", "appeared", "vanish", "vanished", "realize",
    "realized", "decide", "decided", "try", "tried", "fail", "failed",
    "succeed", "succeeded", "save", "saved", "kill", "killed", "die", "died",
    "survive", "survived", "panic", "panicked", "rush", "rushed",
    "said", "told", "asked", "replied", "answered", "spoke",
}


def clean_text(text: str) -> str:
    """Clean input text by normalizing whitespace and removing special characters."""
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)  # collapse multiple spaces
    text = re.sub(r'[^\w\s.,!?;:\'"()\-\u2013\u2014]', '', text)  # keep common punctuation
    return text


def _segment_sentences_regex(text: str) -> list[str]:
    """Fallback sentence segmentation using regex (when spaCy is unavailable)."""
    # Split on sentence-ending punctuation followed by space + capital letter or end of string
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def segment_sentences(text: str) -> list[str]:
    """Split text into sentences. Uses spaCy if available, regex fallback otherwise."""
    cleaned = clean_text(text)

    if _SPACY_AVAILABLE and _nlp is not None:
        doc = _nlp(cleaned)
        sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
        return sentences
    else:
        return _segment_sentences_regex(cleaned)


def extract_action_verbs(text: str) -> list[str]:
    """Extract action verbs from text for pacing analysis."""
    if _SPACY_AVAILABLE and _nlp is not None:
        doc = _nlp(text)
        state_verbs = {"be", "is", "am", "are", "was", "were", "been", "being",
                       "have", "has", "had", "do", "does", "did",
                       "will", "would", "shall", "should", "may", "might",
                       "can", "could", "must"}
        action_verbs = []
        for token in doc:
            if token.pos_ == "VERB" and token.lemma_.lower() not in state_verbs:
                action_verbs.append(token.text.lower())
        return action_verbs
    else:
        # Fallback: match words against known action verb list
        words = text.lower().split()
        return [w.strip(".,!?;:'\"") for w in words if w.strip(".,!?;:'\"") in ACTION_VERB_LIST]


def detect_dialogue(text: str) -> list[str]:
    """Detect dialogue segments in text (text within quotes)."""
    dialogue_patterns = re.findall(r'["\u201c](.*?)["\u201d]', text)
    dialogue_patterns += re.findall(r"['\u2018](.*?)['\u2019]", text)
    return [d.strip() for d in dialogue_patterns if d.strip()]


def get_word_count(text: str) -> int:
    """Get word count of text."""
    return len(text.split())


def process_episode(text: str) -> dict:
    """
    Full text processing pipeline for an episode.
    Returns structured linguistic data for downstream analysis.
    """
    cleaned = clean_text(text)
    sentences = segment_sentences(cleaned)
    action_verbs = extract_action_verbs(cleaned)
    dialogues = detect_dialogue(cleaned)

    return {
        "cleaned_text": cleaned,
        "sentences": sentences,
        "sentence_count": len(sentences),
        "word_count": get_word_count(cleaned),
        "action_verbs": action_verbs,
        "action_verb_count": len(action_verbs),
        "dialogues": dialogues,
        "dialogue_count": len(dialogues),
        "avg_sentence_length": (
            sum(get_word_count(s) for s in sentences) / len(sentences)
            if sentences else 0
        ),
        "spacy_available": _SPACY_AVAILABLE,
    }
