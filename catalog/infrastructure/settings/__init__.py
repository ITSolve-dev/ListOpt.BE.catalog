from functools import cache
from typing import Literal

from pydantic import Field, computed_field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    PyprojectTomlConfigSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

LOG_LEVEL_TYPE = Literal[
    "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "TRACE"
]


class ServerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        yaml_file="config.yml",
        yaml_config_section="server",
        yaml_file_encoding="utf-8",
    )
    host: str = Field(default="0.0.0.0", description="Host for server")
    port: int = Field(default=8000, description="Port for server")
    reload: bool = Field(default=True, description="Reload server")
    workers: int = Field(default=1, description="Workers for server")
    root_path: str = Field(default="", description="Root path for server")
    root_path_in_servers: bool = Field(
        default=True, description="Root path in servers"
    )
    prefix: str = Field(default="", description="Prefix for server")
    allow_origins: list[str] = Field(
        default=["*"], description="Allow hostnames for requests"
    )
    allow_credentials: bool = Field(
        default=True, description="Allow credentials for requests"
    )
    allow_methods: list[str] = Field(
        default=["*"], description="Allow methods for requests"
    )
    allow_headers: list[str] = Field(
        default=["*"], description="Allow headers for requests"
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            YamlConfigSettingsSource(settings_cls),
        )


class ProjectSettings(BaseSettings):
    model_config = SettingsConfigDict(
        pyproject_toml_table_header=("project",), extra="ignore"
    )
    name: str = Field(default="project_name", description="Project name")
    version: str = Field(default="0.1.0", description="Project version")
    description: str = Field(default="", description="Project description")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (PyprojectTomlConfigSettingsSource(settings_cls),)


class JwtSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="JWT__",
        env_file_encoding="utf-8",
        yaml_file="config.yml",
        yaml_config_section="jwt",
        yaml_file_encoding="utf-8",
    )
    access_token_lifetime: int = Field(
        default=15, description="Expiration access token in minutes"
    )
    refresh_token_lifetime: int = Field(
        default=30, description="Expiration refresh token in days"
    )
    SIGNING_KEY: str = Field(
        default="secret", description="Secret key of sign of jwt"
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
            env_settings,
        )


class PermissionsSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PERMISSIONS__",
        yaml_file="config.yml",
        yaml_config_section="permissions",
        yaml_file_encoding="utf-8",
    )
    model: str = Field(default="permissions_model.conf")
    policy: str = Field(default="policy.csv")
    log: bool = False
    URL: str = Field(default="http://localhost:8004/permissions")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
            env_settings,
        )


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DATABASE__",
        env_file_encoding="utf-8",
        yaml_file="config.yml",
        yaml_config_section="db",
        yaml_file_encoding="utf-8",
    )
    HOST: str = Field(
        default="localhost",
        description="Database host",
    )
    PORT: int = Field(
        default=5432,
        description="Database port",
    )
    USER: str = Field(
        default="postgres",
        description="Database user",
    )
    PASSWORD: str = Field(
        default="postgres",
        description="Database password",
    )
    NAME: str = Field(
        default="db",
        description="Database name",
    )
    log: bool = Field(
        default=False,
        description="Log ORM queries",
    )
    pool_size: int = Field(default=10, description="Database pool size")
    max_overflow: int = Field(default=5, description="Database max overflow")

    @computed_field
    @property
    def URL(self) -> str:  # noqa: N802
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
            env_settings,
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    server: ServerSettings = Field(default_factory=ServerSettings)
    project: ProjectSettings = Field(default_factory=ProjectSettings)
    jwt: JwtSettings = Field(default_factory=JwtSettings)
    permissions: PermissionsSettings = Field(
        default_factory=PermissionsSettings
    )


@cache
def get_settings() -> Settings:
    from dotenv import load_dotenv

    load_dotenv()
    return Settings()
