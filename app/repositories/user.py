from uuid import UUID

from app.database.models.user import User
from app.repositories.base import BaseRepository
from app.api.schemas.user import (
  UserCreateSchema,
  UserUpdateSchema,
  UserDetailResponseSchema, 
  UserListResponseSchema,
  )


class UserRepository(BaseRepository):  
    model = User

    async def create_new_user(self, user: UserCreateSchema) -> UserDetailResponseSchema:
        new_user = await self.add(obj_data=user.model_dump())
        return new_user.to_dto()

    async def get_list_of_users(self) -> UserListResponseSchema:
        return await self.list()

    async def get_user_by_id(self, user_id: UUID) -> UserDetailResponseSchema:
        return await self.get(user_id)

    async def update_user(
        self, user_id: UUID, user_upd: UserUpdateSchema
        ) -> UserDetailResponseSchema:
        user_upd = await self.update(
            obj_id=user_id, 
            obj_new_data=user_upd.model_dump()
            )
        return user_upd.to_dto()

    async def delete_user_by_id(self, user_id: UUID) -> UserDetailResponseSchema:
        return await self.delete(user_id)
