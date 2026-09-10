"""Exercise infrastructure using disposable records, not business data."""

import argparse
import asyncio
from uuid import uuid4

import httpx
from redis.asyncio import Redis
from sqlalchemy import text

from app.config import Settings
from app.db.session import make_engine
from app.storage import make_s3


async def main(analytics=False):
    settings = Settings()
    engine = make_engine(settings)
    try:
        async with engine.connect() as conn:
            async with conn.begin():
                await conn.execute(
                    text("CREATE TEMP TABLE sf_smoke (value INTEGER) ON COMMIT DROP")
                )
                await conn.execute(text("INSERT INTO sf_smoke VALUES (42)"))
                assert (await conn.execute(text("SELECT value FROM sf_smoke"))).scalar_one() == 42
        print("PASS PostgreSQL write/read")
    finally:
        await engine.dispose()
    redis = Redis.from_url(settings.redis_url, socket_timeout=3)
    key = f"smoke:{uuid4()}"
    try:
        await redis.set(key, "ok", ex=30)
        assert await redis.get(key) == b"ok"
        print("PASS Redis write/read")
    finally:
        await redis.delete(key)
        await redis.aclose()
    s3 = make_s3(settings)
    key = f"_smoke/{uuid4()}.txt"
    try:
        s3.put_object(Bucket=settings.s3_bucket, Key=key, Body=b"streamforge")
        body = s3.get_object(Bucket=settings.s3_bucket, Key=key)["Body"]
        try:
            assert body.read() == b"streamforge"
        finally:
            body.close()
        print("PASS S3 write/read")
    finally:
        s3.delete_object(Bucket=settings.s3_bucket, Key=key)
        s3.close()
    if analytics:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                settings.clickhouse_url,
                content="SELECT 1",
                auth=("streamforge", settings.clickhouse_password.get_secret_value()),
            )
            response.raise_for_status()
            assert response.text.strip() == "1"
        print("PASS ClickHouse query")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--analytics", action="store_true")
    asyncio.run(main(parser.parse_args().analytics))
