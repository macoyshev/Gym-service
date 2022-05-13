from http import HTTPStatus

from fastapi import APIRouter, Depends

from app.api.exceptions import EntityAlreadyExists, EntityNotFound
from app.api.security import utils
from app.api.services import HistoryService, TrainService
from app.db import schemas

router = APIRouter(
    prefix='/trains', tags=['trains'], dependencies=[Depends(utils.get_current_user)]
)


@router.get('/', response_model=list[schemas.TrainOut])
async def fetch() -> list[schemas.TrainOut]:
    trains = await TrainService.find_all()

    return trains


@router.post('/', response_model=schemas.TrainOut, status_code=HTTPStatus.CREATED)
async def create(train: schemas.TrainCreate) -> schemas.TrainOut:
    train_exists = await TrainService.find_by_name(train.name)

    if train_exists:
        raise EntityAlreadyExists()

    train_new = await TrainService.create(train)

    return train_new


@router.get('/{train_id}', response_model=schemas.TrainOut)
async def get_by_id(
    train_id: int, user: schemas.UserOut = Depends(utils.get_current_user)
) -> schemas.TrainOut:
    train = await TrainService.find_by_id(train_id)

    if not train:
        raise EntityNotFound()

    await HistoryService.add_train(user.id, train.id)

    return train
