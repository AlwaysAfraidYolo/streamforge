from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    postgres_host: str = "127.0.0.1"
    postgres_port: int = 15432
    postgres_user: str = "streamforge"
    postgres_db: str = "streamforge"
    postgres_password: SecretStr
    redis_url: str = "redis://127.0.0.1:16379/0"
    s3_endpoint: str = "http://127.0.0.1:18333"
    s3_access_key: str
    s3_secret_key: SecretStr
    s3_bucket: str = "streamforge-raw"
    clickhouse_url: str = "http://127.0.0.1:18123"
    clickhouse_password: SecretStr = SecretStr("")
