from typing import Optional

from fastapi import APIRouter, Depends

from app.api.exceptions import EntityAlreadyExists
from app.api.security.utils import get_current_user
from app.api.services import HistoryService, UserService
from app.db import schemas

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/')
async def create_user(user: schemas.UserCreate) -> schemas.UserOut:
    user_exists = await UserService.find_by_name(username=user.username)

    if user_exists:
        raise EntityAlreadyExists('user')

    new_user = await UserService.create(user)

    return new_user


@router.get('/me')
async def read_users_me(
    current_user: schemas.UserOut = Depends(get_current_user),
) -> schemas.UserOut:
    return current_user


@router.get('/me/history/')
async def get_history(
    user: schemas.UserOut = Depends(get_current_user),
) -> Optional[schemas.HistoryOut]:
    history = await HistoryService.find_user_history(user.id)

    return history
