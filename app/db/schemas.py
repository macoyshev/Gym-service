from datetime import date, time
from typing import Optional

from pydantic import BaseModel

from app.db.models.train_model import Difficulty


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class TrainBase(BaseModel):
    name: str
    description: Optional[str]
    difficulty: Optional[Difficulty]
    duration: Optional[time]

    class Config:
        orm_mode = True
        use_enum_values = True


class ExerciseBase(BaseModel):
    name: str
    video_link: Optional[str]
    description: Optional[str]


class MuscleBase(BaseModel):
    name: str


class Exercise(ExerciseBase):
    id: int

    class Config:
        orm_mode = True


class Muscle(MuscleBase):
    id: int

    class Config:
        orm_mode = True


class Train(TrainBase):
    id: int

    class Config:
        orm_mode = True


class UserOut(UserBase):
    id: int
    trains: Optional[list[Train]]

    class Config:
        orm_mode = True


class UserDB(UserOut):
    password: str


class ExerciseOut(Exercise):
    muscles: Optional[list[Muscle]]


class MuscleOut(Muscle):
    exercises: Optional[list[Exercise]]


class TrainOut(Train):
    exercises: Optional[list[Exercise]]


class ExerciseCreate(ExerciseBase):
    muscles_id: Optional[list[int]] = []


class MuscleCreate(MuscleBase):
    exercises_id: Optional[list[int]] = []


class TrainCreate(TrainBase):
    exercises_id: Optional[list[int]] = []


class TrainCount(BaseModel):
    count: int
    train: TrainBase

    class Config:
        orm_mode = True


class TrainDayOut(BaseModel):
    date: date
    train_counts: Optional[list[TrainCount]]

    class Config:
        orm_mode = True


class HistoryOut(BaseModel):
    user_id: int
    train_days: Optional[list[TrainDayOut]]

    class Config:
        orm_mode = True
