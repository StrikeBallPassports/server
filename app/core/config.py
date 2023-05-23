from typing import List, Union, Any

from pydantic import AnyHttpUrl, BaseSettings, validator, PostgresDsn


class Settings(BaseSettings):
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v

        raise ValueError(v)

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    DATABASE_URI: PostgresDsn | None = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120000

    TIME_ZONE = 'Asia/Vladivostok'

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
