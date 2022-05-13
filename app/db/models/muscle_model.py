from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.db.models.exercise_model import exercise_muscle_table


class Muscle(Base):
    name = Column(String, nullable=False)
    exercises = relationship(
        'Exercise',
        secondary=exercise_muscle_table,
        lazy='subquery',
        back_populates='muscles',
    )

    def __repr__(self) -> str:
        return f'muscle: {self.name}'
