from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_fetch(client, exercise_batch, token):
    res = client.get('/exercises/', headers={'Authorization': f'Bearer {token}'})
    exercises = res.json()

    assert res.status_code == HTTPStatus.OK
    assert len(exercises) == len(exercise_batch)
    assert exercises[0]['name'] == exercise_batch[0].name


@pytest.mark.asyncio
async def test_create(client, token):
    res = client.post(
        '/exercises/',
        json={'name': 'test'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert res.status_code == HTTPStatus.CREATED
    assert res.json()['name'] == 'test'


@pytest.mark.asyncio
async def test_create_existing(client, exercise, token):
    res = client.post(
        '/exercises/',
        json={'name': exercise.name},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert res.status_code == HTTPStatus.CONFLICT


@pytest.mark.asyncio
async def test_get(client, exercise, token):
    res = client.get(
        f'/exercises/{exercise.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert res.status_code == HTTPStatus.OK
    assert res.json()['name'] == exercise.name


@pytest.mark.asyncio
async def test_delete(client, exercise, token):
    res = client.delete(
        f'/exercises/{exercise.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert res.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_update(client, exercise, token):
    new_name = 'new_name'
    res = client.put(
        f'/exercises/{exercise.id}',
        json={'name': new_name},
        headers={'Authorization': f'Bearer {token}'},
    )
    exr_upd = res.json()

    assert exr_upd
    assert exr_upd['name'] == new_name
    assert exr_upd['id'] == exercise.id
    assert exr_upd['name'] != exercise.name
    assert res.status_code == HTTPStatus.OK
