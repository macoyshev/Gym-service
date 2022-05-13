from typing import Optional

from fastapi.exceptions import HTTPException


class EntityAlreadyExists(HTTPException):
    def __init__(self, entity: Optional[str] = 'Entity') -> None:
        super().__init__(status_code=409, detail=f'{entity} already exists')


class EntityNotFound(HTTPException):
    def __init__(self, entity: Optional[str] = 'Entity') -> None:
        super().__init__(status_code=404, detail=f'{entity} not found')
