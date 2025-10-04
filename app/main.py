from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.api import router
from app.core.config import settings
from app.core.database import db_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db_manager.init_pool()
    yield
    # Shutdown
    await db_manager.close_pool()


app = FastAPI(title="Libro Könyvtár API", description="SZTE Felhő és DevOps alkalmazásai - Könyvtár kezelő rendszer", version="1.0.0", lifespan=lifespan)

app.include_router(router, prefix=settings.API_PREFIX)
