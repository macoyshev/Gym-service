from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import (
    auth_router,
    exercises_router,
    muscles_router,
    train_router,
    users_router,
)


def create_api() -> FastAPI:
    app = FastAPI()

    app.add_middleware(CORSMiddleware, allow_origins='http://localhost:3000/')

    app.include_router(users_router.router)
    app.include_router(exercises_router.router)
    app.include_router(muscles_router.router)
    app.include_router(auth_router.router)
    app.include_router(train_router.router)

    return app
