import os
from typing import Optional

from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict
from pydantic_settings_yaml import \
    YamlBaseSettings  # type:ignore[import-untyped]

from src.enums import LogFormat

CONFIG_FILE = os.environ.get("CONFIG_FILE", "config.yml")


def get_allowed_origins() -> list[str]:
    return ["*"]


class HttpAddrSettings(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    protocol: str = "http"

    @property
    def url(self) -> str:
        return f"{self.protocol}://{self.host}:{self.port}"


class HttpInstanceSettings(BaseModel):
    addr: HttpAddrSettings
    workers: int = 1
    allowed_origins: list[str] = Field(default_factory=get_allowed_origins)


class HttpSettings(BaseModel):
    v1: HttpInstanceSettings


class DatabaseSettings(BaseModel):
    engine: str = "postgresql+asyncpg"
    user: str = "postgres"
    password: str = "password"
    host: str = "localhost"
    port: int = 5432
    database: str = "med_db"
    test_database: str = "test_med_db"
    echo: bool = False

    @property
    def url(self) -> str:
        return f"{self.engine}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def test_url(self) -> str:
        return f"{self.engine}://{self.user}:{self.password}@{self.host}:{self.port}/{self.test_database}"


class ServingSettings(BaseModel):
    http: HttpSettings


class DependsSettings(BaseModel):
    database: DatabaseSettings


class ServiceSettings(BaseModel):
    day_start: str
    day_end: str
    next_taking_period_hours: int


class LoggingSettings(BaseModel):
    sentry_dsn: Optional[str] = None
    log_level: str = "INFO"
    log_format: LogFormat = LogFormat.plain


class Settings(YamlBaseSettings):
    name: str = ""

    debug: bool = False

    serving: ServingSettings
    service: ServiceSettings
    depends: DependsSettings

    logging: LoggingSettings

    model_config = SettingsConfigDict(yaml_file=CONFIG_FILE)


settings = Settings()  # type:ignore[call-arg]
