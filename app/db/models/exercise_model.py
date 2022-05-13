from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.db.models.train_model import train_exercise_table

exercise_muscle_table = Table(
    'muscles_exercises',
    Base.metadata,
    Column('muscle_id', ForeignKey('muscle.id'), primary_key=True),
    Column('exercise_id', ForeignKey('exercise.id'), primary_key=True),
)


class Exercise(Base):
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    video_link = Column(String, nullable=True)

    muscles = relationship(
        'Muscle',
        secondary=exercise_muscle_table,
        lazy='subquery',
        back_populates='exercises',
    )

    trains = relationship(
        'Train',
        secondary=train_exercise_table,
        lazy='subquery',
        back_populates='exercises',
    )

    def __repr__(self) -> str:
        return f'exercise: {self.name}'
