from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import List, Protocol, Optional

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
