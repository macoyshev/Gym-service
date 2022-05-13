from datetime import datetime
from typing import Optional

from sqlalchemy import select

from app.db import create_session, models, schemas


class HistoryService:
    @staticmethod
    async def add_train(user_id: int, train_id: int) -> None:
        async with create_session(expire_on_commit=False) as session:
            history = (
                await session.scalars(
                    select(models.History).filter(models.History.user_id == user_id)
                )
            ).first()

            train_day = (
                await session.scalars(
                    select(models.TrainDay).filter(
                        models.TrainDay.date == datetime.utcnow().date(),
                    )
                )
            ).first()

            train_count = (
                await session.scalars(
                    select(models.TrainCount).filter(
                        models.TrainCount.train_id == train_id,
                    )
                )
            ).first()

            if not history:
                history = models.History(user_id=user_id)
                session.add(history)

            if not train_day:
                train_day = models.TrainDay(history_id=history.id)
                history.train_days.append(train_day)
                session.add(train_day)

            if not train_count:
                train_count = models.TrainCount(train_id=train_id)
                train_day.train_counts.append(train_count)
                session.add(train_count)
            else:
                train_count.count += 1

            await session.commit()

    @staticmethod
    async def find_user_history(user_id: int) -> Optional[schemas.HistoryOut]:
        async with create_session(expire_on_commit=False) as session:
            history = (
                await session.scalars(
                    select(models.History).filter(models.History.user_id == user_id)
                )
            ).first()

            if history:
                history = schemas.HistoryOut.from_orm(history)

            return history
