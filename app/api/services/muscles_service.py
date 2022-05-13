from typing import Optional

from sqlalchemy.future import select

from app.db import create_session, models, schemas


class MuscleService:
    @staticmethod
    async def find_all(
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[schemas.MuscleOut]:
        async with create_session(expire_on_commit=False) as session:
            statement = select(models.Muscle)

            if limit:
                statement = statement.offset(offset)

            if offset:
                statement = statement.limit(limit)

            muscles = (await session.scalars(statement)).all()

            return [schemas.MuscleOut.from_orm(msl) for msl in muscles]

    @staticmethod
    async def create(muscle: schemas.MuscleCreate) -> schemas.MuscleOut:
        async with create_session(expire_on_commit=False) as session:
            msl_new = models.Muscle(name=muscle.name)

            msl_new.exercises = (
                await session.scalars(
                    select(models.Exercise).where(
                        models.Exercise.id.in_(muscle.exercises_id)
                    )
                )
            ).all()

            session.add(msl_new)
            await session.commit()

            return schemas.MuscleOut.from_orm(msl_new)

    @staticmethod
    async def find_by_id(muscle_id: int) -> Optional[schemas.MuscleOut]:
        async with create_session(expire_on_commit=False) as session:
            msl = (
                await session.scalars(
                    select(models.Muscle).filter(models.Muscle.id == muscle_id)
                )
            ).first()

            if msl:
                msl = schemas.MuscleOut.from_orm(msl)

        return msl

    @staticmethod
    async def update(msl_id: int, msl_upd: schemas.MuscleCreate) -> schemas.MuscleOut:
        async with create_session(expire_on_commit=False) as session:
            msl = (
                await session.execute(
                    select(models.Muscle).filter(models.Muscle.id == msl_id)
                )
            ).scalar()

            msl.name = msl_upd.name

            if msl_upd.exercises_id:
                msl.exercises = (
                    await session.scalars(
                        select(models.Exercise).filter(
                            models.Exercise.id.in_(msl_upd.exercises_id)
                        )
                    )
                ).all()

            return schemas.MuscleOut.from_orm(msl)

    @staticmethod
    async def find_by_name(msl_name: str) -> Optional[schemas.MuscleOut]:
        async with create_session(expire_on_commit=False) as session:
            msl = (
                await session.scalars(
                    select(models.Muscle).filter(models.Muscle.name == msl_name)
                )
            ).first()

            if msl:
                msl = schemas.MuscleOut.from_orm(msl)

        return msl
