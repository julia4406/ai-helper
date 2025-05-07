from uuid import UUID
from fastapi import APIRouter

from src.api.schemas.user import UserCreateSchema


router = APIRouter()


@router.post("/users")
async def create_user(
    user_data: UserCreateSchema
):
    return {"ok": True}


@router.get("/users")
async def get_all_users():
    pass


@router.get("/users/{user_id}")
async def get_user_by_id(
    user_id: UUID,
):
    pass
