from datetime import datetime

from fastapi import APIRouter, HTTPException, status

from typing import List
from beanie import PydanticObjectId

from app.schemas.TasksSchemas import TaskBase
from app.utils.LoggerSingleton import logger
from app.repositories.TaskRepository import TaskRepository
from app.models.Tasks import Task

task_router = APIRouter()


@task_router.get("/",status_code=status.HTTP_200_OK)
async def getalltasks(page: int = 1, limit: int = 10) -> List[Task]:

    tasks = await TaskRepository.get_all_tasks(page= page, limit = limit)
    return tasks


@task_router.post("/",status_code=status.HTTP_201_CREATED)
async def createTask(task: TaskBase):
    task_dict = task.model_dump()
    task_dict["date_created"] = datetime.now().isoformat()
    task_model = Task(**task_dict)
    task_data = await TaskRepository.create_task(task_model)
    logger.info("Task has been saved")
    return {"message": "Task has been saved"}


@task_router.get("/{task_id}", status_code=status.HTTP_200_OK)
async def retrieveTask(task_id: PydanticObjectId) -> Task:
    task_to_get = await TaskRepository.get_task_by_id(task_id)
    logger.info(task_id)
    if not task_to_get:
        raise HTTPException(status_code=404, detail="Resource not found")
    logger.info(task_to_get)
    logger.info("Task retrieved")
    return task_to_get


@task_router.put("/{task_id}", status_code=status.HTTP_200_OK)
async def updateTask(task: Task, task_id: PydanticObjectId) -> Task:

    task_to_update = await TaskRepository.update_task(task_id, task)
    if not task_to_update:
        raise HTTPException(status_code=404, detail="Resource not found")

    logger.info("Task updated")
    return task_to_update


@task_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteTask(task_id: PydanticObjectId):
    task_to_delete = await TaskRepository.delete_task(task_id)
    if not task_to_delete:
        raise HTTPException(status_code=404, detail="Resource not found")

    logger.info("Task deleted")
    return {"message": "Task deleted"}