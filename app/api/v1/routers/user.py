from uuid import UUID
from fastapi import APIRouter

from app.api.dependencies import UserServiceDep
from app.api.schemas.user import (
  UserCreateResponseSchema,
  UserCreateSchema,
  UserDetailResponseSchema,
  UserUpdateSchema
  )


router = APIRouter(tags=["Users"], prefix="/users")


@router.post("", response_model=UserCreateResponseSchema)
async def create_user(
    user_data: UserCreateSchema,
    user_service: UserServiceDep
):
    new_user = await user_service.create_new_user(user=user_data)
    return UserCreateResponseSchema(id=new_user.id)


@router.get("")
async def get_all_users(user_service: UserServiceDep):
    return await user_service.get_list_of_users()


@router.get("/{user_id}", response_model=UserDetailResponseSchema)
async def get_user_by_id(
    user_id: UUID,
    user_service: UserServiceDep
):
    return await user_service.get_user_by_id(user_id=user_id)


@router.patch("/{user_id}", response_model=UserDetailResponseSchema)
async def partial_update_user(
    user_id: UUID,
    new_user_data: UserUpdateSchema,
    user_service: UserServiceDep

):
    updated_user = await user_service.update_user(
        user_id=user_id,
        user_upd=new_user_data
    )
    return updated_user


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: UUID,
    user_service: UserServiceDep
):
    await user_service.delete_user_by_id(user_id)
    return {"message": f"User {user_id} was successfully deleted."}
