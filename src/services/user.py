from uuid import UUID

from src.repositories.user import UserRepository
from src.api.schemas.user import UserCreateSchema, UserUpdateSchema


class UserService:
    
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def create_new_user(self, user: UserCreateSchema):
        return await self._user_repo.create_new_user(user=user)

    async def get_list_of_users(self):
        return await self._user_repo.get_list_of_users()

    async def get_user_by_id(self, user_id: UUID):
        return await self._user_repo.get_user_by_id(user_id)

    async def update_user(self, user_id: UUID, user_upd: UserUpdateSchema):
        return await self._user_repo.update_user(user_id=user_id, user_upd=user_upd)

    async def delete_user_by_id(self, user_id: UUID):
        return await self._user_repo.delete_user_by_id(user_id=user_id)
