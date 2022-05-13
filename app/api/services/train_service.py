from typing import Optional

from sqlalchemy import select

from app.db import create_session, models, schemas


class TrainService:
    @staticmethod
    async def find_all() -> list[schemas.TrainOut]:
        async with create_session(expire_on_commit=False) as session:
            trains = (await session.scalars(select(models.Train))).all()

            return [schemas.TrainOut.from_orm(train) for train in trains]

    @staticmethod
    async def create(train: schemas.TrainCreate) -> schemas.TrainOut:
        async with create_session(expire_on_commit=False) as session:
            train_new = models.Train(
                name=train.name,
                description=train.description,
                difficulty=train.difficulty,
                duration=train.duration,
            )

            train_new.exercises = (
                await session.scalars(
                    select(models.Exercise).where(
                        models.Exercise.id.in_(train.exercises_id)
                    )
                )
            ).all()

            session.add(train_new)
            await session.commit()

            return schemas.TrainOut.from_orm(train_new)

    @staticmethod
    async def find_by_id(train_id: int) -> Optional[schemas.TrainOut]:
        async with create_session(expire_on_commit=False) as session:
            train = (
                await session.execute(
                    select(models.Train).filter(models.Train.id == train_id)
                )
            ).scalar()

            if train:
                train = schemas.TrainOut.from_orm(train)

        return train

    @staticmethod
    async def find_by_name(train_name: str) -> Optional[schemas.TrainOut]:
        async with create_session(expire_on_commit=False) as session:
            train = (
                await session.execute(
                    select(models.Train).filter(models.Train.name == train_name)
                )
            ).scalar()

            if train:
                train = schemas.TrainOut.from_orm(train)

        return train
