from datetime import datetime

from sqlalchemy import Column, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class TrainCount(Base):
    count = Column(Integer, default=1)
    train_id = Column(Integer, ForeignKey('train.id'))
    train_day_id = Column(Integer, ForeignKey('trainday.id'))

    train = relationship('Train', lazy='subquery')

    def __repr__(self) -> str:
        return f'train_count: {self.count} - {self.train}'


class TrainDay(Base):
    date = Column(Date, default=datetime.utcnow().date())
    history_id = Column(Integer, ForeignKey('history.id'))
    train_counts = relationship(
        'TrainCount',
        uselist=True,
        lazy='subquery',
    )

    def __repr__(self) -> str:
        return f'train_day: {self.date}'


class History(Base):
    train_days = relationship('TrainDay', uselist=True, lazy='subquery')

    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'history: {self.id} of user: {self.user_id}'
