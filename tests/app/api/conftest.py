from typing import Optional, SupportsIndex

import pytest

from app.db import factories, schemas
from app.db.models.train_model import Difficulty


@pytest.fixture
def user():
    _user = factories.UserFactory()

    return _user


@pytest.fixture
def exercise():
    exr = factories.ExerciseFactory()

    return exr


@pytest.fixture
def muscle():
    msl = factories.MuscleFactory()

    return msl


@pytest.fixture
def train():
    _train = factories.TrainFactory()

    return _train


@pytest.fixture
def user_with_trains(size: Optional[int] = 10):
    _user = factories.UserFactory.create(trains=size)

    return _user


@pytest.fixture
def muscle_branch(size: Optional[int] = 10):
    msls = factories.MuscleFactory.create_batch(size)

    return msls


@pytest.fixture
def exercise_batch(size: Optional[int] = 10):
    exrs = factories.ExerciseFactory.create_batch(size)

    return exrs


@pytest.fixture
def train_batch(size: Optional[int] = 10):
    trains = factories.TrainFactory.create_batch(size)

    return trains


@pytest.fixture
def exercise_batch_with_muscles(size: SupportsIndex = 10):
    exrs = []
    for _ in range(size):
        msl = factories.MuscleFactory.create()
        exr = factories.ExerciseFactory.create(muscles=(msl,))
        exrs.append(exr)

    return exrs


@pytest.fixture
def exercise_schema():
    exr = schemas.ExerciseCreate(
        name='test_name', video_link='test_video_link', description='test_description'
    )

    return exr


@pytest.fixture
def muscle_schema():
    msl = schemas.MuscleCreate(name='test_msl')

    return msl


@pytest.fixture
def user_schema():
    _user = schemas.UserCreate(username='test_username', password='test_password')

    return _user


@pytest.fixture
def train_schema():
    _train = schemas.TrainCreate(
        name='test_name',
        description='test_description',
        difficulty=Difficulty.NORMAL,
    )

    return _train
