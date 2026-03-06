"""
Drop-off Zone Predictor
Predicts specific time segments where viewers are likely to drop off.
"""

import numpy as np
from typing import List, Dict, Tuple


class DropoffPredictor:
    """Predicts viewer drop-off zones in episodic content"""
    
    # Time segment definitions (in seconds for 90-second video)
    SEGMENTS = [
        (0, 15, "Hook"),
        (15, 30, "Setup"),
        (30, 60, "Development"),
        (60, 90, "Climax/Ending")
    ]
    
    def predict_dropoff_zones(
        self,
        sentences: List[str],
        sentence_emotions: List[Dict],
        emotional_arc: Dict,
        semantic_features: Dict
    ) -> Dict:
        """
        Predict drop-off zones by analyzing engagement per segment.
        
        Args:
            sentences: List of sentences
            sentence_emotions: Emotion data per sentence
            emotional_arc: Emotional arc analysis results
            semantic_features: Semantic feature scores
            
        Returns:
            {
                "segments": list of segment analyses,
                "high_risk_segments": list of segment indices,
                "overall_dropoff_risk": float (0-1),
                "reason": str
            }
        """
        if not sentences:
            return self._empty_result()
        
        n_sentences = len(sentences)
        
        # Divide sentences into segments
        segment_analyses = []
        high_risk_segments = []
        
        for idx, (start_sec, end_sec, label) in enumerate(self.SEGMENTS):
            # Map time to sentence indices (assume ~1 sentence per 6 seconds)
            start_idx = int((start_sec / 90) * n_sentences)
            end_idx = int((end_sec / 90) * n_sentences)
            end_idx = min(end_idx, n_sentences)
            
            if start_idx >= n_sentences:
                break
            
            segment_sentences = sentences[start_idx:end_idx]
            segment_emotions = sentence_emotions[start_idx:end_idx]
            
            # Analyze segment
            analysis = self._analyze_segment(
                idx, label, segment_sentences, segment_emotions,
                emotional_arc, semantic_features
            )
            
            segment_analyses.append(analysis)
            
            # Mark high-risk segments
            if analysis["dropoff_risk"] > 0.6:
                high_risk_segments.append(idx)
        
        # Overall dropoff risk
        if segment_analyses:
            overall_risk = np.mean([s["dropoff_risk"] for s in segment_analyses])
        else:
            overall_risk = 0.5
        
        # Build reason
        reason = self._build_dropoff_reason(segment_analyses, high_risk_segments)
        
        return {
            "segments": segment_analyses,
            "high_risk_segments": high_risk_segments,
            "overall_dropoff_risk": round(float(overall_risk), 3),
            "reason": reason
        }
    
    def _analyze_segment(
        self,
        idx: int,
        label: str,
        sentences: List[str],
        emotions: List[Dict],
        emotional_arc: Dict,
        semantic_features: Dict
    ) -> Dict:
        """Analyze a single time segment"""
        if not sentences or not emotions:
            return {
                "segment_index": idx,
                "label": label,
                "engagement_score": 0.0,
                "emotion_level": 0.0,
                "conflict_density": 0.0,
                "surprise_level": 0.0,
                "dropoff_risk": 1.0,
                "reason": "No content in segment"
            }
        
        # Compute engagement metrics
        engagement_score = self._compute_segment_engagement(emotions)
        emotion_level = self._compute_segment_emotion_level(emotions)
        conflict_density = self._compute_segment_conflict(emotions)
        surprise_level = self._compute_segment_surprise(emotions)
        
        # Segment-specific adjustments
        if idx == 0:  # Hook segment
            # Hook segment depends heavily on hook strength
            hook_strength = semantic_features.get("hook_strength", 0.0)
            engagement_score = (engagement_score + hook_strength) / 2
        elif idx == 3:  # Ending segment
            # Ending depends on cliffhanger
            cliff_strength = semantic_features.get("cliffhanger_score", 0.0)
            engagement_score = (engagement_score + cliff_strength) / 2
        
        # Compute dropoff risk (inverse of engagement)
        dropoff_risk = 1.0 - engagement_score
        
        # Build reason
        reason = self._build_segment_reason(
            label, engagement_score, emotion_level, conflict_density, surprise_level
        )
        
        return {
            "segment_index": idx,
            "label": label,
            "engagement_score": round(engagement_score, 3),
            "emotion_level": round(emotion_level, 3),
            "conflict_density": round(conflict_density, 3),
            "surprise_level": round(surprise_level, 3),
            "dropoff_risk": round(dropoff_risk, 3),
            "reason": reason
        }
    
    def _compute_segment_engagement(self, emotions: List[Dict]) -> float:
        """Compute overall engagement score for segment"""
        if not emotions:
            return 0.0
        
        # High-engagement emotions
        engaging_emotions = {"fear", "anger", "surprise", "joy"}
        
        engagement_scores = []
        for e in emotions:
            if e["dominant_emotion"] in engaging_emotions:
                engagement_scores.append(e["dominant_score"])
            else:
                engagement_scores.append(e["dominant_score"] * 0.3)
        
        return float(np.mean(engagement_scores))
    
    def _compute_segment_emotion_level(self, emotions: List[Dict]) -> float:
        """Compute average emotional intensity in segment"""
        if not emotions:
            return 0.0
        
        intensities = [e["dominant_score"] for e in emotions]
        return float(np.mean(intensities))
    
    def _compute_segment_conflict(self, emotions: List[Dict]) -> float:
        """Compute conflict density in segment"""
        if not emotions:
            return 0.0
        
        conflict_emotions = {"anger", "fear", "disgust"}
        conflict_count = sum(
            1 for e in emotions
            if e["dominant_emotion"] in conflict_emotions and e["dominant_score"] > 0.5
        )
        
        return conflict_count / len(emotions)
    
    def _compute_segment_surprise(self, emotions: List[Dict]) -> float:
        """Compute surprise level in segment"""
        if not emotions:
            return 0.0
        
        surprise_count = sum(
            1 for e in emotions
            if e["dominant_emotion"] == "surprise" and e["dominant_score"] > 0.5
        )
        
        return min(surprise_count / max(len(emotions), 1), 1.0)
    
    def _build_segment_reason(
        self,
        label: str,
        engagement: float,
        emotion: float,
        conflict: float,
        surprise: float
    ) -> str:
        """Build explanation for segment analysis"""
        if engagement >= 0.6:
            return f"{label}: High engagement - strong emotional content"
        elif engagement >= 0.4:
            return f"{label}: Moderate engagement - some emotional movement"
        else:
            issues = []
            if emotion < 0.3:
                issues.append("low emotional intensity")
            if conflict < 0.2:
                issues.append("minimal conflict")
            if surprise < 0.1:
                issues.append("no surprises")
            
            if issues:
                return f"{label}: Low engagement - {', '.join(issues)}"
            else:
                return f"{label}: Low engagement"
    
    def _build_dropoff_reason(
        self,
        segments: List[Dict],
        high_risk: List[int]
    ) -> str:
        """Build overall dropoff explanation"""
        if not high_risk:
            return "Good engagement across all segments"
        
        risk_labels = [segments[i]["label"] for i in high_risk if i < len(segments)]
        
        if len(high_risk) >= 3:
            return f"High drop-off risk in multiple segments: {', '.join(risk_labels)}"
        else:
            return f"Drop-off risk in: {', '.join(risk_labels)}"
    
    def _empty_result(self) -> Dict:
        """Return empty result for invalid input"""
        return {
            "segments": [],
            "high_risk_segments": [],
            "overall_dropoff_risk": 1.0,
            "reason": "No content to analyze"
        }


# Global instance
_dropoff_predictor = None

def get_dropoff_predictor() -> DropoffPredictor:
    """Get or create the global dropoff predictor instance"""
    global _dropoff_predictor
    if _dropoff_predictor is None:
        _dropoff_predictor = DropoffPredictor()
    return _dropoff_predictor


def predict_dropoff_zones(
    sentences: List[str],
    sentence_emotions: List[Dict],
    emotional_arc: Dict,
    semantic_features: Dict
) -> Dict:
    """Convenience function to predict dropoff zones"""
    predictor = get_dropoff_predictor()
    return predictor.predict_dropoff_zones(
        sentences, sentence_emotions, emotional_arc, semantic_features
    )
