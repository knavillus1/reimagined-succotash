from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
import logging
import os
import json
from typing import List, Dict, Any

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

repo = FileProjectRepository(
    Path(__file__).resolve().parents[1] / "project_store" / "projects"
)

global_omissions_path = (
    Path(__file__).resolve().parents[1] / "project_store" / "GlobalRepoOmissions.json"
)


def load_global_omissions() -> list[str]:
    if not global_omissions_path.exists():
        return []
    with global_omissions_path.open("r") as f:
        return json.load(f)

images_path = Path(__file__).resolve().parents[1] / "project_store" / "images"

# Optionally serve images from Azure Blob Storage if a connection string is
# provided. Otherwise fall back to local static files.
azure_conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
azure_container = os.getenv("AZURE_STORAGE_CONTAINER", "images")

if azure_conn_str:
    try:
        from azure.storage.blob import BlobServiceClient

        blob_service_client = BlobServiceClient.from_connection_string(
            azure_conn_str
        )
        container_client = blob_service_client.get_container_client(azure_container)

        @app.get("/images/{image_path:path}")
        def fetch_image(image_path: str):
            try:
                blob_client = container_client.get_blob_client(image_path)
                data = blob_client.download_blob().readall()
                props = blob_client.get_blob_properties()
                media_type = (
                    props.content_settings.content_type
                    or "application/octet-stream"
                )
                return Response(content=data, media_type=media_type)
            except Exception:
                logger.exception("Failed to fetch image %s from Azure", image_path)
                raise HTTPException(status_code=404, detail="Image not found")

    except Exception:
        logger.exception("Failed to configure Azure Blob Storage, falling back to local images")
        app.mount("/images", StaticFiles(directory=images_path), name="images")
else:
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
