from pydantic import BaseModel
from typing import Optional


class Project(BaseModel):
    id: str
    title: str
    image: Optional[str] = None
    repo_url: str
    description: str
    demo_url: str

    class Config:
        orm_mode = True
