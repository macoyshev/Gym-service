import pytest

from app.api.services import UserService


@pytest.mark.asyncio
async def test_create_user(user_schema):
    user_new = await UserService.create(user_schema)

    assert user_new.username == user_schema.username
    assert not hasattr(user_new, 'password')


@pytest.mark.asyncio
async def test_find_user_by_name(user):
    user_found = await UserService.find_by_name(user.username)

    assert user_found
    assert user_found.username == user.username
    assert not hasattr(user_found, 'password')


@pytest.mark.asyncio
async def test_find_user_with_password(user):
    user_found = await UserService.find_with_password(user.username)

    assert user_found
    assert user_found.username == user.username
    assert user_found.password == user.password


@pytest.mark.asyncio
async def test_add_train(train, user):
    user_with_trains = await UserService.add_train(user.id, train.id)

    assert user_with_trains.trains
    assert len(user_with_trains.trains) == 1
    assert user_with_trains.trains
    assert user_with_trains.trains[0].name == train.name
