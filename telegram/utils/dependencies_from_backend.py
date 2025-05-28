from app.database.core.engine import async_session_maker
from app.repositories.user import UserRepository
from app.services.user import UserService


async def provide_user_service() -> UserService:
    async with async_session_maker() as session:
        user_repo = UserRepository(session=session)
        return UserService(user_repo=user_repo)