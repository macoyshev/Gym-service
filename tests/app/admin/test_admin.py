from http import HTTPStatus


def test_access(admin_client):
    res = admin_client.get('/admin/')

    assert res.status_code == HTTPStatus.OK
