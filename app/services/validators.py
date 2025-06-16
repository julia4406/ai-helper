from app.api.schemas.user import UserCreateSchema
from app.repositories.user import UserRepository


async def existing_user(
        user: UserCreateSchema,
        user_repo: UserRepository
) -> bool:
    telegram_id = await user_repo.get_user_by_field(
        "telegram_id", user.telegram_id
    )
    username = await user_repo.get_user_by_field(
        "username", user.username
    )
    if any([telegram_id, username]):
        return True
    return False
