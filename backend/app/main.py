from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from app.users.router import router as users_router
from app.posts.router import router as posts_router
from app.donations.router import router as donations_router
from app.mailer.router import router as mailer_router
from app.skins.router import router as skins_router
from app.config import settings
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(lifespan=lifespan)


TEMPLATES_PATH = Path("app/templates")


app.include_router(users_router, prefix="/api")
app.include_router(posts_router, prefix="/api")
app.include_router(donations_router, prefix="/api")
app.include_router(mailer_router, prefix="/api")
app.include_router(skins_router, prefix="/api")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:5173",
    "http://localhost:8000",
    "https://tortugagot.com",
    "https://www.tortugagot.com",
]
# test
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)
app.add_middleware(HTTPSRedirectMiddleware)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
