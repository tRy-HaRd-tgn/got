#!/bin/bash

# Применяем миграции
alembic upgrade head

# Запускаем FastAPI через Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000