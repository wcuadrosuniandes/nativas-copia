from typing import Annotated
from uuid import uuid4
import pytest
import random
from datetime import datetime, timedelta
from fastapi import HTTPException, Header
from faker import Faker
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from  app.dependencies  import  Database, create_db_and_tables, get_session, validate_user

from  app.main  import app



@pytest.fixture(name="client")
def client_fixture():
    async def validate_user_override(
        authorization: Annotated[str | None, Header()] = None
    ):
        if authorization is None:
            raise HTTPException(status_code=403, detail="No hay token en la solicitud")
        elif authorization == "b3ed1083-e753-4beb-95f5-e005d5ff1ce4":
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

def test_create_route(client: TestClient, fake: Faker):
    flight = random.randint(10,1000)
    route_data = generate_route(flight, fake)
    response = client.post("/routes", json=route_data, headers={"Authorization": "b3ed1083-e753-4beb-95f5-e005d5ff1ce4"})
    data = response.json()
    assert response.status_code == 201
    assert data["id"] is not None
    assert data["createdAt"] is not None
    

def test_create_route_invalid_date(client: TestClient, fake: Faker):
    flight = random.randint(10,1000)
    route_data = generate_route(flight, fake)
    route_data["plannedStartDate"] = "2024-07-01T11:20:53.214Z"
    response = client.post("/routes", json=route_data, headers={"Authorization": "b3ed1083-e753-4beb-95f5-e005d5ff1ce4"})
    data = response.json()
    assert response.status_code == 412

def test_create_route_not_token(client: TestClient, fake: Faker):
    dates = generate_dates()
    flight = random.randint(10,1000)
    route_data = generate_route(flight, fake)
    response = client.post("/routes", json=route_data)
    data = response.json()
    assert response.status_code == 403


def test_create_route_flightId_exist(client: TestClient, fake: Faker):
    dates = generate_dates()
    flight = random.randint(10,1000)
    route_data =  generate_route(flight, fake)
    route_data_copy = generate_route(flight, fake)
    response = client.post("/routes", json=route_data, headers={"Authorization": "b3ed1083-e753-4beb-95f5-e005d5ff1ce4"})
    response = client.post("/routes", json=route_data_copy, headers={"Authorization": "b3ed1083-e753-4beb-95f5-e005d5ff1ce4"})
    data = response.json()
    assert response.status_code == 412
    assert data["msg"] is not None



def test_get_routes(client: TestClient, fake: Faker):
    route_data =  generate_route(random.randint(10,1000), fake)
    response = client.post("/routes", json=route_data, headers={"Authorization": "b3ed1083-e753-4beb-95f5-e005d5ff1ce4"})
    response = client.get("/routes", headers={"Authorization": "b3ed1083-e753-4beb-95f5-e005d5ff1ce4"})
    data = response.json()
    print(data)
    route = data[0]
    assert response.status_code == 200
    assert len(data) > 0
    assert route["flightId"] is not None
    assert route["sourceAirportCode"] is not None
    assert route["sourceCountry"] is not None
    assert route["destinyAirportCode"] is not None
    assert route["destinyCountry"] is not None
    assert route["bagCost"] is not None
    assert route["plannedStartDate"] is not None
    assert route["plannedEndDate"] is not None
    assert route["createdAt"] is not None

def test_delete_routes(client: TestClient, fake: Faker):
    route_data =  generate_route(random.randint(10,1000), fake)
    response = client.post("/routes", json=route_data, headers={"Authorization": "b3ed1083-e753-4beb-95f5-e005d5ff1ce4"})
    data = response.json()
    id_route = data["id"]

    response = client.delete("/routes/"+id_route, headers={"Authorization": "b3ed1083-e753-4beb-95f5-e005d5ff1ce4"})
    data = response.json()
    assert response.status_code == 200
    assert data["msg"] == "el trayecto fue eliminado"

def test_healthcheck(client: TestClient):
    response = client.get("/routes/ping", headers={"Authorization": "b3ed1083-e753-4beb-95f5-e005d5ff1ce4"})
    assert response.status_code == 200
    assert response.text == "pong"

def generate_dates():
    now = datetime.now() + timedelta(days=1)
    plannedStartDate = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    new_date = now + timedelta(days=2)
    plannedEndDate = new_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return [plannedStartDate, plannedEndDate]

def generate_route(flight, fake: Faker):
    dates = generate_dates()
    return {
        "flightId": str(flight),
        "sourceAirportCode": fake.word(),
        "sourceCountry": fake.word(),
        "destinyAirportCode": fake.word(),
        "destinyCountry": fake.word(),
        "bagCost": random.randint(100,1000) ,
        "plannedStartDate": dates[0] ,
        "plannedEndDate":  dates[1]
    }
