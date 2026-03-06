"""
Engine routes — GenAI generation + ML analysis endpoints.
Returns dummy data that mirrors the real pipeline output (BACKEND_INTEGRATION_GUIDE.md).

Includes input validation, logging, and async support as recommended by the guide.
"""
import logging
import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.schemas import (
    StoryPromptRequest,
    AnalysisRequest,
    GeneratedSeries,
    EpisodeAnalysis,
    SeriesAnalysis,
    DirectionsResponse,
)
from app.dummy_data import generate_dummy_series, generate_dummy_directions, analyze_dummy_episode, analyze_dummy_series

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/engine", tags=["Engine"])

MAX_TEXT_LENGTH = 10_000


# ──────────────────────────────────────────────
# GenAI Generation
# ──────────────────────────────────────────────

@router.post("/directions", response_model=DirectionsResponse)
async def get_directions(req: dict):
    """
    Suggest 3 narrative directions for a concept.
    Currently returns dummy data — swap with GenAI's generate_directions() later.
    """
    concept = req.get("concept", "")
    if not concept.strip():
        raise HTTPException(status_code=400, detail="Concept must be a non-empty string")

    start = time.time()
    logger.info(f"Generating directions — concept length: {len(concept)}")
    data = generate_dummy_directions(concept)
    logger.info(f"Directions generated — {time.time() - start:.2f}s")
    return data


@router.post("/generate", response_model=GeneratedSeries)
async def generate_series(req: StoryPromptRequest):
    """
    Takes a story concept and returns a generated series of episodes.
    Currently returns dummy data — swap with GenAI layer later.
    """
    if not req.concept.strip():
        raise HTTPException(status_code=400, detail="Concept must be a non-empty string")

    start = time.time()
    logger.info(f"Generating series — concept length: {len(req.concept)}, episodes: {req.num_episodes}, audience: {req.audience}, direction: {req.direction}")

    data = generate_dummy_series(req.concept, req.num_episodes, req.direction, req.audience)

    logger.info(f"Generation complete — {time.time() - start:.2f}s")
    return data


# ──────────────────────────────────────────────
# ML Analysis (matches BACKEND_INTEGRATION_GUIDE.md)
# ──────────────────────────────────────────────

@router.post("/analyze", response_model=EpisodeAnalysis)
async def analyze_content(req: AnalysisRequest):
    """
    Analyze single episode content for retention prediction.
    Matches the exact API from BACKEND_INTEGRATION_GUIDE.md:
        POST /api/analyze  { text, category }
    Currently returns dummy data — swap with ml_pipeline_v2.analyze_episode_v2() later.
    """
    if not req.text or not isinstance(req.text, str):
        raise HTTPException(status_code=400, detail="Text must be a non-empty string")
    if len(req.text) > MAX_TEXT_LENGTH:
        raise HTTPException(status_code=400, detail=f"Text exceeds maximum length of {MAX_TEXT_LENGTH}")

    start = time.time()
    logger.info(f"Starting analysis — Category: {req.category}, Length: {len(req.text)}")

    result = analyze_dummy_episode(text=req.text, category=req.category)

    duration = time.time() - start
    logger.info(f"Analysis complete — Duration: {duration:.2f}s, Score: {result['summary']['overall_score']}")
    return result


class AnalyzeSeriesRequest(BaseModel):
    episodes: list[dict]
    category: str | None = None


@router.post("/analyze-series", response_model=SeriesAnalysis)
async def analyze_series(payload: AnalyzeSeriesRequest):
    """
    Analyze an entire series of episodes.
    Currently returns dummy data — swap with ml_pipeline_v2.analyze_series_v2() later.
    """
    if not payload.episodes:
        raise HTTPException(status_code=400, detail="Episodes list must not be empty")

    start = time.time()
    logger.info(f"Analyzing series — {len(payload.episodes)} episodes")

    result = analyze_dummy_series(payload.episodes, payload.category)

    duration = time.time() - start
    logger.info(f"Series analysis complete — Duration: {duration:.2f}s, Avg score: {result['series_insights']['avg_overall_score']}")
    return result
