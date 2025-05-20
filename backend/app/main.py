from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
try:
    from fastapi.templating import Jinja2Templates
    import jinja2  # ensure dependency is installed
except Exception as e:  # pragma: no cover - optional
    Jinja2Templates = None  # type: ignore
    missing_jinja2_error: Optional[Exception] = e
else:
    missing_jinja2_error = None
import logging
import os

from .models import Project
from .repositories.project_repository import FileProjectRepository

logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG") == "1" else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

repo = FileProjectRepository(Path(__file__).resolve().parents[1] / "project_store")

images_path = Path(__file__).resolve().parents[1] / "project_store" / "images"
app.mount("/images", StaticFiles(directory=images_path), name="images")

templates: Optional[Jinja2Templates]
if Jinja2Templates is None:
    templates = None
    logger.warning("Jinja2Templates not available: %s", missing_jinja2_error)
else:
    templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))


@app.get("/api/projects", response_model=list[Project])
def list_projects():
    logger.debug("Listing all projects")
    projects = repo.list_projects()
    logger.debug("Returning %d projects", len(projects))
    return projects


@app.get("/api/projects/{project_id}", response_model=Project)
def get_project(project_id: str):
    logger.debug("Fetching project %s", project_id)
    project = repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    logger.debug("Found project %s", project_id)
    return project


@app.get("/project/{project_id}", response_class=HTMLResponse)
def project_page(request: Request, project_id: str):
    logger.debug("Rendering page for project %s", project_id)
    project = repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if templates:
        return templates.TemplateResponse(
            "project_detail.html",
            {"request": request, "project": project},
        )
    html = f"<h1>{project.title}</h1><p>{project.description}</p>"
    return HTMLResponse(html)


# Path to the built frontend assets
build_path = Path(__file__).resolve().parents[1] / 'frontend' / 'dist'

if build_path.exists():
    app.mount('/', StaticFiles(directory=build_path, html=True), name='static')
else:
    @app.get('/', response_class=HTMLResponse)
    async def placeholder():
        return "<html><body><h1>Hello World</h1></body></html>"
