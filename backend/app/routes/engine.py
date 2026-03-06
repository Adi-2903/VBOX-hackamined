"""
Engine routes — GenAI generation + ML analysis endpoints.
Returns dummy data that mirrors the real pipeline output (BACKEND_INTEGRATION_GUIDE.md).

Includes input validation, logging, and async support as recommended by the guide.
"""
import logging
import time
import asyncio
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.schemas import (
    StoryPromptRequest,
    AnalysisRequest,
    AnalyzeSeriesRequest,
    GeneratedSeries,
    EpisodeAnalysis,
    SeriesAnalysis,
    DirectionsResponse,
)
from app.services.llm import (
    generate_directions_async,
    generate_series_async
)
from app.ml_engine.ml_pipeline_v2 import analyze_episode_v2, analyze_series_v2

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
    data = await generate_directions_async(concept)
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

    data = await generate_series_async(
        concept=req.concept,
        num_episodes=req.num_episodes,
        genres=req.genres,
        audience=req.audience,
        direction=req.direction
    )

    logger.info(f"Generation complete — {time.time() - start:.2f}s")
    return data


# ──────────────────────────────────────────────
# ML Analysis (matches BACKEND_INTEGRATION_GUIDE.md)
# ──────────────────────────────────────────────

@router.post("/analyze", response_model=EpisodeAnalysis)
async def analyze_content(req: AnalysisRequest):
    """
    Analyze single episode content for retention prediction using the ML engine.
    Matches the exact API from BACKEND_INTEGRATION_GUIDE.md and supports metadata.
    """
    if not req.text or not isinstance(req.text, str):
        raise HTTPException(status_code=400, detail="Text must be a non-empty string")
    if len(req.text) > MAX_TEXT_LENGTH:
        raise HTTPException(status_code=400, detail=f"Text exceeds maximum length of {MAX_TEXT_LENGTH}")

    start = time.time()
    logger.info(f"Starting ML analysis — Category: {req.category}, Length: {len(req.text)}")

    # Run ML pipeline in a thread pool to avoid blocking the event loop
    try:
        result = await asyncio.to_thread(
            analyze_episode_v2,
            text=req.text,
            category=req.category,
            hook=req.hook,
            cliffhanger=req.cliffhanger
        )
    except Exception as e:
        logger.error(f"ML Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"ML Engine error: {str(e)}")

    duration = time.time() - start
    logger.info(f"ML Analysis complete — Duration: {duration:.2f}s, Score: {result['summary']['overall_score']}")
    return result


@router.post("/analyze-series", response_model=SeriesAnalysis)
async def analyze_series(payload: AnalyzeSeriesRequest):
    """
    Analyze an entire series of episodes using the ML engine.
    """
    if not payload.episodes:
        raise HTTPException(status_code=400, detail="Episodes list must not be empty")

    start = time.time()
    logger.info(f"Analyzing series with ML — {len(payload.episodes)} episodes")

    # Prepare episode texts and metadata for the ML engine
    # analyze_series_v2 currently takes a list of strings, but we should probably 
    # process them to match what the frontend expects or what the ML engine needs.
    # Looking at ml_pipeline_v2.py: analyze_series_v2(episodes: list[str])
    
    # However, SeriesAnalysis expects EpisodeAnalysisWithMeta which includes title, etc.
    # So we'll loop and call analyze_episode_v2 for each to keep metadata.
    
    try:
        episode_analyses = []
        for ep in payload.episodes:
            # Run each analysis in a thread
            res = await asyncio.to_thread(
                analyze_episode_v2,
                text=ep.story,
                category=payload.category,
                hook=ep.hook,
                cliffhanger=ep.cliffhanger
            )
            episode_analyses.append({
                "episode_number": ep.episode_number,
                "title": ep.title,
                "analysis": res
            })
        
        # We need to compute series insights manually since we called individual episodes
        # to preserve titles and episode numbers in the response format.
        from app.ml_engine.ml_pipeline_v2 import _compute_series_insights
        series_insights_raw = _compute_series_insights([ea["analysis"] for ea in episode_analyses])
        
        # Add weakest/strongest which might be missing from raw insights
        scores = [ea["analysis"]["summary"]["overall_score"] for ea in episode_analyses]
        series_insights_raw["weakest_episode"] = scores.index(min(scores)) + 1 if scores else 1
        series_insights_raw["strongest_episode"] = scores.index(max(scores)) + 1 if scores else 1

        result = {
            "episodes": episode_analyses,
            "series_insights": series_insights_raw
        }
    except Exception as e:
        logger.error(f"ML Series Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"ML Engine error: {str(e)}")

    duration = time.time() - start
    logger.info(f"Series ML analysis complete — Duration: {duration:.2f}s, Avg score: {result['series_insights'].get('avg_overall_score')}")
    return result
