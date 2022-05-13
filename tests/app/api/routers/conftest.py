from datetime import timedelta

import pytest

from app.api.security.utils import create_access_token
from app.configs import settings


@pytest.fixture
def token(user):
    access_token_expires = timedelta(minutes=settings.token_ttl)
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )

    return access_token


@pytest.fixture
def token_for_user_with_train(user_with_trains):
    access_token_expires = timedelta(minutes=settings.token_ttl)
    access_token = create_access_token(
        data={'sub': user_with_trains.username}, expires_delta=access_token_expires
    )

    return access_token
