from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends

from app.api.exceptions import EntityAlreadyExists, EntityNotFound
from app.api.security.utils import get_current_user
from app.api.services import ExercisesService
from app.db.schemas import ExerciseCreate, ExerciseOut

router = APIRouter(
    prefix='/exercises', tags=['exercises'], dependencies=[Depends(get_current_user)]
)


@router.get('/', response_model=list[ExerciseOut])
async def fetch(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> list[ExerciseOut]:
    return await ExercisesService.find_all(limit, offset)


@router.post('/', response_model=ExerciseOut, status_code=HTTPStatus.CREATED)
async def create(exercise: ExerciseCreate) -> ExerciseOut:
    exr = await ExercisesService.find_by_name(exercise.name)

    if exr:
        raise EntityAlreadyExists()

    exr = await ExercisesService.create(exercise)

    return exr


@router.get('/{exercise_id}', response_model=ExerciseOut)
async def get_by_id(exercise_id: int) -> Optional[ExerciseOut]:
    exr = await ExercisesService.find_by_id(exercise_id)

    if not exr:
        raise EntityNotFound()

    return exr


@router.put('/{exercise_id}', response_model=ExerciseOut)
async def update(exercise_id: int, exercise: ExerciseCreate) -> ExerciseOut:
    exr = await ExercisesService.update(exr_id=exercise_id, exr_upd=exercise)

    return exr


@router.delete('/{exercise_id}')
async def delete(exercise_id: int) -> None:
    await ExercisesService.delete(exercise_id)
