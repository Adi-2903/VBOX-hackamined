"""
Emotional Arc Analyzer - Full Emotional Timeline Analysis
Builds a complete emotional timeline instead of just computing variance.
"""

import numpy as np
from typing import List, Dict


class EmotionalArcAnalyzer:
    """Analyzes the emotional progression throughout a story"""
    
    # Emotion intensity mapping
    EMOTION_INTENSITY = {
        "neutral": 0.0,
        "joy": 0.6,
        "surprise": 0.7,
        "sadness": 0.5,
        "anger": 0.8,
        "fear": 0.9,
        "disgust": 0.6,
    }
    
    def analyze_emotional_arc(self, sentence_emotions: List[Dict]) -> Dict:
        """
        Build full emotional timeline and extract arc features.
        
        Args:
            sentence_emotions: List of emotion classifications per sentence
            
        Returns:
            {
                "timeline": list of intensity scores,
                "emotion_variance": float,
                "emotion_peak": float,
                "emotion_shift_frequency": float,
                "climax_position": float (0-1),
                "emotional_drop_segments": list of segment indices,
                "arc_shape": str (rising/falling/flat/dynamic),
                "reason": str
            }
        """
        if not sentence_emotions:
            return self._empty_result()
        
        # Build intensity timeline
        timeline = []
        emotion_labels = []
        
        for sent_emotion in sentence_emotions:
            emotion = sent_emotion["dominant_emotion"]
            score = sent_emotion["dominant_score"]
            
            # Intensity = base intensity * confidence score
            base_intensity = self.EMOTION_INTENSITY.get(emotion, 0.0)
            intensity = base_intensity * score
            
            timeline.append(intensity)
            emotion_labels.append(emotion)
        
        timeline = np.array(timeline)
        
        # Extract features
        emotion_variance = float(np.var(timeline))
        emotion_peak = float(np.max(timeline))
        
        # Emotion shift frequency (transitions between different emotions)
        shifts = sum(1 for i in range(1, len(emotion_labels)) 
                    if emotion_labels[i] != emotion_labels[i-1])
        emotion_shift_frequency = shifts / max(len(emotion_labels) - 1, 1)
        
        # Climax position (where peak intensity occurs)
        peak_idx = int(np.argmax(timeline))
        climax_position = peak_idx / max(len(timeline) - 1, 1)
        
        # Emotional drop segments (segments with low intensity)
        emotional_drop_segments = self._find_drop_segments(timeline)
        
        # Arc shape classification
        arc_shape = self._classify_arc_shape(timeline)
        
        # Build 1-10 arc score with improved short-text handling
        # For very short texts (<=3 sentences), variance is often 0. So we weight peak heavily.
        if len(timeline) <= 3:
            # For short texts, rely more on peak intensity and keyword presence
            keyword_boost = 0.0
            
            # Try to get keyword analysis if available
            try:
                from .keyword_detector import get_keyword_detector
                # Reconstruct approximate text from emotion labels for keyword search
                pseudo_text = " ".join(emotion_labels)
                kd = get_keyword_detector()
                kw_analysis = kd.analyze_text(pseudo_text)
                keyword_boost = kw_analysis.get("overall_keyword_strength", 0.0) * 2.0
            except:
                pass
            
            # If emotion model failed (peak < 0.1), boost based on keywords
            if emotion_peak < 0.1 and keyword_boost > 0.1:
                emotion_peak = 0.4 + keyword_boost
                    
            raw_score = (emotion_peak * 7.0) + (emotion_variance * 3.0) + keyword_boost
        else:
            # For longer texts, balance peak and variance
            raw_score = (emotion_peak * 5.0) + (min(emotion_variance, 0.15) * 40.0)
            
        arc_score = round(max(1.0, min(10.0, raw_score + 1.0)), 1)

        # Build reason
        reason = self._build_arc_reason(
            emotion_variance, emotion_peak, emotion_shift_frequency,
            climax_position, arc_shape, emotion_labels
        )
        
        return {
            "timeline": [round(float(x), 3) for x in timeline],
            "emotion_variance": round(emotion_variance, 4),
            "emotion_peak": round(emotion_peak, 3),
            "emotion_shift_frequency": round(emotion_shift_frequency, 3),
            "climax_position": round(climax_position, 3),
            "emotional_drop_segments": emotional_drop_segments,
            "arc_shape": arc_shape,
            "arc_score": arc_score,
            "reason": reason,
        }
    
    def _find_drop_segments(self, timeline: np.ndarray, threshold: float = 0.3) -> List[int]:
        """Find segments where emotional intensity drops below threshold"""
        # Divide into 4 segments
        segment_size = len(timeline) // 4
        if segment_size == 0:
            return []
        
        drop_segments = []
        for i in range(4):
            start = i * segment_size
            end = start + segment_size if i < 3 else len(timeline)
            segment = timeline[start:end]
            
            if len(segment) > 0 and np.mean(segment) < threshold:
                drop_segments.append(i)
        
        return drop_segments
    
    def _classify_arc_shape(self, timeline: np.ndarray) -> str:
        """Classify the overall shape of the emotional arc"""
        if len(timeline) < 3:
            return "flat"
        
        # Divide into thirds
        third = len(timeline) // 3
        first_third = np.mean(timeline[:third])
        middle_third = np.mean(timeline[third:2*third])
        last_third = np.mean(timeline[2*third:])
        
        # Check variance
        variance = np.var(timeline)
        
        if variance < 0.02:
            return "flat"
        elif last_third > first_third * 1.3:
            return "rising"
        elif last_third < first_third * 0.7:
            return "falling"
        else:
            return "dynamic"
    
    def _build_arc_reason(
        self, variance: float, peak: float, shift_freq: float,
        climax_pos: float, arc_shape: str, emotion_labels: List[str]
    ) -> str:
        """Build human-readable explanation of emotional arc"""
        reasons = []
        
        # Arc shape
        if arc_shape == "rising":
            reasons.append("Rising emotional arc - builds to climax")
        elif arc_shape == "falling":
            reasons.append("Falling emotional arc - starts strong, fades")
        elif arc_shape == "dynamic":
            reasons.append("Dynamic emotional arc - multiple peaks and valleys")
        else:
            reasons.append("Flat emotional arc - limited emotional variation")
        
        # Peak intensity
        if peak > 0.7:
            reasons.append(f"Strong emotional peak (intensity: {peak:.2f})")
        elif peak > 0.4:
            reasons.append(f"Moderate emotional peak (intensity: {peak:.2f})")
        else:
            reasons.append(f"Weak emotional peak (intensity: {peak:.2f})")
        
        # Climax position
        if 0.6 <= climax_pos <= 0.8:
            reasons.append("Well-positioned climax (60-80% through story)")
        elif climax_pos < 0.3:
            reasons.append("Early climax - may lose momentum")
        elif climax_pos > 0.9:
            reasons.append("Late climax - builds slowly")
        
        # Emotion diversity
        unique_emotions = len(set(emotion_labels))
        if unique_emotions >= 4:
            reasons.append(f"Rich emotional palette ({unique_emotions} emotions)")
        elif unique_emotions <= 2:
            reasons.append(f"Limited emotional range ({unique_emotions} emotions)")
        
        return "; ".join(reasons)
    
    def _empty_result(self) -> Dict:
        """Return empty result for invalid input"""
        return {
            "timeline": [],
            "emotion_variance": 0.0,
            "emotion_peak": 0.0,
            "emotion_shift_frequency": 0.0,
            "climax_position": 0.0,
            "emotional_drop_segments": [],
            "arc_shape": "flat",
            "arc_score": 0.0,
            "reason": "No emotional data available",
        }


# Global instance
_emotional_arc_analyzer = None

def get_emotional_arc_analyzer() -> EmotionalArcAnalyzer:
    """Get or create the global emotional arc analyzer instance"""
    global _emotional_arc_analyzer
    if _emotional_arc_analyzer is None:
        _emotional_arc_analyzer = EmotionalArcAnalyzer()
    return _emotional_arc_analyzer


def analyze_emotional_arc(sentence_emotions: List[Dict]) -> Dict:
    """Convenience function to analyze emotional arc"""
    analyzer = get_emotional_arc_analyzer()
    return analyzer.analyze_emotional_arc(sentence_emotions)
