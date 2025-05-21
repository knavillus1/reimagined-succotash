from pydantic import BaseModel
from typing import Optional, List


class Project(BaseModel):
    id: str
    title: str
    image: Optional[str] = None
    repo_url: str
    description: str
    demo_url: str
    exclude_paths: Optional[List[str]] = None
