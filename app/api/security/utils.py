from datetime import datetime, timedelta
from typing import Optional, Union

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.api.exceptions import InvalidCredentials
from app.api.services import UserService
from app.configs import settings
from app.db.schemas import TokenData, UserDB, UserOut

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str) -> Optional[UserDB]:
    user = await UserService.find_with_password(username)

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user


def create_access_token(
    data: dict[str, Union[str, datetime]], expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm.get_secret_value(),
    )

    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm.get_secret_value()],
        )
        username: str = payload.get('sub')

        if username is None:
            raise InvalidCredentials()

        token_data = TokenData(username=username)

    except JWTError as ex:
        raise InvalidCredentials from ex

    user = None
    if token_data.username:
        user = await UserService.find_by_name(username=token_data.username)

    if user is None:
        raise InvalidCredentials()

    return user
