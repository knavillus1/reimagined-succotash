from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import List, Protocol, Optional

from azure.data.tables import TableServiceClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import HttpResponseError

from ..models import Project

logger = logging.getLogger(__name__)


class ProjectRepository(Protocol):
    def list_projects(self) -> List[Project]:
        ...

    def get_project(self, project_id: str) -> Optional[Project]:
        ...


class FileProjectRepository:
    def __init__(self, directory: Path):
        self.directory = directory

    def _project_path(self, project_id: str) -> Path:
        return self.directory / f"{project_id}.json"

    def list_projects(self) -> List[Project]:
        logger.debug("Reading projects from %s", self.directory)
        projects = []
        for file in self.directory.glob("*.json"):
            logger.debug("Loading project file %s", file)
            with file.open("r") as f:
                data = json.load(f)
                projects.append(Project(**data))
        return projects

    def get_project(self, project_id: str) -> Optional[Project]:
        path = self._project_path(project_id)
        if not path.exists():
            return None
        logger.debug("Loading project %s from %s", project_id, path)
        with path.open("r") as f:
            data = json.load(f)
            return Project(**data)


class TableProjectRepository:
    def __init__(self, account_url: str, table_name: str, partition: str = "projects"):
        self.partition = partition
        credential = DefaultAzureCredential()
        service = TableServiceClient(endpoint=account_url, credential=credential)
        service.create_table_if_not_exists(table_name=table_name)  # Corrected: Use service client to create table
        self.table = service.get_table_client(table_name)

    def _deserialize(self, entity: dict) -> Project:
        data_json = entity.get("data")
        if data_json:
            data = json.loads(data_json)
            # Ensure exclude_paths is a list if it's a string representation of a list
            if isinstance(data.get("exclude_paths"), str):
                try:
                    data["exclude_paths"] = json.loads(data["exclude_paths"])
                except json.JSONDecodeError:
                    logger.warning(f"Failed to parse exclude_paths string: {data['exclude_paths']}. Defaulting to empty list.")
                    data["exclude_paths"] = []
            elif data.get("exclude_paths") is None: # Handle if exclude_paths might be missing
                 data["exclude_paths"] = []

        else:
            # This part handles when project data is stored as individual columns
            data = {k: v for k, v in entity.items() if k not in {"PartitionKey", "RowKey", "etag", "Timestamp"}}
            if isinstance(data.get("exclude_paths"), str):
                try:
                    data["exclude_paths"] = json.loads(data["exclude_paths"])
                except json.JSONDecodeError:
                    logger.warning(f"Failed to parse exclude_paths string from entity properties: {data['exclude_paths']}. Defaulting to empty list.")
                    data["exclude_paths"] = []
            elif data.get("exclude_paths") is None: # Handle if exclude_paths might be missing
                 data["exclude_paths"] = []
            data.setdefault("id", entity["RowKey"])
        
        # Ensure exclude_paths is a list if it's None at this point, to satisfy Pydantic model
        if data.get("exclude_paths") is None:
            data["exclude_paths"] = []
            
        return Project(**data)

    def list_projects(self) -> List[Project]:
        logger.debug("Querying projects from Azure Table")
        entities = self.table.query_entities(f"PartitionKey eq '{self.partition}'")
        return [self._deserialize(e) for e in entities]

    def get_project(self, project_id: str) -> Optional[Project]:
        try:
            entity = self.table.get_entity(partition_key=self.partition, row_key=project_id)
        except HttpResponseError as exc:
            if getattr(exc, "status_code", None) == 404:
                return None
            raise
        return self._deserialize(entity)
