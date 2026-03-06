"""
Narrative Structure Analyzer
Analyzes story structure for vertical video format (90-second episodes).

Structure:
- 0-10 seconds: Hook
- 10-50 seconds: Conflict development  
- 50-80 seconds: Twist/reveal
- 80-90 seconds: Cliffhanger
"""

import numpy as np
from typing import List, Dict


class NarrativeStructureAnalyzer:
    """Analyzes narrative structure and positioning"""
    
    def analyze_structure(
        self,
        sentences: List[str],
        sentence_emotions: List[Dict],
        semantic_features: Dict
    ) -> Dict:
        """
        Analyze narrative structure and compute structural scores.
        
        Args:
            sentences: List of sentences
            sentence_emotions: Emotion data per sentence
            semantic_features: Pre-computed semantic features
            
        Returns:
            {
                "hook_position_score": float,
                "conflict_density": float,
                "twist_position_score": float,
                "cliffhanger_strength": float,
                "resolution_absence_score": float,
                "structure_quality": str,
                "reason": str
            }
        """
        if not sentences:
            return self._empty_result()
        
        n_sentences = len(sentences)
        
        # Compute structural scores
        hook_position_score = self._compute_hook_position(
            semantic_features.get("hook_strength", 0.0),
            n_sentences
        )
        
        conflict_density = self._compute_conflict_density(
            sentence_emotions,
            n_sentences
        )
        
        twist_position_score = self._compute_twist_position(
            sentence_emotions,
            n_sentences
        )
        
        cliffhanger_strength = semantic_features.get("cliffhanger_score", 0.0)
        
        resolution_absence_score = self._compute_resolution_absence(
            sentence_emotions
        )
        
        # Overall structure quality
        structure_quality = self._assess_structure_quality(
            hook_position_score,
            conflict_density,
            twist_position_score,
            cliffhanger_strength,
            resolution_absence_score
        )
        
        # Build reason
        reason = self._build_structure_reason(
            hook_position_score,
            conflict_density,
            twist_position_score,
            cliffhanger_strength,
            resolution_absence_score,
            structure_quality
        )
        
        return {
            "hook_position_score": round(hook_position_score, 3),
            "conflict_density": round(conflict_density, 3),
            "twist_position_score": round(twist_position_score, 3),
            "cliffhanger_strength": round(cliffhanger_strength, 3),
            "resolution_absence_score": round(resolution_absence_score, 3),
            "structure_quality": structure_quality,
            "reason": reason
        }
    
    def _compute_hook_position(self, hook_strength: float, n_sentences: int) -> float:
        """
        Score hook positioning. Ideal: strong hook in first 10-15% of story.
        """
        # If hook is weak, position doesn't matter much
        if hook_strength < 0.3:
            return 0.3
        
        # Strong hook in early position = good
        # We assume hook is measured from first sentences, so just return strength
        return hook_strength
    
    def _compute_conflict_density(
        self,
        sentence_emotions: List[Dict],
        n_sentences: int
    ) -> float:
        """
        Compute conflict density in middle section (10-80% of story).
        High-tension emotions = conflict.
        """
        if n_sentences < 3:
            return 0.0
        
        # Middle section: 10% to 80%
        start_idx = max(1, int(n_sentences * 0.1))
        end_idx = max(start_idx + 1, int(n_sentences * 0.8))
        
        middle_emotions = sentence_emotions[start_idx:end_idx]
        
        if not middle_emotions:
            return 0.0
        
        # Count high-tension emotions
        tension_emotions = {"anger", "fear", "surprise"}
        tension_count = sum(
            1 for e in middle_emotions
            if e["dominant_emotion"] in tension_emotions and e["dominant_score"] > 0.5
        )
        
        density = tension_count / len(middle_emotions)
        return min(density * 2, 1.0)  # Scale up
    
    def _compute_twist_position(
        self,
        sentence_emotions: List[Dict],
        n_sentences: int
    ) -> float:
        """
        Score twist positioning. Ideal: emotional spike at 50-80% of story.
        """
        if n_sentences < 3:
            return 0.0
        
        # Find position of maximum emotional intensity
        intensities = []
        for e in sentence_emotions:
            emotion = e["dominant_emotion"]
            score = e["dominant_score"]
            
            # High-intensity emotions
            if emotion in {"fear", "anger", "surprise"}:
                intensities.append(score)
            else:
                intensities.append(score * 0.5)
        
        if not intensities:
            return 0.0
        
        peak_idx = np.argmax(intensities)
        peak_position = peak_idx / max(n_sentences - 1, 1)
        
        # Ideal position: 0.5 to 0.8
        if 0.5 <= peak_position <= 0.8:
            return 1.0
        elif 0.3 <= peak_position < 0.5:
            return 0.7
        elif 0.8 < peak_position <= 0.9:
            return 0.8
        else:
            return 0.4
    
    def _compute_resolution_absence(self, sentence_emotions: List[Dict]) -> float:
        """
        Score absence of resolution. Good vertical video avoids neat endings.
        High score = no resolution (good for retention).
        """
        if not sentence_emotions:
            return 0.0
        
        # Check last 2 sentences for "resolution" emotions (joy, neutral)
        last_emotions = sentence_emotions[-2:]
        
        resolution_emotions = {"joy", "neutral"}
        resolution_count = sum(
            1 for e in last_emotions
            if e["dominant_emotion"] in resolution_emotions and e["dominant_score"] > 0.6
        )
        
        # High resolution = bad for cliffhanger
        resolution_ratio = resolution_count / len(last_emotions)
        absence_score = 1.0 - resolution_ratio
        
        return absence_score
    
    def _assess_structure_quality(
        self,
        hook_pos: float,
        conflict_dens: float,
        twist_pos: float,
        cliff_str: float,
        res_abs: float
    ) -> str:
        """Assess overall structure quality"""
        avg_score = (hook_pos + conflict_dens + twist_pos + cliff_str + res_abs) / 5
        
        if avg_score >= 0.7:
            return "EXCELLENT"
        elif avg_score >= 0.5:
            return "GOOD"
        elif avg_score >= 0.35:
            return "FAIR"
        else:
            return "POOR"
    
    def _build_structure_reason(
        self,
        hook_pos: float,
        conflict_dens: float,
        twist_pos: float,
        cliff_str: float,
        res_abs: float,
        quality: str
    ) -> str:
        """Build explanation of structure analysis"""
        reasons = []
        
        # Hook
        if hook_pos >= 0.6:
            reasons.append("Strong opening hook")
        elif hook_pos < 0.4:
            reasons.append("Weak opening - needs stronger hook")
        
        # Conflict
        if conflict_dens >= 0.5:
            reasons.append("Good conflict density in middle section")
        elif conflict_dens < 0.3:
            reasons.append("Low conflict in middle - risk of boredom")
        
        # Twist
        if twist_pos >= 0.8:
            reasons.append("Well-positioned emotional peak")
        elif twist_pos < 0.5:
            reasons.append("Emotional peak poorly positioned")
        
        # Cliffhanger
        if cliff_str >= 0.6:
            reasons.append("Strong cliffhanger ending")
        elif cliff_str < 0.4:
            reasons.append("Weak cliffhanger - needs more tension")
        
        # Resolution
        if res_abs >= 0.7:
            reasons.append("Good - avoids neat resolution")
        elif res_abs < 0.4:
            reasons.append("Too much resolution - weakens cliffhanger")
        
        return f"{quality} structure: " + "; ".join(reasons)
    
    def _empty_result(self) -> Dict:
        """Return empty result for invalid input"""
        return {
            "hook_position_score": 0.0,
            "conflict_density": 0.0,
            "twist_position_score": 0.0,
            "cliffhanger_strength": 0.0,
            "resolution_absence_score": 0.0,
            "structure_quality": "POOR",
            "reason": "Insufficient data for structure analysis"
        }


# Global instance
_narrative_structure_analyzer = None

def get_narrative_structure_analyzer() -> NarrativeStructureAnalyzer:
    """Get or create the global narrative structure analyzer instance"""
    global _narrative_structure_analyzer
    if _narrative_structure_analyzer is None:
        _narrative_structure_analyzer = NarrativeStructureAnalyzer()
    return _narrative_structure_analyzer


def analyze_narrative_structure(
    sentences: List[str],
    sentence_emotions: List[Dict],
    semantic_features: Dict
) -> Dict:
    """Convenience function to analyze narrative structure"""
    analyzer = get_narrative_structure_analyzer()
    return analyzer.analyze_structure(sentences, sentence_emotions, semantic_features)
