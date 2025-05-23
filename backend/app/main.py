from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import logging
import os
import json
from typing import List, Dict, Any
import io

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

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

# Azure Table Storage Configuration
account_url = os.environ.get("AZURE_TABLES_ACCOUNT_URL")
table_name = os.environ.get("AZURE_TABLES_TABLE_NAME")
partition_key = os.environ.get("AZURE_TABLES_PARTITION", "projects")
if not account_url or not table_name:
    raise RuntimeError("Azure Table configuration missing: AZURE_TABLES_ACCOUNT_URL and AZURE_TABLES_TABLE_NAME must be set")

repo = TableProjectRepository(account_url, table_name, partition=partition_key)

# Azure Blob Storage Configuration
blob_account_url = os.environ.get("AZURE_BLOB_STORAGE_ACCOUNT_URL")
blob_container_name = os.environ.get("AZURE_BLOB_CONTAINER_NAME", "images")

if not blob_account_url:
    raise RuntimeError("Azure Blob Storage configuration missing: AZURE_BLOB_STORAGE_ACCOUNT_URL must be set")

try:
    credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(account_url=blob_account_url, credential=credential)
    container_client = blob_service_client.get_container_client(blob_container_name)
except Exception as e:
    logger.error(f"Failed to initialize Azure Blob Service Client: {e}")
    blob_service_client = None
    container_client = None


global_omissions_path = (
    Path(__file__).resolve().parents[1] / "project_store" / "GlobalRepoOmissions.json"
)


def load_global_omissions() -> list[str]:
    if not global_omissions_path.exists():
        return []
    with global_omissions_path.open("r") as f:
        return json.load(f)


@app.get("/api/images/{image_name}")
async def get_image(image_name: str):
    if not container_client:
        raise HTTPException(status_code=503, detail="Azure Blob Service is not available.")
    try:
        logger.debug(f"Attempting to fetch image '{image_name}' from blob storage container '{blob_container_name}'")
        blob_client = container_client.get_blob_client(image_name)
        
        if not blob_client.exists():
            logger.error(f"Image '{image_name}' not found in blob storage.")
            raise HTTPException(status_code=404, detail="Image not found")

        stream = blob_client.download_blob()
        
        # Determine media type based on file extension
        media_type = "application/octet-stream"
        if "." in image_name:
            extension = image_name.split(".")[-1].lower()
            if extension == "png":
                media_type = "image/png"
            elif extension in ["jpg", "jpeg"]:
                media_type = "image/jpeg"
            elif extension == "gif":
                media_type = "image/gif"
        
        logger.debug(f"Streaming image '{image_name}' with media type '{media_type}'")
        return StreamingResponse(io.BytesIO(stream.readall()), media_type=media_type)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching image '{image_name}' from blob storage: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


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
if static_dir.exists():
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
else:
    logger.warning(
        "Static directory %s not found. Skipping static file mounting.", static_dir
    )
