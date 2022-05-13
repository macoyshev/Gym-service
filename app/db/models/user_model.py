from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.db.models.train_model import train_user_table


class User(Base):
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String, nullable=False)

    trains = relationship(
        'Train',
        secondary=train_user_table,
        lazy='subquery',
        back_populates='users',
    )

    def __repr__(self) -> str:
        return f'user: {self.username}'
