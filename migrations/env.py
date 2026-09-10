import asyncio

from alembic import context

from app.config import Settings
from app.db.session import Base, make_engine


def migrations(connection):
    context.configure(connection=connection, target_metadata=Base.metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run():
    engine = make_engine(Settings())
    async with engine.connect() as connection:
        await connection.run_sync(migrations)
    await engine.dispose()


if context.is_offline_mode():
    raise RuntimeError("Use online migrations in this starter")
asyncio.run(run())
