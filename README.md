# Каталог книг (Book Catalog)

Сервис на FastAPI для управления каталогом книг.

## Установка
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt

## Запуск
uvicorn app_final:app --reload
Документация: http://127.0.0.1:8000/docs

## Тесты
python -m pytest -v

## Переменные окружения
APP_VERSION, MAX_BOOKS (см. .env.example)

## Диагностика
curl http://127.0.0.1:8000/health