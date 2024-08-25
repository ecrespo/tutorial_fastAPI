from datetime import datetime
from typing import List

from fastapi import Request, Depends, Security, HTTPException, status,APIRouter

from app.repositories.UserRepository import UserRepository
from app.schemas.UserSchema import UserBase, UserResponseBase
from app.utils.LoggerSingleton import logger
from app.models.UsersModel import User
from app.utils.auth import get_current_active_user, get_password_hash

users_router = APIRouter(
    tags=["users"]
)

@users_router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    logger.info(f"User {current_user.username} accessed their own information")
    return current_user


@users_router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_user(user: UserBase):
    user_dict = user.model_dump()
    user_dict["date_created"] = datetime.now().isoformat()
    user_dict["disabled"] = False
    password = user_dict["password"]
    user_dict["hashed_password"] = get_password_hash(password)
    del user_dict["password"]
    user_model = User(**user_dict)
    result = await UserRepository().add_user(user_model)
    if not result:
        raise HTTPException(status_code=404, detail="Resource not added")

    logger.info("User has been saved")
    return {"message": "User added"}

@users_router.get("/",status_code=status.HTTP_200_OK)
async def getallusers() -> List[UserResponseBase]:

    users = await UserRepository().list_users()
    items = []
    for user in users:
        item = user.model_dump()
        del(item["hashed_password"])
        items.append(item)
    return items

# @users_router.get("/{user_id}", status_code=status.HTTP_200_OK)
# async def retrieveTask(task_id: PydanticObjectId) -> User:
#
#     task_to_get = await TaskRepository.get_task_by_id(task_id)
#     logger.info(task_id)
#     if not task_to_get:
#         raise HTTPException(status_code=404, detail="Resource not found")
#     logger.info(task_to_get)
#     logger.info("Task retrieved")
#     return task_to_get

#
# @task_router.put("/{task_id}", status_code=status.HTTP_200_OK)
# async def updateTask(task: Task, task_id: PydanticObjectId) -> Task:
#
#     task_to_update = await TaskRepository.update_task(task_id, task)
#     if not task_to_update:
#         raise HTTPException(status_code=404, detail="Resource not found")
#
#     logger.info("Task updated")
#     return task_to_update
#
#
# @task_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def deleteTask(task_id: PydanticObjectId):
#     task_to_delete = await TaskRepository.delete_task(task_id)
#     if not task_to_delete:
#         raise HTTPException(status_code=404, detail="Resource not found")
#
#     logger.info("Task deleted")
#     return {"message": "Task deleted"}