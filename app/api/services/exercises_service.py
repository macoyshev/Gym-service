from typing import Optional

from sqlalchemy import select

from app.db import create_session, models, schemas


class ExercisesService:
    @staticmethod
    async def find_all(
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[schemas.ExerciseOut]:
        async with create_session(expire_on_commit=False) as session:
            statement = select(models.Exercise)

            if limit:
                statement = statement.offset(offset)

            if offset:
                statement = statement.limit(limit)

            exercises = (await session.scalars(statement)).all()

        return [schemas.ExerciseOut.from_orm(exr) for exr in exercises]

    @staticmethod
    async def create(exr: schemas.ExerciseCreate) -> schemas.ExerciseOut:
        async with create_session(expire_on_commit=False) as session:
            exr_new = models.Exercise(
                name=exr.name, description=exr.description, video_link=exr.video_link
            )

            exr_new.muscles = (
                await session.scalars(
                    select(models.Muscle).where(models.Muscle.id.in_(exr.muscles_id))
                )
            ).all()

            session.add(exr_new)
            await session.commit()

            return schemas.ExerciseOut.from_orm(exr_new)

    @staticmethod
    async def find_by_name(exr_name: str) -> Optional[schemas.ExerciseOut]:
        async with create_session(expire_on_commit=False) as session:
            res = await session.execute(
                select(models.Exercise).filter(models.Exercise.name == exr_name)
            )

            exr = res.scalar()

            if exr:
                exr = schemas.ExerciseOut.from_orm(exr)

        return exr

    @staticmethod
    async def find_by_id(exr_id: int) -> Optional[schemas.ExerciseOut]:
        async with create_session(expire_on_commit=False) as session:
            res = await session.execute(
                select(models.Exercise).filter(models.Exercise.id == exr_id)
            )
            exr = res.scalar()

            if exr:
                exr = schemas.ExerciseOut.from_orm(exr)

        return exr

    @staticmethod
    async def delete(exr_id: int) -> None:
        async with create_session() as session:
            res = await session.execute(
                select(models.Exercise).filter(models.Exercise.id == exr_id)
            )
            exr = res.scalar()

            await session.delete(exr)

    @staticmethod
    async def update(
        exr_id: int, exr_upd: schemas.ExerciseCreate
    ) -> schemas.ExerciseOut:
        async with create_session(expire_on_commit=False) as session:
            res = await session.execute(
                select(models.Exercise).filter(models.Exercise.id == exr_id)
            )
            exr = res.scalar()

            exr.name = exr_upd.name
            exr.description = exr_upd.description
            exr.video_link = exr_upd.video_link
            exr.muscles = (
                await session.scalars(
                    select(models.Muscle).filter(
                        models.Muscle.id.in_(exr_upd.muscles_id)
                    )
                )
            ).all()

            return schemas.ExerciseOut.from_orm(exr)
