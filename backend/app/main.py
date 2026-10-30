"""FastAPI application: REST API for the AI furniture planner.

Run:  uvicorn app.main:app --reload   (from the backend/ directory)
Docs: http://localhost:8000/docs
"""

import os
import uuid

from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware

from . import catalog
from .geometry import validate
from .layout import auto_layout, layout_csv
from .models import (
    FurnitureItem,
    LayoutRequest,
    LayoutResponse,
    Project,
    RecommendationRequest,
    RecommendationResponse,
    StoredProject,
    Style,
    ValidateRequest,
    Violation,
)
from .recommender import recommend

app = FastAPI(title="AI Furniture Planner API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory project store; replaced by PostgreSQL in DIP-17.
_projects: dict[str, StoredProject] = {}


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/catalog", response_model=list[FurnitureItem])
def list_catalog(
    category: str | None = None,
    style: Style | None = None,
    max_price: int | None = Query(None, ge=0),
) -> list[FurnitureItem]:
    return catalog.search(category=category, style=style, max_price=max_price)


@app.get("/api/catalog/categories", response_model=list[str])
def list_categories() -> list[str]:
    return catalog.categories()


@app.get("/api/catalog/{item_id}", response_model=FurnitureItem)
def get_item(item_id: str) -> FurnitureItem:
    item = catalog.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/api/recommendations", response_model=RecommendationResponse)
def recommendations(request: RecommendationRequest) -> RecommendationResponse:
    return recommend(request)


@app.post("/api/layout", response_model=LayoutResponse)
def layout(request: LayoutRequest) -> LayoutResponse:
    return auto_layout(request)


@app.post("/api/layout/csv")
def layout_export(request: LayoutRequest) -> Response:
    return Response(
        layout_csv(auto_layout(request)),
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="layout_run.csv"'},
    )


@app.post("/api/validate", response_model=list[Violation])
def validate_layout(request: ValidateRequest) -> list[Violation]:
    return validate(request.room, request.placements, catalog.load_catalog())


@app.post("/api/projects", response_model=StoredProject, status_code=201)
def create_project(project: Project) -> StoredProject:
    stored = StoredProject(id=uuid.uuid4().hex, **project.model_dump())
    _projects[stored.id] = stored
    return stored


@app.get("/api/projects/{project_id}", response_model=StoredProject)
def get_project(project_id: str) -> StoredProject:
    if project_id not in _projects:
        raise HTTPException(status_code=404, detail="Project not found")
    return _projects[project_id]


@app.put("/api/projects/{project_id}", response_model=StoredProject)
def update_project(project_id: str, project: Project) -> StoredProject:
    if project_id not in _projects:
        raise HTTPException(status_code=404, detail="Project not found")
    _projects[project_id] = StoredProject(id=project_id, **project.model_dump())
    return _projects[project_id]
