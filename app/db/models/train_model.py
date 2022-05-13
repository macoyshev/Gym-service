import enum

from sqlalchemy import Column, Enum, ForeignKey, String, Table, Time
from sqlalchemy.orm import relationship

from app.db.models.base import Base

train_exercise_table = Table(
    'train_exercise',
    Base.metadata,
    Column('train_id', ForeignKey('train.id'), primary_key=True),
    Column('exercise_id', ForeignKey('exercise.id'), primary_key=True),
)


train_user_table = Table(
    'train_user',
    Base.metadata,
    Column('train_id', ForeignKey('train.id'), primary_key=True),
    Column('user_id', ForeignKey('user.id'), primary_key=True),
)


class Difficulty(str, enum.Enum):
    EASY = 'easy'
    NORMAL = 'normal'
    HARD = 'hard'


class Train(Base):
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    difficulty = Column(Enum(Difficulty), nullable=True)
    duration = Column(Time, nullable=True)

    exercises = relationship(
        'Exercise',
        secondary=train_exercise_table,
        lazy='subquery',
        back_populates='trains',
    )

    users = relationship(
        'User',
        secondary=train_user_table,
        lazy='subquery',
        back_populates='trains',
    )

    def __repr__(self) -> str:
        return f'train: {self.name}'
