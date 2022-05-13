from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_create(client, train_schema, token):
    res = client.post(
        '/trains/',
        json=train_schema.dict(),
        headers={'Authorization': f'Bearer {token}'},
    )
    train_new = res.json()

    assert res.status_code == HTTPStatus.CREATED
    assert train_new
    assert train_new['name'] == train_schema.name
    assert train_new['description'] == train_schema.description
    assert train_new['difficulty'] == train_schema.difficulty


@pytest.mark.asyncio
async def test_fetch(client, token, train_batch):
    res = client.get('/trains/', headers={'Authorization': f'Bearer {token}'})
    trains = res.json()

    assert res.status_code == HTTPStatus.OK
    assert trains
    assert len(trains) == len(train_batch)
    assert trains[0]['name'] == train_batch[0].name
    assert trains[0]['description'] == train_batch[0].description


# @pytest.mark.asyncio
# async def test_get_by_id(client, token, train):
#     res = client.get(
#         f'/trains/{train.id}', headers={'Authorization': f'Bearer {token}'}
#     )
#     train_found = res.json()
#
#     assert res.status_code == HTTPStatus.OK
#     assert train_found['name'] == train.name
#     assert train_found['description'] == train.description
#     assert train_found['difficulty'] == train.difficulty
