from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.orm import declarative_base, declared_attr


class BaseTable:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()  # type: ignore  #pylint: disable=E1101

    id = Column(Integer, primary_key=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


Base = declarative_base(cls=BaseTable)
