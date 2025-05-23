from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import logging
import os
import json
from typing import List, Dict, Any

from .models import Project
from .repositories.project_repository import TableProjectRepository

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

account_url = os.environ.get("AZURE_TABLES_ACCOUNT_URL")
table_name = os.environ.get("AZURE_TABLES_TABLE_NAME")
partition_key = os.environ.get("AZURE_TABLES_PARTITION", "projects")
if not account_url or not table_name:
    raise RuntimeError("Azure Table configuration missing: AZURE_TABLES_ACCOUNT_URL and AZURE_TABLES_TABLE_NAME must be set")

repo = TableProjectRepository(account_url, table_name, partition=partition_key)

global_omissions_path = (
    Path(__file__).resolve().parents[1] / "project_store" / "GlobalRepoOmissions.json"
)


def load_global_omissions() -> list[str]:
    if not global_omissions_path.exists():
        return []
    with global_omissions_path.open("r") as f:
        return json.load(f)

images_path = Path(__file__).resolve().parents[1] / "project_store" / "images"
app.mount("/images", StaticFiles(directory=images_path), name="images")


@app.get("/api/projects", response_model=List[Dict[str, Any]])
def list_projects():
    logger.debug("Listing all projects")
    projects = repo.list_projects()
    global_omissions = load_global_omissions()
    result = []
    for p in projects:
        exclude_paths = p.exclude_paths or []
        effective_exclude_paths = list(sorted(set(global_omissions + exclude_paths)))
        proj_dict = p.dict()
        proj_dict["effective_exclude_paths"] = effective_exclude_paths
        result.append(proj_dict)
    logger.debug("Returning %d projects", len(result))
    return result


@app.get("/api/projects/{project_id}", response_model=Dict[str, Any])
def get_project(project_id: str):
    logger.debug("Fetching project %s", project_id)
    project = repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    global_omissions = load_global_omissions()
    exclude_paths = project.exclude_paths or []
    effective_exclude_paths = list(sorted(set(global_omissions + exclude_paths)))
    proj_dict = project.dict()
    proj_dict["effective_exclude_paths"] = effective_exclude_paths
    logger.debug("Found project %s", project_id)
    return proj_dict


@app.get("/api/global_repo_omissions", response_model=list[str])
def get_global_repo_omissions():
    logger.debug("Returning global repo omissions")
    return load_global_omissions()

# Mount static frontend build output
static_dir = Path(__file__).parent / "static"
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
