from fastapi import FastAPI

from app.api import create_api
from app.db import create_db


async def on_startup() -> None:
    await create_db()


def create_app() -> FastAPI:
    _api = create_api()
    _api.add_event_handler('startup', on_startup)

    return _api
