from uuid import UUID
from fastapi import APIRouter, UploadFile, File
from src.api.schemas.user_profile import UserProfileCreateSchema


router = APIRouter(tags=["User_profiles"], prefix="/user_profiles")

@router.post("")
async def generate_user_profile(
    id: UUID,
    cv_file_path: UploadFile = File(...)
):
    pdf_content_bytes = await cv_file_path.read()
    pdf_content_task = extract_text_from_pdf.delay(pdf_content_bytes)
    return {
        "task_id": pdf_content_task.id,
        "content": pdf_content_task.text
      }
  