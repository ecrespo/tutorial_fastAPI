from typing import List, Optional
from beanie import PydanticObjectId
from app.models.UsersModel import User  # Asegúrate de importar el modelo User definido anteriormente
from app.utils.LoggerSingleton import logger


class UserRepository:
    async def add_user(self, entity: User) -> User:
        await entity.insert()
        return entity

    async def get_user(self, _id: PydanticObjectId) -> Optional[User]:
        return await User.get(_id)

    async def update_user(self, _id: PydanticObjectId, entity: User) -> Optional[User]:
        logger.info(f"Updating user {_id}")
        logger.info(entity)
        await User.find_one(User.id == _id).update({"$set": entity})
        return await self.get_user(_id)

    async def delete_user(self, _id: PydanticObjectId) -> bool:
        user = await self.get_user(_id)
        if user:
            await user.delete()
            return True
        return False

    async def list_users(self) -> List[User]:
        return await User.find_all().to_list()

