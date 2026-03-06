"""
Feature Extractor V2 - Improved with Semantic Analysis
Integrates semantic similarity, emotional arc analysis, and narrative structure.
"""

from .text_processor import process_episode
from .emotion_model import classify_sentences
from .semantic_analyzer import get_semantic_analyzer
from .emotional_arc_analyzer import analyze_emotional_arc
from .narrative_structure_analyzer import analyze_narrative_structure
from .dropoff_predictor import predict_dropoff_zones

def _count_syllables(word: str) -> int:
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count

def calculate_flesch_reading_ease(text: str, total_words: int, total_sentences: int) -> float:
    if total_words == 0 or total_sentences == 0:
        return 100.0
    
    words = text.split()
    total_syllables = sum(_count_syllables(w) for w in words)
    
    score = 206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (total_syllables / total_words)
    return round(max(0.0, min(score, 100.0)), 2)

def detect_repetition(sentences: list) -> int:
    """Detects consecutive sentences starting with common LLM transition words or structurally identical phrases."""
    repetition_count = 0
    llm_transitions = {"moreover", "additionally", "furthermore", "in conclusion", "ultimately", "importantly"}
    
    for i in range(1, len(sentences)):
        prev_words = sentences[i-1].lower().split()
        curr_words = sentences[i].lower().split()
        
        if not prev_words or not curr_words:
            continue
            
        # Check LLM transition words
        clean_first_word = curr_words[0].strip(".,!?:;")
        if clean_first_word in llm_transitions:
            repetition_count += 1
            
        # Check 3-word exact match openings
        if len(prev_words) >= 3 and len(curr_words) >= 3:
            if prev_words[:3] == curr_words[:3]:
                repetition_count += 1
                
    return repetition_count


def extract_all_features_v2(text: str, hook: str = None, cliffhanger: str = None) -> dict:
    """
    Enhanced feature extraction with semantic analysis.
    
    Args:
        text: Raw episode story text
        hook: Optional episode hook (if provided, used instead of extracting from text)
        cliffhanger: Optional episode cliffhanger (if provided, used instead of extracting from text)
        
    Returns:
        {
            "semantic_features": {
                "hook_strength": float,
                "conflict_score": float,
                "cliffhanger_score": float,
                ...
            },
            "emotional_arc": {
                "timeline": list,
                "emotion_variance": float,
                "emotion_peak": float,
                ...
            },
            "narrative_structure": {
                "hook_position_score": float,
                "conflict_density": float,
                ...
            },
            "dropoff_prediction": {
                "segments": list,
                "high_risk_segments": list,
                ...
            },
            "sentence_emotions": list,
            "processed_text": dict
        }
    """
    # Step 1: Process text
    processed = process_episode(text)
    sentences = processed["sentences"]
    
    if not sentences:
        return _empty_result()
    
    # Step 2: Emotion classification
    sentence_emotions = classify_sentences(sentences)
    
    # Step 3: Semantic analysis
    semantic_analyzer = get_semantic_analyzer()
    
    # If hook is provided, analyze it separately; otherwise extract from text
    if hook:
        hook_sentences = [s.strip() for s in hook.split('.') if s.strip()]
        hook_result = semantic_analyzer.compute_semantic_hook_strength(hook_sentences)
    else:
        hook_result = semantic_analyzer.compute_semantic_hook_strength(sentences)
    
    conflict_result = semantic_analyzer.compute_semantic_conflict_score(sentences)
    
    # If cliffhanger is provided, analyze it separately; otherwise extract from text
    if cliffhanger:
        cliff_sentences = [s.strip() for s in cliffhanger.split('.') if s.strip()]
        cliffhanger_result = semantic_analyzer.compute_semantic_cliffhanger(cliff_sentences)
    else:
        cliffhanger_result = semantic_analyzer.compute_semantic_cliffhanger(sentences)
    
    semantic_features = {
        "hook_strength": hook_result["score"],
        "hook_reason": hook_result["reason"],
        "conflict_score": conflict_result["score"],
        "conflict_reason": conflict_result["reason"],
        "conflict_density": conflict_result["conflict_density"],
        "cliffhanger_score": cliffhanger_result["score"],
        "cliffhanger_reason": cliffhanger_result["reason"],
    }
    
    # Step 4: Emotional arc analysis
    emotional_arc = analyze_emotional_arc(sentence_emotions)
    
    # Step 5: Narrative structure analysis
    narrative_structure = analyze_narrative_structure(
        sentences,
        sentence_emotions,
        semantic_features
    )
    
    # Step 6: Linguistic Bias Checks (Readability & Repetition)
    reading_ease = calculate_flesch_reading_ease(
        processed["cleaned_text"], 
        processed["word_count"], 
        processed["sentence_count"]
    )
    repetition_count = detect_repetition(sentences)
    
    # Step 7: Dropoff prediction
    dropoff_prediction = predict_dropoff_zones(
        sentences,
        sentence_emotions,
        emotional_arc,
        semantic_features
    )
    
    return {
        "semantic_features": semantic_features,
        "emotional_arc": emotional_arc,
        "narrative_structure": narrative_structure,
        "dropoff_prediction": dropoff_prediction,
        "linguistic_bias": {
            "reading_ease": reading_ease,
            "repetition_count": repetition_count
        },
        "sentence_emotions": sentence_emotions,
        "processed_text": processed,
    }


def _empty_result() -> dict:
    """Return empty result for invalid input"""
    return {
        "semantic_features": {
            "hook_strength": 0.0,
            "hook_reason": "No content",
            "conflict_score": 0.0,
            "conflict_reason": "No content",
            "conflict_density": 0.0,
            "cliffhanger_score": 0.0,
            "cliffhanger_reason": "No content",
        },
        "emotional_arc": {
            "timeline": [],
            "emotion_variance": 0.0,
            "emotion_peak": 0.0,
            "emotion_shift_frequency": 0.0,
            "climax_position": 0.0,
            "emotional_drop_segments": [],
            "arc_shape": "flat",
            "reason": "No content",
        },
        "narrative_structure": {
            "hook_position_score": 0.0,
            "conflict_density": 0.0,
            "twist_position_score": 0.0,
            "cliffhanger_strength": 0.0,
            "resolution_absence_score": 0.0,
            "structure_quality": "POOR",
            "reason": "No content"
        },
        "dropoff_prediction": {
            "segments": [],
            "high_risk_segments": [],
            "overall_dropoff_risk": 1.0,
            "reason": "No content"
        },
        "linguistic_bias": {
            "reading_ease": 100.0,
            "repetition_count": 0
        },
        "sentence_emotions": [],
        "processed_text": {},
    }
