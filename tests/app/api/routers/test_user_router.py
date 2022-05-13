from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_create(client, user_schema):
    res = client.post('/users/', json=user_schema.dict())
    user_new = res.json()

    assert res.status_code == HTTPStatus.OK
    assert user_new['username'] == user_schema.username
    assert not hasattr(user_new, 'password')


@pytest.mark.asyncio
async def test_get_user(client, user, token):
    res = client.get('/users/me', headers={'Authorization': f'Bearer {token}'})
    user_found = res.json()

    assert res.status_code == HTTPStatus.OK
    assert user_found
    assert user_found['username'] == user.username
