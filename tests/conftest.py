import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from app.admin import create_admin
from app.api import create_api
from app.db import clear_db, create_db


@pytest_asyncio.fixture(autouse=True)
async def _init_db():
    await create_db()
    yield
    await clear_db()


@pytest.fixture
def client():
    _client = TestClient(create_api())
    return _client


@pytest.fixture
def admin_client():
    _client = create_admin()

    _client.config.update(
        {
            'TESTING': True,
        }
    )

    return _client.test_client()
