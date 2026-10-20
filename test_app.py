from fastapi.testclient import TestClient
from app_final import app

# Тестовый клиентз апросов к API
client = TestClient(app)

# Тест проверки health
def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

# Получение списка книг
def test_list_books():
    r = client.get("/books")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

# Получение книги по ID
def test_get_book_by_id():
    r = client.get("/books/1")
    assert r.status_code == 200
    assert r.json()["id"] == 1

# книга не найдена
def test_get_book_not_found():
    r = client.get("/books/9999")
    assert r.status_code == 404