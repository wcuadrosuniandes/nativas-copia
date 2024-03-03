import json
from os import environ
import re
from urllib.parse import parse_qs, urlparse
from dotenv import load_dotenv, find_dotenv
from faker import Faker
from fastapi.testclient import TestClient
from httpx import URL, Response, Request
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

def route_get(request: Request):
    code = 200
    json = None
    request_url = str(request.url)    
    parsed_url = urlparse(request_url)    
    query_params = parse_qs(parsed_url.query)    
    flight = query_params.get('flight', [None])[0]

    if "Authorization" not in request.headers:
        code = 403
        json = {"msg": "El token no existe"}
    elif request.headers["Authorization"] != "OK":
        code = 401
        json = {"msg": "El token no es válido"}
    elif flight == "847":
        json = {}
    elif flight == "179":
        json = [{
            "id": "d58e4651-1d98-47e3-a589-a56eea417421",
            "flightId": "179",
            "sourceAirportCode": "BOG",
            "sourceCountry": "Colombia",
            "destinyAirportCode": "LGW",
            "destinyCountry": "Inglaterra",
            "bagCost": 124,
            "plannedStartDate": "2024-03-29T03:12:37.241000",
            "plannedEndDate": "2024-04-08T03:12:37.241000",
            "createdAt": "2024-02-24T01:44:03.654027"
        }]
    else:
        json = [{
            "id": "daac2036-9f28-4e61-ae45-901444e38c7c",
            "flightId": "555",
            "sourceAirportCode": "BOG",
            "sourceCountry": "Colombia",
            "destinyAirportCode": "LGW",
            "destinyCountry": "Inglaterra",
            "bagCost": 117,
            "plannedStartDate": "2024-03-29T03:12:37.241000",
            "plannedEndDate": "2024-04-08T03:12:37.241000",
            "createdAt": "2024-02-24T01:44:03.654027"
        }]

    return Response(code, json=json)

def route_create(request: Request):
    code = 200
    if "Authorization" not in request.headers:
        code = 403
        json = {"msg": "El token no existe"}
    elif request.headers["Authorization"] != "OK":
        code = 401
        json = {"msg": "El token no es válido"}
    else:
        json = {
            "id": "461f1891-ac36-47a2-ba13-9d4fdb949a3c",
            "createdAt": "2024-02-24T01:44:03.654027",
        }
    return Response(code, json=json)

def post_create(request: Request):
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
            "expireAt": "2024-04-24T01:44:03.654027",
            "route": {
                "id": "461f1891-ac36-47a2-ba13-9d4fdb949a3c",
                "createdAt": "2024-02-24T01:44:03.654027",
            }
        }
    return Response(code, json=json)

def routeAssociatedPost_get(request: Request):
    code = 200    
    request_url = str(request.url)    
    parsed_url = urlparse(request_url)    
    query_params = parse_qs(parsed_url.query)    
    route_id = query_params.get('route', [None])[0]

    if "Authorization" not in request.headers:
        code = 403
        json = {"msg": "El token no existe"}
    elif request.headers["Authorization"] != "OK":
        code = 401
        json = {"msg": "El token no es válido"}
    elif(route_id == "daac2036-9f28-4e61-ae45-901444e38c7c"):
        json = {}
    else:
        json = {
            "id": "d58e4651-1d98-47e3-a589-a56eea417421",
        }
    return Response(code, json=json)

@pytest.fixture(name="client")
def client_fixture():
    client = TestClient(app)
    yield client

@pytest.fixture
def users_api():
    with respx.mock(
        base_url=environ["USERS_PATH"], assert_all_called=False
    ) as respx_mock:
        respx_mock.get("/users/me", name="user_me").mock(side_effect=user_me)
        yield respx_mock

@pytest.fixture
def routes_api():
    with respx.mock(
        base_url=environ["ROUTES_PATH"], assert_all_called=False
    ) as respx_mock:
        respx_mock.get("/routes?flight=555", name="route_get").mock(side_effect=route_get)
        respx_mock.get("/routes?flight=847", name="route_get_route").mock(side_effect=route_get)
        respx_mock.get("/routes?flight=179", name="route_get_route_full").mock(side_effect=route_get)
        respx_mock.post("/routes", name="route_create").mock(side_effect=route_create)
        yield respx_mock

@pytest.fixture
def posts_api():
    with respx.mock(
        base_url=environ["POSTS_PATH"], assert_all_called=False
    ) as respx_mock:
        respx_mock.post("/posts", name="post_create").mock(side_effect=post_create)
        respx_mock.get("/posts?route=daac2036-9f28-4e61-ae45-901444e38c7c", name="routeAssociatedPost_get").mock(side_effect=routeAssociatedPost_get)
        respx_mock.get("/posts?route=d58e4651-1d98-47e3-a589-a56eea417421", name="routeAssociatedPost_get_full").mock(side_effect=routeAssociatedPost_get)
        yield respx_mock

