from typing import Annotated
from uuid import uuid4
from fastapi import HTTPException, Header
import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlmodel import create_engine
from sqlmodel.pool import StaticPool

from app.dependencies import Database, create_db_and_tables, get_session, validate_user

from app.main import app
from app.entities.offer import SizeEnum


@pytest.fixture(name="client")
def client_fixture():

    async def validate_user_override(
        authorization: Annotated[str | None, Header()] = None
    ):
        if authorization is None:
            raise HTTPException(status_code=403, detail="No hay token en la solicitud")
        elif authorization == "valid":
            return {
                "id": "541a12c5-9388-4f48-93f3-dd56d553c4c3",
                "username": "felicita",
                "email": "josefina37@hotmail.com",
                "fullName": "dr. doug smith",
                "dni": "849",
                "phoneNumber": "7063069022",
                "status": "NO_VERIFICADO",
            }
        else:
            raise HTTPException(
                status_code=401, detail="El token no es válido o está vencido."
            )

    app.dependency_overrides[validate_user] = validate_user_override
    Database._engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    create_db_and_tables()
    client = TestClient(app)
    yield client


@pytest.fixture
def fake():
    return Faker()


def test_create_offer(client: TestClient, fake: Faker):

    sizes = [member.value for member in SizeEnum]
    offer_data = {
        "postId": str(uuid4()),
        "description": fake.text(100),
        "size": fake.random_element(sizes),
        "fragile": "false",
        "offer": fake.random_int(min=1, max=100),
    }
    response = client.post("/offers", json=offer_data, headers={"Authorization": "valid"})
    data = response.json()

    assert response.status_code == 201
    assert data["id"] is not None
    assert data["createdAt"] is not None
    offer_data["id"] = data["id"]
    offer_data["createdAt"] = data["createdAt"]


def test_get_offers(client: TestClient, fake: Faker):
    # Crear algunas ofertas falsas en la base de datos
    for _ in range(5):
        sizes = [member.value for member in SizeEnum]
        offer_data = {
            "postId": str(uuid4()),
            "description": fake.text(100),
            "size": fake.random_element(sizes),
            "fragile": "false",
            "offer": fake.random_int(min=1, max=100),
        }
        client.post("/offers", json=offer_data, headers={"Authorization": "valid"})

    response = client.get("/offers", headers={"Authorization": "valid"})
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 5
    for offer_data in data:
        assert "id" in offer_data
        assert "postId" in offer_data
        assert "description" in offer_data
        assert "size" in offer_data
        assert "fragile" in offer_data
        assert "offer" in offer_data
        assert "createdAt" in offer_data
        assert "userId" in offer_data


def test_get_offer(client: TestClient, fake: Faker):
    sizes = [member.value for member in SizeEnum]
    offer_data = {
        "postId": str(uuid4()),
        "description": fake.text(100),
        "size": fake.random_element(sizes),
        "fragile": "false",
        "offer": fake.random_int(min=1, max=100),
    }
    response = client.post("/offers", json=offer_data, headers={"Authorization": "valid"})
    data = response.json()

    offer_id = data["id"]

    response = client.get(f"/offers/{offer_id}", headers={"Authorization": "valid"})
    data = response.json()

    assert response.status_code == 200

    assert "id" in data
    assert "postId" in data
    assert "description" in data
    assert "size" in data
    assert "fragile" in data
    assert "offer" in data
    assert "createdAt" in data
    assert "userId" in data

    response = client.get("/offers/bf8792d2-3097-11ee-be56-0242ac120002", headers={"Authorization": "valid"})
    assert response.status_code == 404
    assert response.json()["detail"] == "La oferta con ese ID no existe."

    response = client.get("/offers/1", headers={"Authorization": "valid"})
    assert response.status_code == 400
    assert response.json()["detail"] == "El id no es un valor string con formato uuid."

def test_delete_offer(client: TestClient, fake: Faker):
    sizes = [member.value for member in SizeEnum]
    offer_data = {
        "postId": str(uuid4()),
        "description": fake.text(100),
        "size": fake.random_element(sizes),
        "fragile": "false",
        "offer": fake.random_int(min=1, max=100),
    }
    response = client.post("/offers", json=offer_data, headers={"Authorization": "valid"})
    data = response.json()

    assert response.status_code == 201
    assert "id" in data
    assert "createdAt" in data
    offer_id = data["id"]

    delete_response = client.delete(f"/offers/{offer_id}", headers={"Authorization": "valid"})
    delete_data = delete_response.json()

    assert delete_response.status_code == 200
    assert delete_data == {"msg": "la oferta fue eliminada"}

    get_response = client.get(f"/offers/{offer_id}")
    assert get_response.status_code == 403

    response = client.delete("/offers/bf8792d2-3097-11ee-be56-0242ac120002", headers={"Authorization": "valid"})
    assert response.status_code == 404
    assert response.json()["detail"] == "La oferta con ese ID no existe."

    response = client.delete("/offers/1", headers={"Authorization": "valid"})
    assert response.status_code == 400
    assert response.json()["detail"] == "El id no es un valor string con formato uuid."
    

def test_healthcheck(client: TestClient):
    response = client.get(f"/offers/ping")

    assert response.status_code == 200
    assert response.text == "PONG"


def test_reset_db(client: TestClient):
    response = client.post(f"/offers/reset")
    data = response.json()

    assert response.status_code == 200
    assert data["msg"] == "Todos los datos fueron eliminados"