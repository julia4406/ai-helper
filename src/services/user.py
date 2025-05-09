from src.repositories.user import UserRepository
from src.api.schemas.user import UserCreateSchema


class UserService:
    
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def create_new_user(self, user: UserCreateSchema):
        return await self._user_repo.create_new_user(user=user)

    async def get_list_of_users(self):
        return await self._user_repo.get_list_of_users()
