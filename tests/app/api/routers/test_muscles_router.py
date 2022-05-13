from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_fetch(client, muscle_branch, token):
    res = client.get('/muscles/', headers={'Authorization': f'Bearer {token}'})
    msls = res.json()

    assert res.status_code == HTTPStatus.OK
    assert len(msls) == len(muscle_branch)
    assert msls[0]['name'] == muscle_branch[0].name


@pytest.mark.asyncio
async def test_create(client, token, muscle_schema):
    res = client.post(
        '/muscles/',
        json=muscle_schema.dict(),
        headers={'Authorization': f'Bearer {token}'},
    )
    msl_new = res.json()

    assert res.status_code == HTTPStatus.CREATED
    assert msl_new
    assert msl_new['name'] == muscle_schema.name


@pytest.mark.asyncio
async def test_get(client, muscle, token):
    res = client.get(
        f'/muscles/{muscle.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert res.status_code == HTTPStatus.OK
    assert res.json()['name'] == muscle.name


@pytest.mark.asyncio
async def test_update(client, muscle, token, muscle_schema):
    res = client.put(
        f'/muscles/{muscle.id}',
        json=muscle_schema.dict(),
        headers={'Authorization': f'Bearer {token}'},
    )
    msl_new = res.json()

    assert msl_new['name'] == muscle_schema.name
    assert res.status_code == HTTPStatus.OK
