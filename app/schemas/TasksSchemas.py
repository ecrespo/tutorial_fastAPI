from pydantic import BaseModel



class TaskBase(BaseModel):
    task_content: str
    is_complete: bool = False

