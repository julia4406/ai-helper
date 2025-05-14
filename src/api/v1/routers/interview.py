from uuid import UUID

from fastapi import APIRouter

router = APIRouter(tags=["Interviews"], prefix="/interviews")

@router.post("")
async def create_interview(
    user_id: UUID,
):

    return {
        "content": "some message"
      }
