from uuid import UUID
from fastapi import APIRouter, UploadFile, File
from src.api.schemas.user_profile import UserProfileCreateSchema
from src.celery.tasks.pdf_reader_task import extract_text_from_pdf


router = APIRouter(tags=["User_profiles"], prefix="/user_profiles")

@router.post("")
async def generate_user_profile(
    id: UUID,
    cv_file_path: UploadFile = File(...)
):
    pdf_content_bytes = await cv_file_path.read()
    # TODO remade into task (all services inside compose)
    # pdf_content_task = extract_text_from_pdf.delay(pdf_content_bytes)
    pdf_content_task = extract_text_from_pdf(pdf_content_bytes)
    return {
        "content": pdf_content_task
      }
  