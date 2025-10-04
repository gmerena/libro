import asyncpg

from app.core.config import settings


class DatabaseManager:

    def __init__(self):
        self.pool: asyncpg.Pool | None = None

    async def init_pool(self):
        print("Initializing database pool...")

        self.pool = await asyncpg.create_pool(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            min_size=settings.DB_POOL_MIN_SIZE,
            max_size=settings.DB_POOL_MAX_SIZE,
            command_timeout=60,
        )

        print("Database pool initialized")

    async def close_pool(self):
        if self.pool:
            print("Closing database pool...")
            await self.pool.close()
            print("Pool closed")


db_manager = DatabaseManager()
