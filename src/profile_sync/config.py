from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', case_sensitive=True, extra='ignore')
    APP_ENVIRONMENT: str = "development"
    SWAGGER_ENABLED: bool = True

    DATABASE_URL: SecretStr | None = None
    MAX_UPLOAD_SIZE_MB: int = Field(10, ge=1, le=50)
    MAX_IMPORT_ROWS: int = Field(10000, ge=1, le=100000)
    MAX_IMPORT_COLUMNS: int = Field(200, ge=1, le=500)
    DEFAULT_PHONE_REGION: str = 'US'
    JWT_ISSUER: str = ''
    JWT_AUDIENCE: str = ''
    PROFILE_TAG_AGENT_URL: str = ''
    FIELD_MAPPING_AGENT_URL: str = ''
    AZURE_STORAGE_ACCOUNT_URL: str = ''
    AZURE_BLOB_CONTAINER: str = ''
    AZURE_STORAGE_QUEUE_NAME: str = ''
