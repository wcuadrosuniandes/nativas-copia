from uuid import uuid4
import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.dependencies import Database, create_db_and_tables, get_session

from app.main import app
from app.entities.user import StatusEnum


@pytest.fixture(name="client")
def client_fixture():
    Database._engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    create_db_and_tables()
    client = TestClient(app)
    yield client


@pytest.fixture
def fake():
    return Faker()


def test_create_user(client: TestClient, fake: Faker):
    profile = fake.profile()
    user_data = {
        "username": profile["username"],
        "password": fake.password(length=12),
        "email": profile["mail"],
        "dni": profile["ssn"],
        "fullName": profile["name"],
        "phoneNumber": fake.phone_number(),
    }
    response = client.post(
        "/users",
        json=user_data,
    )
    data = response.json()

    assert response.status_code == 201
    assert data["id"] is not None
    assert data["createdAt"] is not None
    user_data["id"] = data["id"]
    user_data["createdAt"] = data["createdAt"]
    return user_data


def test_create_user_repeated(client: TestClient, fake: Faker):
    profile = fake.profile()
    user_data = {
        "username": profile["username"],
        "password": fake.password(length=12),
        "email": profile["mail"],
        "dni": profile["ssn"],
        "fullName": profile["name"],
        "phoneNumber": fake.phone_number(),
    }
    _ = client.post("/users", json=user_data)
    response2 = client.post("/users", json=user_data)

    assert response2.status_code == 412


def test_create_user_with_missing_data(client: TestClient, fake: Faker):
    profile = fake.profile()
    user_data = {"fullName": profile["name"]}
    response = client.post("/users", json=user_data)

    assert response.status_code == 400


def test_update_user(client: TestClient, fake: Faker):
    user = test_create_user(client, fake)
    profile = fake.profile()
    statuses = [member.value for member in StatusEnum]
    update_data = {
        "status": fake.random_element(statuses),
        "dni": profile["ssn"],
        "fullName": profile["name"],
        "phoneNumber": fake.phone_number(),
    }
    response = client.patch(f"/users/{user['id']}", json=update_data)
    data = response.json()

    assert response.status_code == 200
    assert data["msg"] == "el usuario ha sido actualizado"


def test_update_user_without_fields(client: TestClient, fake: Faker):
    user = test_create_user(client, fake)
    update_data = {}
    response = client.patch(f"/users/{user['id']}", json=update_data)

    assert response.status_code == 400


def test_update_user_invalid_fields(client: TestClient, fake: Faker):
    user = test_create_user(client, fake)
    update_data = {"email": fake.email()}
    response = client.patch(f"/users/{user['id']}", json=update_data)

    assert response.status_code == 400


def test_update_user_invalid_user_id(client: TestClient, fake: Faker):
    user_id = uuid4()
    profile = fake.profile()
    statuses = [member.value for member in StatusEnum]
    update_data = {
        "status": fake.random_element(statuses),
        "dni": profile["ssn"],
        "fullName": profile["name"],
        "phoneNumber": fake.phone_number(),
    }
    response = client.patch(f"/users/{user_id}", json=update_data)

    assert response.status_code == 404


def test_auth(client: TestClient, fake: Faker):
    user = test_create_user(client, fake)
    update_data = {"username": user["username"], "password": user["password"]}
    response = client.post(f"/users/auth", json=update_data)
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == user["id"]
    assert data["token"] is not None
    assert data["expireAt"] is not None
    user["token"] = data["token"]
    return user


def test_auth_invalid_credentials(client: TestClient, fake: Faker):
    user = test_create_user(client, fake)
    update_data = {"username": user["username"], "password": user["password"] + "wrong"}
    response = client.post(f"/users/auth", json=update_data)

    assert response.status_code == 404


def test_auth_notexistent_user(client: TestClient, fake: Faker):
    update_data = {"username": "not_exist", "password": "not_exist"}
    response = client.post(f"/users/auth", json=update_data)

    assert response.status_code == 404


def test_auth_missing_fields(client: TestClient, fake: Faker):
    update_data = {"username": "not_exist"}
    response = client.post(f"/users/auth", json=update_data)

    assert response.status_code == 400


def test_get_user_info(client: TestClient, fake: Faker):
    user = test_auth(client, fake)
    client.headers.update({"Authorization": f"Bearer {user['token']}"})
    response = client.get(f"/users/me")
    data = response.json()

    assert response.status_code == 200
    assert data["id"] is not None
    assert data["username"] is not None
    assert data["email"] is not None
    assert data["fullName"] is not None
    assert data["dni"] is not None
    assert data["phoneNumber"] is not None
    assert data["status"] is not None
    assert data["id"] == user["id"]
    assert data["username"] == user["username"]
    assert data["email"] == user["email"]
    assert data["fullName"] == user["fullName"]
    assert data["dni"] == user["dni"]
    assert data["phoneNumber"] == user["phoneNumber"]


def test_get_user_info_without_token(client: TestClient):
    response = client.get(f"/users/me")

    assert response.status_code == 403


def test_get_user_info_invalid_token_1(client: TestClient, fake: Faker):
    user = test_auth(client, fake)
    client.headers.update({"Authorization": f"Bearer {user['token']}fake"})
    response = client.get(f"/users/me")

    assert response.status_code == 401


def test_get_user_info_invalid_token_2(client: TestClient):
    client.headers.update({"Authorization": f"Bearer {uuid4()}"})
    response = client.get(f"/users/me")

    assert response.status_code == 401


def test_healthcheck(client: TestClient):
    response = client.get(f"/users/ping")

    assert response.status_code == 200
    assert response.text == "PONG"


def test_reset_db(client: TestClient):
    response = client.post(f"/users/reset")
    data = response.json()

    assert response.status_code == 200
    assert data["msg"] == "Todos los datos fueron eliminados"

