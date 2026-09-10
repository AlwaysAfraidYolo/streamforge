import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text
from starlette.concurrency import run_in_threadpool

from app.config import Settings
from app.db.session import make_engine
from app.storage import make_s3


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    app.state.settings = settings
    app.state.engine = make_engine(settings)
    app.state.s3 = make_s3(settings)
    try:
        yield
    finally:
        await app.state.engine.dispose()
        app.state.s3.close()


app = FastAPI(title="StreamForge", version="0.1.0", lifespan=lifespan)


@app.get("/live", tags=["Infrastructure"])
async def live():
    return {"status": "alive"}


@app.get("/ready", tags=["Infrastructure"])
async def ready(request: Request):
    checks = {}
    try:
        async with asyncio.timeout(4):
            async with request.app.state.engine.connect() as connection:
                await connection.execute(text("SELECT 1"))
        checks["postgres"] = "ok"
    except Exception:
        checks["postgres"] = "unavailable"
    try:
        await run_in_threadpool(
            request.app.state.s3.head_bucket,
            Bucket=request.app.state.settings.s3_bucket,
        )
        checks["s3"] = "ok"
    except Exception:
        checks["s3"] = "unavailable"
    return JSONResponse(
        {
            "status": "ready" if all(v == "ok" for v in checks.values()) else "not_ready",
            "checks": checks,
        },
        status_code=200 if all(v == "ok" for v in checks.values()) else 503,
    )
