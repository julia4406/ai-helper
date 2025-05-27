from uuid import UUID

from fastapi import HTTPException, status

class ObjectNotFoundException(HTTPException):
    def __init__(self, obj_type: str, obj_id: UUID | str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{obj_type} with id {obj_id} not found"
        )


class ObjectAlreadyExistException(HTTPException):
    def __init__(self, obj_type: str, obj_id: UUID | str) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{obj_type} with id {obj_id} already exist"
        )
