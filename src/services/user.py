class UserService:

  def __init__(self):
    self._user_repo = ...

  async def create_new_user(self, user: UserCreateSchema):
    await self._user_repo