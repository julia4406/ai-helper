from uuid import UUID

from fastapi import HTTPException, status

class ObjectNotFoundException(HTTPException):
    def __init__(self, obj_id: UUID) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Object with id {obj_id} not found"
        )


class ObjectAlreadyExistException(HTTPException):
    def __init__(self, obj_id: UUID) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Object with id {obj_id} already exist"
        )
