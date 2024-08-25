from typing import Optional, List
from beanie import PydanticObjectId

from app.models.Tasks import Task
from app.utils.LoggerSingleton import logger


class TaskRepository:
    @staticmethod
    async def get_all_tasks(page: int = 1, limit: int = 10) -> List[Task]:
        return await Task.find_all().skip((page - 1) * limit).limit(limit).to_list()

    @staticmethod
    async def get_task_by_id(task_id: PydanticObjectId) -> Optional[Task]:
        return await Task.get(task_id)

    @staticmethod
    async def create_task(task_data: Task) -> Task:
        await task_data.insert()
        return task_data

    @staticmethod
    async def update_task(task_id: PydanticObjectId, task_data: Task) -> Optional[Task]:
        task = await TaskRepository.get_task_by_id(task_id)
        if task:
            task.task_content = task_data.task_content
            task.is_complete = task_data.is_complete
            task.date_created = task_data.date_created
            await task.save()
        return task

    @staticmethod
    async def delete_task(task_id: PydanticObjectId) -> Optional[Task]:
        task = await TaskRepository.get_task_by_id(task_id)
        if task:
            await task.delete()
        return task