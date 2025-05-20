from sqlalchemy import Column, String
from .database import Base

class ProjectORM(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    image = Column(String, nullable=True)
    repo_url = Column(String, nullable=False)
    description = Column(String, nullable=False)
    demo_url = Column(String, nullable=False)
