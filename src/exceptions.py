from uuid import UUID

from fastapi import HTTPException, status

class UserNotFoundException(HTTPException):
    def __init__(self, user_id: UUID) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )