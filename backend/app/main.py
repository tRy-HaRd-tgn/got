from fastapi import FastAPI
from app.users.router import router as users_router
from app.posts.router import router as posts_router
from app.donations.router import router as donations_router
from app.mailer.router import router as mailer_router
from app.config import settings

app = FastAPI()


app.include_router(users_router)
app.include_router(posts_router)
app.include_router(donations_router)
app.include_router(mailer_router)
