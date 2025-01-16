from pydantic import EmailStr, SecretStr, model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DATABASE_URL: str = None

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    SECRET_KEY: str
    ALGORITHM: str

    SALT: str

    REDIS_HOST: str
    REDIS_PORT: int

    EMAIL_USERNAME: str
    EMAIL_PASSWORD: SecretStr
    EMAIL_FROM: EmailStr
    EMAIL_PORT: int
    EMAIL_SERVER: str

    @model_validator(mode="before")
    @classmethod
    def get_database_url(cls, values):
        values["DATABASE_URL"] = (
            f"postgresql+asyncpg://{values['DB_USER']}:{values['DB_PASS']}@{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}"
        )
        return values

    class Config:
        env_file = ".env"


settings = Settings()
