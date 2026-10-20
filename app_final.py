import logging
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Логи
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("book_catalog")

APP_VERSION ="1.0.0"

app = FastAPI(title="Book Catalog", version=APP_VERSION)

@app.get("/")
def root():
    return {"message": "Book Catalog API. Открой /docs"}
MAX_BOOKS = int(os.getenv("MAX_BOOKS", "100"))

books: list[dict] = [
    {"id": 1, "title": "Время жить и Время умирать", "author": "Ремарк"},
    {"id": 2, "title": "Немного солнца в холодной воде", "author": "Саган"},
]

class BookIn(BaseModel):
    title: str
    author: str

@app.on_event("startup")
def on_startup():
    logger.info("Сервис запущен. Версия=%s, MAX_BOOKS=%s", APP_VERSION, MAX_BOOKS)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/version")
def version():
    return {"version": APP_VERSION}


@app.get("/books")
def list_books():
    logger.info("Запрос списка книг, всего=%s", len(books))
    return books

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for b in books:
        if b["id"] == book_id:
            return b
    logger.warning("Книга id=%s не найдена", book_id)
    raise HTTPException(status_code=404, detail="Книга не найдена")

@app.post("/books")
def add_book(book: BookIn):
    if len(books) >= MAX_BOOKS:
        raise HTTPException(status_code=400, detail="Достигнут лимит книг")
    new_id = max((b["id"] for b in books), default=0) + 1
    new_book = {"id": new_id, "title": book.title, "author": book.author}
    books.append(new_book)
    logger.info("Добавлена книга id=%s title=%s", new_id, book.title)
    return new_book

@app.get("/books/search/by-author")
def search_by_author(author: str):
    logger.info("Поиск по автору=%s", author)
    found = [b for b in books if author.lower() in b["author"].lower()]
    return {"count": len(found), "items": found}