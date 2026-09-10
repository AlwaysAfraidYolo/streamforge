"""Create local credentials once; never overwrite existing .env."""

import secrets
from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / ".env"
if path.exists():
    print(".env already exists; kept unchanged")
else:
    values = {
        "POSTGRES_PASSWORD": secrets.token_hex(24),
        "S3_ACCESS_KEY": "streamforge",
        "S3_SECRET_KEY": secrets.token_hex(24),
        "CLICKHOUSE_PASSWORD": secrets.token_hex(24),
        "AIRFLOW_DB_PASSWORD": secrets.token_hex(24),
        "AIRFLOW_API_SECRET": secrets.token_hex(32),
    }
    with path.open("x") as file:
        file.write("".join(f"{key}={value}\n" for key, value in values.items()))
    path.chmod(0o600)
    print("Created .env with local credentials")
