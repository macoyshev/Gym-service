import pytest

from app.api.services import TrainService


@pytest.mark.asyncio
async def test_fetch_trains(train_batch):
    trains = await TrainService.find_all()

    assert len(trains) == len(train_batch)
    assert trains[0].name == train_batch[0].name
    assert trains[0].description == train_batch[0].description


@pytest.mark.asyncio
async def test_create_train(train_schema):
    train_new = await TrainService.create(train_schema)

    assert train_new
    assert train_new.name == train_schema.name
    assert train_new.description == train_schema.description
    assert train_new.duration == train_schema.duration
    assert train_new.difficulty == train_schema.difficulty


@pytest.mark.asyncio
async def test_find_by_id(train):
    train_found = await TrainService.find_by_id(train.id)

    assert train_found
    assert train_found.name == train.name
    assert train_found.description == train.description
    assert train_found.difficulty == train.difficulty


@pytest.mark.asyncio
async def test_find_by_name(train):
    train_found = await TrainService.find_by_name(train.name)

    assert train_found
    assert train_found.name == train.name
    assert train_found.description == train.description
    assert train_found.difficulty == train.difficulty
