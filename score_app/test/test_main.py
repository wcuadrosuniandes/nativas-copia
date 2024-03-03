from typing import Annotated
import pytest
import random
from fastapi import HTTPException, Header,status
from faker import Faker
from fastapi.testclient import TestClient
from sqlmodel import create_engine
from sqlmodel.pool import StaticPool
from app.entities.score import SizeEnum
from  app.dependencies  import  Database, create_db_and_tables, validate_user
from  app.main  import app



@pytest.fixture(name="client")
def client_fixture():
    async def validate_user_override(
        authorization: Annotated[str | None, Header()] = None
    ):
        if authorization is None:
            raise HTTPException(status_code=403, detail="No hay token en la solicitud")
        elif authorization == "Authorization":
            return {
                "id": "541a12c5-9388-4f48-93f3-dd56d553c4c3",
                "username": "usuario",
                "email": "usuario@gmail.com",
                "fullName": "UsuarioCreado",
                "dni": "123",
                "phoneNumber": "123407023",
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

def test_create_score(client: TestClient, fake: Faker):
    score_data = generate_data(fake)
    response = client.post("/scores", json=score_data, headers={"Authorization": "Authorization"})

    assert response.status_code == status.HTTP_201_CREATED

def test_create_score_not_token(client: TestClient, fake: Faker):
    score_data = generate_data(fake)
    response = client.post("/scores", json=score_data)
    score_data = response.json()
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_get_scores(client: TestClient, fake: Faker):
    score_data = generate_data(fake)
    response = client.post("/scores", json=score_data, headers={"Authorization": "Authorization"})
    response = client.get("/scores", headers={"Authorization": "Authorization"})
    data = response.json()

    assert response.status_code == 200
    assert len(data) > 0

def test_get_scores_id(client: TestClient, fake: Faker):
    score_data = generate_data(fake)
    response = client.post("/scores", json=score_data, headers={"Authorization": "Authorization"})
    assert response.status_code == status.HTTP_201_CREATED

    response_get = client.get(f"/scores/{score_data['id']}", headers={"Authorization": "Authorization"})
    data = response_get.json()

    assert response_get.status_code == 200
    assert data["offer"] is not None
    assert data["size"] is not None
    assert data["bagCost"] is not None
    assert len(data) > 0

def test_healthcheck(client: TestClient):
    response = client.get(f"/scores/ping")
    assert response.status_code == 200
    assert response.text == "PONG"

def test_reset_db(client: TestClient):
    response = client.post(f"/scores/reset")
    data = response.json()
    assert response.status_code == 200
    assert data["msg"] == "Todos los datos fueron eliminados"

def generate_data(fake: Faker):
    sizes = [member.value for member in SizeEnum]
    score_data = {
        "id": fake.uuid4(),
        "offer":random.randint(10,1000),
        "postId": fake.uuid4(),
        "size": fake.random_element(sizes),
        "bagCost":random.randint(10,1000),
    }
    return score_data
