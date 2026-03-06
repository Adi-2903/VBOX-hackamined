"""
Keyword Detector V2 - Hybrid Approach
Combines exact keyword matching with semantic similarity for better coverage.
"""

from typing import Dict, List, Set
import re
import numpy as np


# Base keywords for exact matching (category-specific)
BASE_KEYWORDS = {
    "finance": {
        "hook": ["money", "rich", "broke", "debt", "salary", "income", "savings", "investment"],
        "conflict": ["debt", "broke", "struggle", "crisis", "loss", "bankruptcy", "failed"],
        "resolution": ["saved", "earned", "profit", "success", "freedom", "wealthy", "secure"]
    },
    "career": {
        "hook": ["job", "career", "work", "boss", "promotion", "fired", "quit"],
        "conflict": ["fired", "quit", "struggle", "stress", "overworked", "burnout", "toxic"],
        "resolution": ["promoted", "success", "achievement", "growth", "new job", "better"]
    },
    "health": {
        "hook": ["weight", "fitness", "health", "sick", "pain", "disease", "diagnosis"],
        "conflict": ["pain", "sick", "struggle", "failed", "relapse", "worse", "emergency"],
        "resolution": ["healed", "recovered", "healthy", "fit", "strong", "better", "cured"]
    },
    "relationships": {
        "hook": ["love", "breakup", "marriage", "divorce", "cheating", "betrayal", "crush"],
        "conflict": ["fight", "breakup", "cheating", "betrayal", "hurt", "alone", "toxic"],
        "resolution": ["together", "married", "happy", "love", "reconciled", "healed"]
    },
    "general": {
        "hook": ["shocking", "unexpected", "secret", "discovered", "revealed", "mystery"],
        "conflict": ["problem", "crisis", "danger", "struggle", "fight", "wrong", "failed"],
        "resolution": ["solved", "success", "victory", "achieved", "overcome", "won"]
    }
}


# Additional semantic keyword groups (for fuzzy matching)
SEMANTIC_KEYWORD_GROUPS = {
    "finance": {
        "money_terms": ["money", "cash", "funds", "capital", "wealth", "income", "salary", "wage", "earnings", "revenue"],
        "investment_terms": ["invest", "stock", "crypto", "bitcoin", "ethereum", "trading", "portfolio", "asset", "shares", "equity"],
        "debt_terms": ["debt", "loan", "credit", "mortgage", "emi", "interest", "payment", "liability", "owing", "borrowed"],
        "saving_terms": ["save", "saving", "budget", "frugal", "thrift", "economize", "nest egg"],
        "advanced_terms": ["compound interest", "diversification", "passive income", "financial independence", "FIRE", 
                          "index fund", "dividend", "net worth", "cash flow", "leverage", "liquidity", "ROI"]
    },
    "career": {
        "work_terms": ["work", "job", "career", "employment", "position", "role", "occupation", "profession"],
        "workplace_terms": ["office", "workplace", "company", "organization", "firm", "corporation", "employer"],
        "job_change_terms": ["quit", "resign", "leave", "fired", "laid off", "terminated", "dismissed", "let go"],
        "growth_terms": ["promotion", "raise", "advancement", "growth", "development", "progression", "upward mobility"],
        "advanced_terms": ["career trajectory", "professional development", "upskilling", "skill gap", "career pivot",
                          "networking", "personal brand", "thought leader", "resume", "recruiter", "headhunter"]
    },
    "health": {
        "fitness_terms": ["fit", "fitness", "exercise", "workout", "train", "gym", "athletic", "active"],
        "diet_terms": ["diet", "nutrition", "food", "meal", "eating", "calories", "macros", "protein"],
        "wellness_terms": ["health", "wellness", "wellbeing", "mental health", "therapy", "mindfulness", "self-care"],
        "body_terms": ["weight", "body", "muscle", "fat", "strength", "endurance", "physique", "build"],
        "advanced_terms": ["caloric deficit", "progressive overload", "body composition", "metabolic rate",
                          "muscle mass", "body fat percentage", "recovery", "rest day", "meal prep", "tracking"]
    },
    "productivity": {
        "time_terms": ["time", "schedule", "routine", "habit", "daily", "morning", "evening"],
        "focus_terms": ["focus", "concentration", "attention", "distraction", "flow", "deep work"],
        "system_terms": ["system", "method", "technique", "strategy", "approach", "framework"],
        "tool_terms": ["app", "tool", "software", "platform", "productivity", "efficiency"],
        "advanced_terms": ["time blocking", "pomodoro", "batch processing", "context switching", "priority matrix"]
    },
    "entrepreneurship": {
        "startup_terms": ["startup", "business", "venture", "company", "enterprise", "founder", "entrepreneur"],
        "funding_terms": ["funding", "investment", "investor", "capital", "seed", "series A", "angel", "VC"],
        "growth_terms": ["growth", "scale", "traction", "revenue", "profit", "customer", "user"],
        "failure_terms": ["fail", "failure", "pivot", "shutdown", "bankruptcy", "loss"],
        "advanced_terms": ["product-market fit", "customer acquisition cost", "lifetime value", "churn rate",
                          "runway", "burn rate", "unit economics", "go-to-market", "MVP", "iterate", "beta testing"]
    },
    "self_improvement": {
        "habit_terms": ["habit", "routine", "practice", "discipline", "consistency", "commitment"],
        "mindset_terms": ["mindset", "belief", "attitude", "perspective", "outlook", "mentality"],
        "growth_terms": ["growth", "improvement", "development", "progress", "evolution", "transformation"],
        "identity_terms": ["identity", "self", "character", "personality", "values", "purpose"],
        "advanced_terms": ["growth mindset", "fixed mindset", "self-awareness", "emotional intelligence", "limiting beliefs"]
    },
    "lifestyle": {
        "daily_terms": ["daily", "everyday", "routine", "life", "living", "lifestyle"],
        "social_terms": ["friend", "family", "relationship", "social", "community", "connection"],
        "balance_terms": ["balance", "harmony", "peace", "calm", "stress", "pressure"],
        "enjoyment_terms": ["enjoy", "fun", "happiness", "joy", "pleasure", "satisfaction"]
    },
    "technology": {
        "tech_terms": ["tech", "technology", "digital", "software", "hardware", "device"],
        "ai_terms": ["AI", "artificial intelligence", "machine learning", "algorithm", "automation"],
        "internet_terms": ["internet", "online", "web", "website", "app", "platform"],
        "advanced_terms": ["API", "cloud computing", "blockchain", "cybersecurity", "data privacy"]
    },
    "education": {
        "learning_terms": ["learn", "study", "education", "knowledge", "skill", "training"],
        "academic_terms": ["school", "college", "university", "course", "class", "degree"],
        "exam_terms": ["exam", "test", "quiz", "assessment", "grade", "score"],
        "advanced_terms": ["critical thinking", "problem solving", "active learning", "spaced repetition"]
    },
    "history_science_culture": {
        "history_terms": ["history", "historical", "ancient", "past", "civilization", "era"],
        "science_terms": ["science", "scientific", "research", "study", "experiment", "discovery"],
        "culture_terms": ["culture", "cultural", "tradition", "heritage", "society", "custom"],
        "mystery_terms": ["mystery", "secret", "hidden", "unknown", "forbidden", "lost"]
    }
}


