from typing import Annotated, AsyncGenerator

import asyncpg
from fastapi import Depends, HTTPException

from app.core.database import db_manager


async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
    pool = db_manager.pool

    if not pool:
        raise HTTPException(status_code=503, detail="Database pool not initialized")

    async with pool.acquire() as connection:
        yield connection


DatabaseDep = Annotated[asyncpg.Connection, Depends(get_db)]
