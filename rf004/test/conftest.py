from datetime import datetime, timedelta
from os import environ
import re
from dotenv import load_dotenv, find_dotenv
from faker import Faker
from fastapi.testclient import TestClient
from httpx import Request, Response
import pytest
import respx

from app.main import app

environ["ENV"] = "test"


def pytest_configure(config):
    env_file = find_dotenv("../.env.test")
    load_dotenv(env_file)
    return config


def user_me(request: Request):
    code = 200
    json = None
    if "Authorization" not in request.headers:
        code = 403
        json = {"msg": "El token no existe"}
    elif request.headers["Authorization"] != "OK":
        code = 401
        json = {"msg": "El token no es válido"}
    else:
        json = {
            "id": "461f1891-ac36-47a2-ba13-9d4fdb949a3c",
            "username": "earlene",
            "email": "paige.bergstrom72@gmail.com",
            "fullName": "mae sipes",
            "dni": "189",
            "phoneNumber": "3806416390",
            "status": "POR_VERIFICAR",
        }
    return Response(code, json=json)


def post_get(request: Request):
    code = 200
    json = None
    postpattern = re.compile("/posts/(.*)")
    post_id = postpattern.search(request.url.path).group(1)
    if "Authorization" not in request.headers:
        code = 403
        json = {"msg": "El token no existe"}
    elif request.headers["Authorization"] != "OK":
        code = 401
        json = {"msg": "El token no es válido"}
    elif post_id == "no_valido":
        code = 400
        json = {"msg": "El id de post es inválido"}
    elif (
        post_id != "ccb66854-c240-4d2f-87e4-9ff0b386682f"
        and post_id != "abcdef12-c240-4d2f-87e4-9ff0b386682f"
        and post_id != "aabbccdd-c240-4d2f-87e4-9ff0b386682f"
    ):
        code = 404
        json = {"msg": "No existe la publicación"}
    elif post_id == "ccb66854-c240-4d2f-87e4-9ff0b386682f":
        json = {
            "id": "ccb66854-c240-4d2f-87e4-9ff0b386682f",
            "userId": "12345678-ac36-47a2-ba13-9d4fdb949a3c",
            "routeId": "2a763671-8f91-407c-b553-109b46162e22",
            "expireAt": (datetime.now() + timedelta(days=15)).isoformat(),
            "createdAt": "2024-02-24T01:44:03.858683",
        }
    elif post_id == "aabbccdd-c240-4d2f-87e4-9ff0b386682f":
        json = {
            "id": "ccb66854-c240-4d2f-87e4-9ff0b386682f",
            "userId": "12345678-ac36-47a2-ba13-9d4fdb949a3c",
            "routeId": "2a763671-8f91-407c-b553-109b46162e22",
            "expireAt": (datetime.now() + timedelta(days=-15)).isoformat(),
            "createdAt": "2024-02-24T01:44:03.858683",
        }
    else:
        json = {
            "id": "abcdef12-c240-4d2f-87e4-9ff0b386682f",
            "userId": "461f1891-ac36-47a2-ba13-9d4fdb949a3c",
            "routeId": "2a763671-8f91-407c-b553-109b46162e22",
            "expireAt": (datetime.now() + timedelta(days=15)).isoformat(),
            "createdAt": "2024-02-24T01:44:03.858683",
        }
    return Response(code, json=json)


def route_get(request: Request):
    code = 200
    json = None
    if "Authorization" not in request.headers:
        code = 403
        json = {"msg": "El token no existe"}
    elif request.headers["Authorization"] != "OK":
        code = 401
        json = {"msg": "El token no es válido"}
    else:
        json = {
            "id": "daac2036-9f28-4e61-ae45-901444e38c7c",
            "flightId": "617",
            "sourceAirportCode": "BOG",
            "sourceCountry": "Colombia",
            "destinyAirportCode": "LGW",
            "destinyCountry": "Inglaterra",
            "bagCost": 117,
            "plannedStartDate": "2024-02-26T21:42:21.138000",
            "plannedEndDate": "2024-03-05T21:42:21.138000",
            "createdAt": "2024-02-24T01:44:03.862906",
        }
    return Response(code, json=json)


def offer_create(request: Request):
    code = 200
    if "Authorization" not in request.headers:
        code = 403
        json = {"msg": "El token no existe"}
    elif request.headers["Authorization"] != "OK":
        code = 401
        json = {"msg": "El token no es válido"}
    else:
        json = {
            "id": "d58e4651-1d98-47e3-a589-a56eea417421",
            "userId": "461f1891-ac36-47a2-ba13-9d4fdb949a3c",
            "createdAt": "2024-02-24T01:44:03.654027",
        }
    return Response(code, json=json)


def score_create(request: Request):
    code = 200
    if "Authorization" not in request.headers:
        code = 403
        json = {"msg": "El token no existe"}
    elif request.headers["Authorization"] != "OK":
        code = 401
        json = {"msg": "El token no es válido"}
    else:
        json = {"msg": "Score Calculado Satisfactoriamente"}
    return Response(code, json=json)


@pytest.fixture(name="client")
def client_fixture():
    client = TestClient(app)
    yield client


@pytest.fixture
def fake():
    return Faker()


@pytest.fixture
def users_api():
    with respx.mock(
        base_url=environ["USERS_PATH"], assert_all_called=False
    ) as respx_mock:
        respx_mock.get("/users/me", name="user_me").mock(side_effect=user_me)
        yield respx_mock


@pytest.fixture
def posts_api():
    with respx.mock(
        base_url=environ["POSTS_PATH"], assert_all_called=False
    ) as respx_mock:
        respx_mock.get(
            "/posts/ccb66854-c240-4d2f-87e4-9ff0b386682f", name="post_get_valid"
        ).mock(side_effect=post_get)
        respx_mock.get(
            "/posts/abcdef12-c240-4d2f-87e4-9ff0b386682f", name="post_get_valid_2"
        ).mock(side_effect=post_get)
        respx_mock.get(
            "/posts/12345678-c240-4d2f-87e4-9ff0b386682f", name="post_get_invalid"
        ).mock(side_effect=post_get)
        respx_mock.get(
            "/posts/aabbccdd-c240-4d2f-87e4-9ff0b386682f", name="post_get_expired"
        ).mock(side_effect=post_get)
        yield respx_mock


@pytest.fixture
def offers_api():
    with respx.mock(
        base_url=environ["OFFERS_PATH"], assert_all_called=False
    ) as respx_mock:
        respx_mock.post("/offers", name="offer_create").mock(side_effect=offer_create)
        yield respx_mock


@pytest.fixture
def scores_api():
    with respx.mock(
        base_url=environ["SCORES_PATH"], assert_all_called=False
    ) as respx_mock:
        respx_mock.post("/scores", name="score_create").mock(side_effect=score_create)
        yield respx_mock


@pytest.fixture
def routes_api():
    with respx.mock(
        base_url=environ["ROUTES_PATH"], assert_all_called=False
    ) as respx_mock:
        respx_mock.get("/routes/2a763671-8f91-407c-b553-109b46162e22", name="route_get").mock(side_effect=route_get)
        yield respx_mock
