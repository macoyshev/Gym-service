from typing import Optional

from fastapi import HTTPException
from starlette import status


class InvalidCredentials(HTTPException):
    def __init__(
        self,
        detail: Optional[str] = 'Could not validate credentials',
    ) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={'WWW-Authenticate': 'Bearer'},
        )
