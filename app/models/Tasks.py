from datetime import datetime
from beanie import Document
from pydantic import Field


class Task(Document):
    task_content: str = Field(max_length=400)
    is_complete: bool = False
    date_created: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "tasks_database"

    class Config:
        schema_extra = {
            "example": {
                "task_content": "A sample content",
                "is_complete": True,
                "date_created": datetime.now(),
            }
        }

