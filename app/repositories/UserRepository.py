from typing import List, Optional
from beanie import PydanticObjectId
from app.models.UsersModel import User  # Asegúrate de importar el modelo User definido anteriormente


class UserRepository:
    async def add_user(self, entity: User) -> User:
        await entity.insert()
        return entity

    async def get_user(self, _id: PydanticObjectId) -> Optional[User]:
        return await User.get(_id)

    async def update_user(self, _id: PydanticObjectId, entity: User) -> Optional[User]:
        await User.find_one(User._id == _id).update({"$set": entity.dict()})
        return await self.get(id)

    async def delete_user(self, _id: PydanticObjectId) -> bool:
        user = await self.get(_id)
        if user:
            await user.delete()
            return True
        return False

    async def list_users(self) -> List[User]:
        return await User.find_all().to_list()

