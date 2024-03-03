import pytest
from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
from app.main import app

def test_create_post_exist_route(
    client: TestClient,
    users_api,
    routes_api,
    posts_api,
    ):
    rf003_data = {
        "flightId": "555",
        "expireAt": "2024-04-29T03:12:37.241Z",
        "plannedStartDate": "2024-03-29T03:12:37.241Z",
        "plannedEndDate": "2024-04-08T03:12:37.241Z",
        "origin": {"airportCode": "BOG", "country": "Colombia"},
        "destiny": {"airportCode": "LGW", "country": "Inglaterra"},
        "bagCost": 117,
    }

    response = client.post("rf003/posts", json=rf003_data, headers={"Authorization": "OK"})
    data = response.json()

    assert response.status_code == 201
    assert data["data"] is not None
    assert data["msg"] is not None
    assert data["data"]["id"] is not None
    assert data["data"]["userId"] is not None
    assert data["data"]["createdAt"] is not None
    assert data["data"]["expireAt"] is not None
    assert data["data"]["route"] is not None

def test_create_post_wrong_datePlannedStart(
    client: TestClient,
    users_api,
    routes_api,
    posts_api,
    ):
    rf003_data = {
        "flightId": "555",
        "expireAt": "2024-04-29T03:12:37.241Z",
        "plannedStartDate": "2024-01-29T03:12:37.241Z",
        "plannedEndDate": "2024-04-08T03:12:37.241Z",
        "origin": {"airportCode": "BOG", "country": "Colombia"},
        "destiny": {"airportCode": "LGW", "country": "Inglaterra"},
        "bagCost": 117,
    }

    response = client.post("rf003/posts", json=rf003_data, headers={"Authorization": "OK"})

    assert response.status_code == 412

def test_create_post_wrong_datePlannedEnd(
    client: TestClient,
    users_api,
    routes_api,
    posts_api,
    ):
    rf003_data = {
        "flightId": "555",
        "expireAt": "2024-04-29T03:12:37.241Z",
        "plannedStartDate": "2024-03-29T03:12:37.241Z",
        "plannedEndDate": "2024-01-08T03:12:37.241Z",
        "origin": {"airportCode": "BOG", "country": "Colombia"},
        "destiny": {"airportCode": "LGW", "country": "Inglaterra"},
        "bagCost": 117,
    }

    response = client.post("rf003/posts", json=rf003_data, headers={"Authorization": "OK"})

    assert response.status_code == 412

def test_create_post_invalid_datePlanned(
    client: TestClient,
    users_api,
    routes_api,
    posts_api,
    ):
    rf003_data = {
        "flightId": "555",
        "expireAt": "2024-04-29T03:12:37.241Z",
        "plannedStartDate": "2022-03-29T03:12:37.241Z",
        "plannedEndDate": "2022-01-08T03:12:37.241Z",
        "origin": {"airportCode": "BOG", "country": "Colombia"},
        "destiny": {"airportCode": "LGW", "country": "Inglaterra"},
        "bagCost": 117,
    }

    response = client.post("rf003/posts", json=rf003_data, headers={"Authorization": "OK"})

    assert response.status_code == 412

def test_create_post_without_route(
    client: TestClient,
    users_api,
    routes_api,
    posts_api,
    ):
    rf003_data = {
        "flightId": "847",
        "expireAt": "2024-04-29T03:12:37.241Z",
        "plannedStartDate": "2024-03-29T03:12:37.241Z",
        "plannedEndDate": "2024-04-08T03:12:37.241Z",
        "origin": {"airportCode": "BOG", "country": "Colombia"},
        "destiny": {"airportCode": "LGW", "country": "Inglaterra"},
        "bagCost": 117,
    }

    response = client.post("rf003/posts", json=rf003_data, headers={"Authorization": "OK"})
    data = response.json()

    assert response.status_code == 201
    assert data["data"] is not None
    assert data["msg"] is not None
    assert data["data"]["id"] is not None
    assert data["data"]["userId"] is not None
    assert data["data"]["createdAt"] is not None
    assert data["data"]["expireAt"] is not None
    assert data["data"]["route"] is not None

def test_create_post_invalid_dateExpire(
    client: TestClient,
    users_api,
    routes_api,
    posts_api,
    ):
    rf003_data = {
        "flightId": "555",
        "expireAt": "2022-08-01T21:20:53.214Z",
        "plannedStartDate": "2024-03-29T03:12:37.241Z",
        "plannedEndDate": "2024-04-08T03:12:37.241Z",
        "origin": {"airportCode": "BOG", "country": "Colombia"},
        "destiny": {"airportCode": "LGW", "country": "Inglaterra"},
        "bagCost": 117,
    }

    response = client.post("rf003/posts", json=rf003_data, headers={"Authorization": "OK"})

    assert response.status_code == 412

def test_create_post_without_token(
    client: TestClient,
    users_api,
    routes_api,
    posts_api,
    ):
    rf003_data = {
        "flightId": "847",
        "expireAt": "2024-04-29T03:12:37.241Z",
        "plannedStartDate": "2024-03-29T03:12:37.241Z",
        "plannedEndDate": "2024-04-08T03:12:37.241Z",
        "origin": {"airportCode": "BOG", "country": "Colombia"},
        "destiny": {"airportCode": "LGW", "country": "Inglaterra"},
        "bagCost": 117,
    }

    response = client.post("rf003/posts", json=rf003_data)
    data = response.json()

    assert response.status_code == 403

def test_create_post_with_invalid_token(
    client: TestClient,
    users_api,
    routes_api,
    posts_api,
    ):
    rf003_data = {
        "flightId": "555",
        "expireAt": "2024-04-29T03:12:37.241Z",
        "plannedStartDate": "2024-03-29T03:12:37.241Z",
        "plannedEndDate": "2024-04-08T03:12:37.241Z",
        "origin": {"airportCode": "BOG", "country": "Colombia"},
        "destiny": {"airportCode": "LGW", "country": "Inglaterra"},
        "bagCost": 117,
    }

    response = client.post("rf003/posts", json=rf003_data, headers={"Authorization": "NO"})
    data = response.json()

    assert response.status_code == 401

def test_create_post_incomplete_field(
    client: TestClient,
    users_api,
    routes_api,
    posts_api,
    ):
    rf003_data = {
        "expireAt": "2024-04-29T03:12:37.241Z",
        "plannedStartDate": "2024-03-29T03:12:37.241Z",
        "plannedEndDate": "2024-04-08T03:12:37.241Z",
        "origin": {"airportCode": "BOG", "country": "Colombia"},
        "destiny": {"airportCode": "LGW", "country": "Inglaterra"},
        "bagCost": 117,
    }

    response = client.post("rf003/posts", json=rf003_data, headers={"Authorization": "OK"})
    data = response.json()

    assert response.status_code == 400

def test_create_post_exist_route_with_post(
    client: TestClient,
    users_api,
    routes_api,
    posts_api,
    ):
    rf003_data = {
        "flightId": "179",
        "expireAt": "2024-04-29T03:12:37.241Z",
        "plannedStartDate": "2024-03-29T03:12:37.241Z",
        "plannedEndDate": "2024-04-08T03:12:37.241Z",
        "origin": {"airportCode": "BOG", "country": "Colombia"},
        "destiny": {"airportCode": "LGW", "country": "Inglaterra"},
        "bagCost": 117,
    }

    response = client.post("rf003/posts", json=rf003_data, headers={"Authorization": "OK"})
    data = response.json()

    assert response.status_code == 412