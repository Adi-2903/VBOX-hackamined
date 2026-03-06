"""
Project routes — MongoDB CRUD for saved projects.
"""
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime, timezone
from app.database import get_database
from app.models.schemas import ProjectCreate, ProjectResponse

router = APIRouter(prefix="/api/v1/projects", tags=["Projects"])


def _project_doc_to_response(doc: dict) -> dict:
    """Convert a MongoDB document to a ProjectResponse dict."""
    return {
        "id": str(doc["_id"]),
        "title": doc.get("title", ""),
        "concept": doc.get("concept", ""),
        "genres": doc.get("genres", []),
        "generated_series": doc.get("generated_series"),
        "analysis": doc.get("analysis"),
        "status": doc.get("status", "draft"),
        "created_at": doc.get("created_at", ""),
        "episode_count": doc.get("episode_count", 0),
        "overall_score": doc.get("overall_score"),
    }


@router.get("", response_model=list[ProjectResponse])
async def list_projects():
    """List all saved projects, most recent first."""
    db = get_database()
    cursor = db["projects"].find().sort("created_at", -1)
    projects = []
    async for doc in cursor:
        projects.append(_project_doc_to_response(doc))
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """Get a single project by ID."""
    db = get_database()
    try:
        doc = await db["projects"].find_one({"_id": ObjectId(project_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid project ID format")
    if not doc:
        raise HTTPException(status_code=404, detail="Project not found")
    return _project_doc_to_response(doc)


@router.post("", response_model=ProjectResponse, status_code=201)
async def create_project(project: ProjectCreate):
    """Create and save a new project to MongoDB."""
    db = get_database()
    doc = project.model_dump()
    doc["created_at"] = datetime.now(timezone.utc).isoformat()
    doc["status"] = "generated"

    # Compute derived fields
    if project.generated_series and project.generated_series.episodes:
        doc["episode_count"] = len(project.generated_series.episodes)
    if project.analysis and project.analysis.series_insights:
        doc["overall_score"] = int(project.analysis.series_insights.avg_overall_score)

    result = await db["projects"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return _project_doc_to_response(doc)


@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: str):
    """Delete a project by ID."""
    db = get_database()
    try:
        result = await db["projects"].delete_one({"_id": ObjectId(project_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid project ID format")
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    return None
