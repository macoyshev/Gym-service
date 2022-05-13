from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends

from app.api.exceptions import EntityAlreadyExists, EntityNotFound
from app.api.security import utils
from app.api.services import MuscleService
from app.db.schemas import MuscleCreate, MuscleOut

router = APIRouter(
    prefix='/muscles', tags=['muscles'], dependencies=[Depends(utils.get_current_user)]
)


@router.get('/', response_model=list[MuscleOut])
async def fetch(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> list[MuscleOut]:
    return await MuscleService.find_all(limit, offset)


@router.post('/', response_model=MuscleOut, status_code=HTTPStatus.CREATED)
async def create(muscle: MuscleCreate) -> MuscleOut:
    msl = await MuscleService.find_by_name(muscle.name)

    if msl:
        raise EntityAlreadyExists()

    return await MuscleService.create(muscle)


@router.get('/{muscle_id}', response_model=MuscleOut)
async def get_by_id(muscle_id: int) -> Optional[MuscleOut]:
    msl = await MuscleService.find_by_id(muscle_id)

    if not msl:
        raise EntityNotFound()

    return msl


@router.put('/{muscle_id}', response_model=MuscleOut)
async def update(muscle_id: int, muscle: MuscleCreate) -> MuscleOut:
    msl = await MuscleService.find_by_id(muscle_id)

    if not msl:
        raise EntityNotFound()

    msl_upd = await MuscleService.update(msl_id=muscle_id, msl_upd=muscle)

    return msl_upd
