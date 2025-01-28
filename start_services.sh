#!/bin/bash

# 1. Запуск Docker (Redis и PostgreSQL)
docker-compose -f docker-compose.yml up -d

# 2. Сборка и запуск фронтенда
cd frontend
npm install
npm run build
sudo nginx -c /nginx.conf

# 3. Установка окружения и запуск бэкенда
cd ../backend
python3.9 -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
alembic upgrade head
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
