from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from app.users.router import router as users_router
from app.posts.router import router as posts_router
from app.donations.router import router as donations_router
from app.mailer.router import router as mailer_router
from app.config import settings
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

TEMPLATES_PATH = Path("app/templates")


app.include_router(users_router)
app.include_router(posts_router)
app.include_router(donations_router)
app.include_router(mailer_router)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Чтение HTML-файла
    with open(TEMPLATES_PATH / "index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())
