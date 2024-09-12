from datetime import datetime, timedelta
from typing import List
from beanie import PydanticObjectId

from fastapi import Request, Depends, Security, HTTPException, status,APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app.repositories.UserRepository import UserRepository
from app.schemas.UserSchema import UserBase, UserResponseBase, UserUpdateRequestBase, UpdatePasswordRequest
from app.utils.LoggerSingleton import logger
from app.models.UsersModel import User, Token
from app.utils.auth import get_current_active_user, get_password_hash, verify_password, authenticate_user, \
    create_access_token

from app.utils.configs import ACCESS_TOKEN_EXPIRE_MINUTES

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

@users_router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def retrieveUser(user_id: PydanticObjectId) -> User:

    user_to_get = await UserRepository().get_user(_id=user_id)
    logger.info(user_id)
    if not user_to_get:
        raise HTTPException(status_code=404, detail="Resource not found")
    logger.info(user_to_get)
    logger.info("User retrieved")
    return user_to_get


@users_router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def updateUser(user: UserUpdateRequestBase, user_id: PydanticObjectId) -> User:

    user_to_update = await UserRepository().update_user(user_id, user.model_dump())
    if not user_to_update:
        raise HTTPException(status_code=404, detail="Resource not found")

    logger.info("User updated")
    return user_to_update


@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteUser(user_id: PydanticObjectId):
    user_to_delete = await UserRepository().delete_user(user_id)
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="Resource not found")

    logger.info("User deleted")
    return {"message": "User deleted"}


@users_router.post("/update_password")
async def update_password(user_id: PydanticObjectId, password: UpdatePasswordRequest):

    logger.info(f"Updating password for user {user_id}")
    logger.info(password)
    user_to_update = await UserRepository().get_user(_id=user_id)
    user_dict = user_to_update.model_dump()
    # del(user_dict["id"])
    logger.info(user_dict)
    logger.info(get_password_hash(password.old_password))
    result = verify_password(password.old_password,user_dict["hashed_password"])
    logger.info(result)
    if verify_password(password.old_password,user_dict["hashed_password"]):
        raise HTTPException(status_code=404, detail="Old password is incorrect")
    if password.new_password != password.confirm_password:
        raise HTTPException(status_code=404, detail="New passwords do not match")


    user_dict["hashed_password"] = get_password_hash(password.new_password)
    user_dict["updated_at"] = datetime.now()
    user_model = User(**user_dict)
    logger.info(user_model)
    result = await UserRepository().update_user(user_id, user_model)
    if not result:
        raise HTTPException(status_code=404, detail="Resource not found")
    logger.info("Password updated")
    return "Password updated"


@users_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    logger.info(f"User {dict(form_data)} attempted to login")
    # user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect username or password",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = create_access_token(
    #     data={"sub": user.username}, expires_delta=access_token_expires
    # )
    # return {"access_token": access_token, "token_type": "bearer"}
