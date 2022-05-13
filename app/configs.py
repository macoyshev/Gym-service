from typing import Optional

from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    db_uri: Optional[str] = 'sqlite+aiosqlite:///tests/app/db/test_db.db'
    db_uri_sync: Optional[str] = 'sqlite:///tests/app/db/test_db.db'

    admin_key: Optional[str] = 'admin key'

    secret_key: SecretStr = SecretStr('secret key')
    algorithm: SecretStr = SecretStr('HS256')
    token_ttl: int = 30

    class Config:
        case_sensitive = False


settings = Settings()