class KeywordDetectorV2:
    """Enhanced keyword detector with semantic matching"""
    
    def __init__(self, use_semantic_matching: bool = True):
        self.base_keywords = BASE_KEYWORDS
        self.semantic_groups = SEMANTIC_KEYWORD_GROUPS
        self.use_semantic = use_semantic_matching
        self.categories = list(BASE_KEYWORDS.keys())
        
        # Compile regex patterns for faster matching
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Pre-compile regex patterns for all keywords"""
        self.patterns = {}
        
        for category, phases in self.base_keywords.items():
            self.patterns[category] = {}
            for phase, keywords in phases.items():
                # Create word boundary patterns to avoid partial matches
                patterns = []
                for kw in keywords:
                    # Escape special regex characters
                    escaped = re.escape(kw)
                    # Add word boundaries for single words, flexible for phrases
                    if ' ' in kw:
                        pattern = escaped
                    else:
                        pattern = r'\b' + escaped + r'\b'
                    patterns.append(pattern)
                
                # Combine all patterns for this phase
                combined = '|'.join(patterns)
                self.patterns[category][phase] = re.compile(combined, re.IGNORECASE)
    
    def detect_category(self, text: str) -> str:
        """
        Auto-detect content category based on keyword presence.
        Uses both exact matching and semantic groups.
        
        Returns:
            Category name (e.g., "finance", "career") or "general"
        """
        text_lower = text.lower()
        category_scores = {}
        
        # Score based on exact keyword matches
        for category, phases in self.base_keywords.items():
            score = 0
            for phase, keywords in phases.items():
                # Use compiled regex for faster matching
                if category in self.patterns and phase in self.patterns[category]:
                    matches = self.patterns[category][phase].findall(text_lower)
                    score += len(matches)
            category_scores[category] = score
        
        # Boost scores with semantic group matches
        if self.use_semantic:
            for category, groups in self.semantic_groups.items():
                if category not in category_scores:
                    category_scores[category] = 0
                
                for group_name, terms in groups.items():
                    for term in terms:
                        if term in text_lower:
                            category_scores[category] += 0.5  # Half weight for semantic matches
        
        if not category_scores or max(category_scores.values()) == 0:
            return "general"
        
        return max(category_scores, key=category_scores.get)
    
    def detect_keywords(
        self,
        text: str,
        category: str,
        phase: str
    ) -> Dict[str, any]:
        """
        Detect keywords in text for a specific category and phase.
        Enhanced with regex matching and semantic groups.
        
        Args:
            text: Text to analyze
            category: Content category (e.g., "finance", "career")
            phase: "hook", "conflict", or "resolution"
            
        Returns:
            {
                "count": int,
                "density": float (0-1),
                "keywords_found": list,
                "boost_factor": float (1.0-1.3),
                "semantic_matches": list (if enabled)
            }
        """
        if category not in self.base_keywords:
            category = "general"
        
        if category == "general" or phase not in self.base_keywords.get(category, {}):
            return {
                "count": 0,
                "density": 0.0,
                "keywords_found": [],
                "boost_factor": 1.0,
                "semantic_matches": []
            }
        
        text_lower = text.lower()
        
        # Find exact keyword matches using regex
        found = []
        if category in self.patterns and phase in self.patterns[category]:
            matches = self.patterns[category][phase].findall(text_lower)
            found = list(set(matches))  # Remove duplicates
        
        count = len(found)
        
        # Find semantic matches
        semantic_matches = []
        if self.use_semantic and category in self.semantic_groups:
            for group_name, terms in self.semantic_groups[category].items():
                for term in terms:
                    if term in text_lower and term not in found:
                        semantic_matches.append(term)
        
        # Total matches (exact + semantic)
        total_matches = count + len(semantic_matches)
        
        # Compute density (normalize by expected max)
        max_expected = 3  # Expect up to 3 keywords
        density = min(total_matches / max_expected, 1.0)
        
        # Compute boost factor (10-30% boost based on density)
        boost_factor = 1.0 + (0.3 * density)
        
        return {
            "count": count,
            "density": round(density, 3),
            "keywords_found": found,
            "boost_factor": round(boost_factor, 3),
            "semantic_matches": semantic_matches
        }
    
    def analyze_text(self, text: str, category: str = None) -> Dict:
        """
        Comprehensive keyword analysis of text.
        
        Args:
            text: Text to analyze
            category: Optional category (auto-detected if None)
            
        Returns:
            {
                "category": str,
                "hook": {...},
                "conflict": {...},
                "resolution": {...},
                "overall_keyword_strength": float,
                "total_keywords_found": int
            }
        """
        # Auto-detect category if not provided
        if category is None:
            category = self.detect_category(text)
        
        # Analyze each phase
        hook = self.detect_keywords(text, category, "hook")
        conflict = self.detect_keywords(text, category, "conflict")
        resolution = self.detect_keywords(text, category, "resolution")
        
        # Compute overall keyword strength
        overall_strength = (
            0.4 * hook["density"] +
            0.4 * conflict["density"] +
            0.2 * resolution["density"]
        )
        
        # Total unique keywords found
        all_keywords = set(hook["keywords_found"] + conflict["keywords_found"] + resolution["keywords_found"])
        all_semantic = set(hook.get("semantic_matches", []) + conflict.get("semantic_matches", []) + resolution.get("semantic_matches", []))
        total_found = len(all_keywords) + len(all_semantic)
        
        return {
            "category": category,
            "hook": hook,
            "conflict": conflict,
            "resolution": resolution,
            "overall_keyword_strength": round(overall_strength, 3),
            "total_keywords_found": total_found
        }
    
    def get_recommendations(self, analysis: Dict) -> List[str]:
        """
        Generate recommendations based on keyword analysis.
        
        Args:
            analysis: Output from analyze_text()
            
        Returns:
            List of actionable recommendations
        """
        recommendations = []
        category = analysis["category"]
        
        # Hook recommendations
        if analysis["hook"]["density"] < 0.3:
            hook_keywords = self.base_keywords.get(category, {}).get('hook', [])
            recommendations.append(
                f"Add stronger hook keywords for {category} content. "
                f"Try: {', '.join(hook_keywords[:3])}"
            )
        
        # Conflict recommendations
        if analysis["conflict"]["density"] < 0.3:
            conflict_keywords = self.base_keywords.get(category, {}).get('conflict', [])
            recommendations.append(
                f"Increase conflict tension with keywords like: "
                f"{', '.join(conflict_keywords[:3])}"
            )
        
        # Resolution recommendations (for cliffhangers, should be LOW)
        if analysis["resolution"]["density"] > 0.5:
            recommendations.append(
                "Too many resolution keywords - reduces cliffhanger strength. "
                "Leave some tension unresolved."
            )
        
        # Overall keyword density
        if analysis["total_keywords_found"] < 3:
            recommendations.append(
                f"Low keyword density ({analysis['total_keywords_found']} keywords found). "
                f"Add more category-specific terms to improve discoverability."
            )
        
        return recommendations


# Global instance
_detector_v2 = None

def get_keyword_detector_v2(use_semantic: bool = True) -> KeywordDetectorV2:
    """Get or create global keyword detector V2 instance"""
    global _detector_v2
    if _detector_v2 is None:
        _detector_v2 = KeywordDetectorV2(use_semantic_matching=use_semantic)
    return _detector_v2


# Alias for backward compatibility
get_keyword_detector = get_keyword_detector_v2


def detect_category_v2(text: str) -> str:
    """Quick function to detect category with V2"""
    detector = get_keyword_detector_v2()
    return detector.detect_category(text)



def analyze_keywords_v2(text: str, category: str = None) -> Dict:
    """Quick function to analyze keywords with V2"""
    detector = get_keyword_detector_v2()
    return detector.analyze_text(text, category)
