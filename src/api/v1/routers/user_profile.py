from uuid import UUID
from fastapi import APIRouter, UploadFile, File
from src.api.schemas.user_profile import UserProfileCreateSchema


router = APIRouter(tags=["User_profiles"], prefix="/user_profiles")

@router.post("")
async def generate_user_profile(
    id: UUID = UserProfileCreateSchema,
    cv_file_path: UploadFile = File(...)
):
    pass
  