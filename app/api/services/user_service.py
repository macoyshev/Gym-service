from typing import Optional

from sqlalchemy import select

from app.api.security import utils
from app.db import create_session, models, schemas


class UserService:
    @staticmethod
    async def find_by_id(user_id: int) -> Optional[schemas.UserOut]:
        async with create_session(expire_on_commit=False) as session:
            user = (
                await session.scalars(
                    select(models.User).filter(models.User.id == user_id)
                )
            ).first()

            if user:
                user = schemas.UserOut.from_orm(user)

            return user

    @staticmethod
    async def find_by_name(username: str) -> Optional[schemas.UserOut]:
        async with create_session(expire_on_commit=False) as session:
            user = (
                await session.scalars(
                    select(models.User).filter(models.User.username == username)
                )
            ).first()

            if user:
                user = schemas.UserOut.from_orm(user)

            return user

    @staticmethod
    async def create(user: schemas.UserCreate) -> schemas.UserOut:
        async with create_session(expire_on_commit=False) as session:
            user_new = models.User(
                username=user.username,
                password=utils.get_password_hash(user.password),
                trains=[],
            )

            session.add(user_new)
            await session.commit()

            return schemas.UserOut.from_orm(user_new)

    @staticmethod
    async def find_with_password(username: str) -> Optional[schemas.UserDB]:
        async with create_session(expire_on_commit=False) as session:
            user = (
                await session.scalars(
                    select(models.User).filter(models.User.username == username)
                )
            ).first()

            if user:
                user = schemas.UserDB.from_orm(user)

            return user

    @staticmethod
    async def add_train(user_id: int, train_id: int) -> schemas.UserOut:
        async with create_session(expire_on_commit=False) as session:
            user = (
                await session.scalars(
                    select(models.User).filter(models.User.id == user_id)
                )
            ).first()

            train = (
                await session.scalars(
                    select(models.Train).filter(models.Train.id == train_id)
                )
            ).first()

            user.trains.append(train)

            return schemas.UserOut.from_orm(user)
