from uuid import UUID
from fastapi import APIRouter, UploadFile, File, Form

from app.api.dependencies import ProfileServiceDep, UserServiceDep
from app.api.schemas.user_profile import UserProfileCreateSchema


router = APIRouter(tags=["User profiles"], prefix="/user_profiles")

@router.post("")
async def generate_user_profile(
    profile_service: ProfileServiceDep,
    user_id: UUID = Form(...),
    cv_file: UploadFile = File(...),
):
    profile_data = UserProfileCreateSchema(
        user_id=user_id,
        cv_file=cv_file
    )
    profile_content = await profile_service.create_new_profile(
        profile_data=profile_data
    )

    return {
        "content": profile_content
      }


@router.get("")
async def get_user_profiles(
        user_id: UUID,
        profile_service: ProfileServiceDep,
        user_service: UserServiceDep
):
    await user_service.get_user_by_id(user_id)

    user_profiles = await profile_service.get_profiles(user_id)
    return user_profiles
