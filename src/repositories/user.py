from src.api.schemas.user import UserCreateSchema


class UserRepository:
  model = ...

  async def create_new_user(
      self,
      user: UserCreateSchema,
      
      ):
    return await self.add()