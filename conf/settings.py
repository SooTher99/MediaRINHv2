from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, PostgresDsn, validator
import os

class Settings(BaseSettings):
    """
    FastAPI settings for MediaRINH project.
    """
    #######################################################################################
    """BASE SETTINGS"""
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = 'MediaRINH'
    SECRET_KEY: str = 'breGveVA3G4MHuD,Ow7Tc^2ACymwik7y3r:(0^-u.ISOG@!q?J5W9irM$TlKflkt'
    #######################################################################################
    """AUTH SETTINGS"""
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    #######################################################################################
    """CORS SETTINGS"""
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    CORS_ALLOW_METHODS: List[str] = [
        "DELETE",
        "GET",
        "OPTIONS",
        "PATCH",
        "POST",
        "PUT",
    ]
    CORS_ALLOW_HEADERS: List[str] = [
        "accept",
        "accept-encoding",
        "authorization",
        "content-type",
        "dnt",
        "origin",
        "user-agent",
        "x-csrftoken",
        "x-requested-with",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Credentials",
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    #######################################################################################
    """TEMPLATES SETTINGS"""
    TEMPLATES_DIR: Path = 'templates'

    @validator("TEMPLATES_DIR", pre=True)
    def get_templates_dir(cls, v: Optional[Path], values: Dict[str, Any]):
        return values.get("BASE_DIR").joinpath(v)

    #######################################################################################
    """DATABASE SETTINGS"""
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    #######################################################################################
    """SMTP SETTINGS"""
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )
    #######################################################################################
    """MEDIA SETTINGS"""

    MEDIA_DIR: Path = 'media'

    os.makedirs(BASE_DIR.joinpath(MEDIA_DIR), 0o777, exist_ok=True)

    @validator("MEDIA_DIR", pre=True)
    def get_media_dir(cls, v: Optional[Path], values: Dict[str, Any]):
        return values.get("BASE_DIR").joinpath(v)


    class Config:
        case_sensitive = True
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()