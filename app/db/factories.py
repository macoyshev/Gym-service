from typing import Any

import factory

from app.api.security.utils import get_password_hash
from app.db import Session, models


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = Session(expire_on_commit=False)
        sqlalchemy_session_persistence = 'commit'

    id = factory.Sequence(lambda n: n)


class MuscleFactory(BaseFactory):
    class Meta:
        model = models.Muscle

    name = factory.Sequence(lambda n: f'test_msl_{n}')


class ExerciseFactory(BaseFactory):
    class Meta:
        model = models.Exercise

    name = factory.Sequence(lambda n: f'test_exr_{n}')


class TrainFactory(BaseFactory):
    class Meta:
        model = models.Train

    name = factory.Sequence(lambda n: f'test_train_{n}')


class UserFactory(BaseFactory):
    class Meta:
        model = models.User

    username = factory.Sequence(lambda n: f'test_user_{n}')
    password = get_password_hash('test_password')

    @factory.post_generation
    def trains(self, create: Any, extracted: int, **kwargs: Any) -> None:
        """
        stores n - 1 trains in the database
        """
        if not create:
            return

        if extracted:
            for _ in range(extracted):
                train = TrainFactory.create(**kwargs)
                self.trains.append(train)  # pylint: disable=no-member
