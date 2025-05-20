from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .models import Project
from .repositories.project_repository import FileProjectRepository

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

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))


@app.get("/api/projects", response_model=list[Project])
def list_projects():
    return repo.list_projects()


@app.get("/api/projects/{project_id}", response_model=Project)
def get_project(project_id: str):
    project = repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.get("/project/{project_id}", response_class=HTMLResponse)
def project_page(request: Request, project_id: str):
    project = repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return templates.TemplateResponse("project_detail.html", {"request": request, "project": project})


# Path to the built frontend assets
build_path = Path(__file__).resolve().parents[1] / 'frontend' / 'dist'

if build_path.exists():
    app.mount('/', StaticFiles(directory=build_path, html=True), name='static')
else:
    @app.get('/', response_class=HTMLResponse)
    async def placeholder():
        return "<html><body><h1>Hello World</h1></body></html>"
