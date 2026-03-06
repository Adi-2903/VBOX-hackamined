"""
Semantic Analyzer Module - Embedding-based Feature Detection
Replaces keyword-based detection with semantic similarity using embeddings.
"""

import numpy as np
from .embedding_model import get_embedding_model, compute_embeddings


# Concept prompts for semantic similarity
HOOK_CONCEPTS = [
    "a shocking revelation occurs",
    "something unexpected happens",
    "a mystery is introduced",
    "a surprising discovery is made",
    "danger suddenly appears",
    "a secret is revealed",
    "an impossible situation unfolds",
]

CONFLICT_CONCEPTS = [
    "two characters are in opposition",
    "a problem emerges",
    "danger or tension appears",
    "a challenge must be overcome",
    "someone faces an obstacle",
    "a threat is present",
]

SUSPENSE_CONCEPTS = [
    "uncertainty about what happens next",
    "tension builds",
    "something ominous is approaching",
    "the situation becomes dangerous",
]

CLIFFHANGER_CONCEPTS = [
    "the story ends with unresolved tension",
    "a question is left unanswered",
    "the outcome remains uncertain",
    "a new problem emerges at the end",
]


class SemanticAnalyzer:
    """Analyzes narrative features using semantic embeddings"""
    
    def __init__(self):
        self.model = get_embedding_model()
        self._concept_embeddings = {}
        self._initialize_concepts()
    
    def _initialize_concepts(self):
        """Pre-compute embeddings for all concept prompts"""
        self._concept_embeddings = {
            "hook": compute_embeddings(HOOK_CONCEPTS, self.model),
            "conflict": compute_embeddings(CONFLICT_CONCEPTS, self.model),
            "suspense": compute_embeddings(SUSPENSE_CONCEPTS, self.model),
            "cliffhanger": compute_embeddings(CLIFFHANGER_CONCEPTS, self.model),
        }
    
    def compute_semantic_hook_strength(self, sentences: list[str]) -> dict:
        """
        Compute hook strength using semantic similarity.
        Analyzes first 10-15% of story.
        
        Returns:
            {"score": float (0-1), "reason": str, "top_matches": list}
        """
        if not sentences:
            return {"score": 0.0, "reason": "No sentences found", "top_matches": []}
        
        # Take first 10-15% of sentences (min 1, max 3)
        hook_count = max(1, min(3, int(len(sentences) * 0.15)))
        hook_sentences = sentences[:hook_count]
        
        # Compute embeddings for hook sentences
        hook_embeddings = compute_embeddings(hook_sentences, self.model)
        concept_embeddings = self._concept_embeddings["hook"]
        
        # Compute cosine similarity between each sentence and each concept
        similarities = []
        for sent_emb in hook_embeddings:
            max_sim = 0.0
            for concept_emb in concept_embeddings:
                sim = self._cosine_similarity(sent_emb, concept_emb)
                max_sim = max(max_sim, sim)
            similarities.append(max_sim)
        
        # Score is the maximum similarity found, with boosting
        raw_score = float(max(similarities)) if similarities else 0.0
        
        # Apply power scaling to amplify differences (cosine similarity is often compressed)
        # This makes the scores more discriminative
        score = raw_score ** 0.7  # Boost scores (0.3 -> 0.44, 0.5 -> 0.63, 0.7 -> 0.79)
        score = round(min(max(score, 0.0), 1.0), 4)
        
        # Build reason with adjusted thresholds
        if score > 0.55:
            reason = "Strong semantic hook - opening strongly matches hook concepts"
        elif score > 0.35:
            reason = "Moderate hook - some hook elements detected"
        else:
            reason = "Weak hook - opening lacks strong hook signals"
        
        return {
            "score": score,
            "reason": reason,
            "top_matches": [round(s, 3) for s in similarities]
        }
    
    def compute_semantic_conflict_score(self, sentences: list[str]) -> dict:
        """
        Compute conflict score using semantic similarity.
        
        Returns:
            {"score": float (0-1), "reason": str, "conflict_density": float}
        """
        if not sentences:
            return {"score": 0.0, "reason": "No sentences found", "conflict_density": 0.0}
        
        # Compute embeddings for all sentences
        sent_embeddings = compute_embeddings(sentences, self.model)
        concept_embeddings = self._concept_embeddings["conflict"]
        
        # Compute max similarity for each sentence
        conflict_scores = []
        for sent_emb in sent_embeddings:
            max_sim = 0.0
            for concept_emb in concept_embeddings:
                sim = self._cosine_similarity(sent_emb, concept_emb)
                max_sim = max(max_sim, sim)
            conflict_scores.append(max_sim)
        
        # Conflict density: percentage of sentences with conflict > threshold
        threshold = 0.30  # Lowered from 0.4
        conflict_count = sum(1 for s in conflict_scores if s > threshold)
        conflict_density = conflict_count / len(sentences)
        
        # Overall score: average of top conflict scores with boosting
        top_scores = sorted(conflict_scores, reverse=True)[:max(1, len(sentences) // 3)]
        raw_score = float(np.mean(top_scores))
        
        # Apply power scaling to boost scores
        score = raw_score ** 0.75
        score = round(min(max(score, 0.0), 1.0), 4)
        
        # Build reason with adjusted thresholds
        if conflict_density > 0.4:
            reason = f"High conflict density - {conflict_count}/{len(sentences)} sentences show conflict"
        elif conflict_density > 0.2:
            reason = f"Moderate conflict - {conflict_count}/{len(sentences)} sentences show conflict"
        else:
            reason = f"Low conflict - only {conflict_count}/{len(sentences)} sentences show conflict"
        
        return {
            "score": score,
            "reason": reason,
            "conflict_density": round(conflict_density, 3)
        }
    
    def compute_semantic_cliffhanger(self, sentences: list[str]) -> dict:
        """
        Compute cliffhanger strength using semantic similarity.
        Analyzes last 10-15% of story.
        
        Returns:
            {"score": float (0-1), "reason": str}
        """
        if not sentences:
            return {"score": 0.0, "reason": "No sentences found"}
        
        # Take last 10-15% of sentences (min 1, max 3)
        cliff_count = max(1, min(3, int(len(sentences) * 0.15)))
        cliff_sentences = sentences[-cliff_count:]
        
        # Compute embeddings
        cliff_embeddings = compute_embeddings(cliff_sentences, self.model)
        concept_embeddings = self._concept_embeddings["cliffhanger"]
        
        # Compute similarities
        similarities = []
        for sent_emb in cliff_embeddings:
            max_sim = 0.0
            for concept_emb in concept_embeddings:
                sim = self._cosine_similarity(sent_emb, concept_emb)
                max_sim = max(max_sim, sim)
            similarities.append(max_sim)
        
        # Score is the maximum similarity with boosting
        raw_score = float(max(similarities)) if similarities else 0.0
        
        # Apply power scaling to boost scores
        score = raw_score ** 0.7
        score = round(min(max(score, 0.0), 1.0), 4)
        
        # Build reason with adjusted thresholds
        if score > 0.55:
            reason = "Strong cliffhanger - ending leaves clear unresolved tension"
        elif score > 0.35:
            reason = "Moderate cliffhanger - some tension in ending"
        else:
            reason = "Weak cliffhanger - ending lacks strong tension or questions"
        
        return {"score": score, "reason": reason}
    
    @staticmethod
    def _cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Compute cosine similarity between two vectors"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))


# Global instance
_semantic_analyzer = None

def get_semantic_analyzer() -> SemanticAnalyzer:
    """Get or create the global semantic analyzer instance"""
    global _semantic_analyzer
    if _semantic_analyzer is None:
        _semantic_analyzer = SemanticAnalyzer()
    return _semantic_analyzer
