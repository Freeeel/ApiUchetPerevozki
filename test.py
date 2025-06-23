import pytest
from fastapi.testclient import TestClient
from main import app  # Импортируйте ваше приложение FastAPI из нужного модуля

client = TestClient(app)


def test_authorization_success():
    response = client.post("/login", json={"login": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "id" in response.json()

def test_authorization_failure():
    response = client.post("/login", json={"login": "wronguser", "password": "wrongpass"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid login or password"}


def test_create_repair():
    response = client.post("/repairs/", json={
        "description_breakdown": "Сломался двигатель",
        "date_and_time_repair": "2024-10-01",
        "address_point_repair": "деревня Сметанино",
        "user_id": 1
    })
    assert response.status_code == 200
    assert "id" in response.json()


def test_create_report():
    response = client.post("/reports/", json={
        "point_departure": "Пункт A",
        "type_point_departure": "Тип A",
        "sender": "Отправитель",
        "point_destination": "Пункт B",
        "type_point_destination": "Тип B",
        "recipient": "Получатель",
        "view_wood": "Фанкряж",
        "length_wood": 6,
        "volume_wood": 10.5,
        "report_date_time": "2024-12-11",
        "assortment_wood_type": "Осина",
        "variety_wood_type": "1 сорт",
        "user_id": 1
    })
    assert response.status_code == 200
    assert "id" in response.json()


def test_update_user():
    response = client.put("/users/1", json={
        "phone": "1234567890",
        "password": "newpassword",
        "address_residential": "New Address",
        "bank_account_number": 1234567890
    })
    assert response.status_code == 200
    assert response.json()

def test_update_user_not_found():
    response = client.put("/users/999", json={
        "phone": "1234567890",
        "password": "newpassword",
        "address_residential": "Новый адрес",
        "bank_account_number": 1234567890
    })
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

# Тесты для получения автомобилей пользователя
def test_get_user_car():
    response = client.get("/user/1/car")
    assert response.status_code == 200
    assert "car_id" in response.json()  # Предполагается, что возвращается car_id

def test_get_user_car_not_found():
    response = client.get("/user/999/car")
    assert response.status_code == 404
    assert response.json() == {"detail": "Нет привязанных автомобилей для этого пользователя"}