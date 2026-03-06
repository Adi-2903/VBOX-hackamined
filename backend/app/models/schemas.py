"""
Pydantic models matching the EXACT ML Pipeline output from BACKEND_INTEGRATION_GUIDE.md
and the GenAI layer output from test_output.json.
"""
from pydantic import BaseModel, Field
from typing import Optional


# ──────────────────────────────────────────────
# REQUEST MODELS
# ──────────────────────────────────────────────

class DirectionSuggestion(BaseModel):
    direction_name: str
    category: str
    why_it_fits: str


class DirectionsResponse(BaseModel):
    suggested_directions: list[DirectionSuggestion]


class StoryPromptRequest(BaseModel):
    concept: str = Field(..., description="The raw story idea / prompt from the creator")
    num_episodes: int = Field(default=5, ge=2, le=8)
    genres: list[str] = Field(default=["Thriller"])
    audience: str = Field(default="Gen Z", description="Target audience")
    direction: str = Field(default="", description="Chosen narrative direction")


class AnalysisRequest(BaseModel):
    """Single episode analysis request matching the integration guide."""
    text: str = Field(..., description="Episode story content to analyze")
    category: str | None = Field(default=None, description="Content category: crime, romance, horror, thriller, drama, comedy")


# ──────────────────────────────────────────────
# GenAI OUTPUT (matches test_output.json)
# ──────────────────────────────────────────────

class GeneratedEpisode(BaseModel):
    episode_number: int
    title: str
    hook: str
    story: str
    cliffhanger: str
    text_overlays_suggestions: list[str] = []


class GeneratedSeries(BaseModel):
    category: str
    direction: str
    hook: str
    episodes: list[GeneratedEpisode]


# ──────────────────────────────────────────────
# ML ANALYSIS OUTPUT — matches BACKEND_INTEGRATION_GUIDE.md §Output Format
# ──────────────────────────────────────────────

# --- Features: Semantic ---
class SemanticFeatures(BaseModel):
    hook_strength: float
    conflict_score: float
    cliffhanger_score: float
    hook_reason: str = ""
    conflict_reason: str = ""
    cliffhanger_reason: str = ""


# --- Features: Emotional Arc ---
class EmotionalArc(BaseModel):
    emotion_variance: float
    emotion_peak: float
    climax_position: float
    arc_shape: str  # RISING_ACTION / FALLING / DYNAMIC / FLAT
    reason: str = ""


# --- Features: Narrative Structure ---
class NarrativeStructure(BaseModel):
    structure_quality: str  # EXCELLENT / GOOD / FAIR / POOR
    hook_position_score: float
    conflict_density: float
    twist_position_score: float
    reason: str = ""


# --- Features: Dropoff Prediction ---
class DropoffSegment(BaseModel):
    label: str  # e.g. "Opening (0-10s)"
    dropoff_risk: float
    engagement_score: float


class DropoffPrediction(BaseModel):
    overall_dropoff_risk: float
    high_risk_segments: list[int] = []
    segments: list[DropoffSegment] = []
    reason: str = ""


# --- Features wrapper ---
class Features(BaseModel):
    semantic_features: SemanticFeatures
    emotional_arc: EmotionalArc
    narrative_structure: NarrativeStructure
    dropoff_prediction: DropoffPrediction


# --- Retention ---
class SegmentRisk(BaseModel):
    risk: float
    label: str  # LOW / MEDIUM / HIGH


class Recommendation(BaseModel):
    area: str
    priority: str  # CRITICAL / HIGH / MEDIUM / LOW
    suggestion: str


class Retention(BaseModel):
    risk_score: float
    risk_level: str  # LOW / MEDIUM / HIGH
    segment_risks: dict[str, SegmentRisk] = {}
    reason: str = ""
    recommendations: list[Recommendation] = []


# --- Cliffhanger ---
class CliffhangerComponents(BaseModel):
    surprise: float
    emotion_spike: float
    conflict_signal: float
    keyword_boost: float = 1.0


class Cliffhanger(BaseModel):
    cliffhanger_score: float = Field(ge=0, le=10)
    strength: str  # STRONG / MODERATE / WEAK
    components: CliffhangerComponents
    category: str = ""
    keywords_found: dict[str, list[str]] = {}
    reason: str = ""


# --- Summary ---
class AnalysisSummary(BaseModel):
    overall_score: float = Field(ge=0, le=100)
    engagement_level: str  # EXCELLENT / GOOD / FAIR / POOR
    key_strengths: list[str] = []
    key_weaknesses: list[str] = []


# ──────────────────────────────────────────────
# COMPLETE EPISODE ANALYSIS (the full response from ml_pipeline_v2)
# ──────────────────────────────────────────────

class EpisodeAnalysis(BaseModel):
    """Matches the exact output of analyze_episode_v2() from the integration guide."""
    category: str = ""
    features: Features
    retention: Retention
    cliffhanger: Cliffhanger
    summary: AnalysisSummary


# Wrapper to also include episode metadata when used in series context
class EpisodeAnalysisWithMeta(BaseModel):
    episode_number: int
    title: str
    analysis: EpisodeAnalysis


# ──────────────────────────────────────────────
# SERIES ANALYSIS
# ──────────────────────────────────────────────

class SeriesInsights(BaseModel):
    avg_overall_score: float
    trend: str  # improving / declining / stable
    consistency_score: float
    weakest_episode: int
    strongest_episode: int


class SeriesAnalysis(BaseModel):
    episodes: list[EpisodeAnalysisWithMeta]
    series_insights: SeriesInsights


# ──────────────────────────────────────────────
# PROJECT (MongoDB document)
# ──────────────────────────────────────────────

class ProjectCreate(BaseModel):
    title: str
    concept: str
    genres: list[str] = []
    generated_series: Optional[GeneratedSeries] = None
    analysis: Optional[SeriesAnalysis] = None


class ProjectResponse(BaseModel):
    id: str
    title: str
    concept: str
    genres: list[str] = []
    generated_series: Optional[GeneratedSeries] = None
    analysis: Optional[SeriesAnalysis] = None
    status: str = "draft"
    created_at: str = ""
    episode_count: int = 0
    overall_score: Optional[float] = None
