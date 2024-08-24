from pydantic import BaseModel

from app.models.Tasks import Task


class TaskBase(BaseModel):
    task_content: str
    is_complete: bool = False

