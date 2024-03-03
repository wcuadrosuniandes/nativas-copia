from os import environ
from httpx import Response
import pytest
from faker import Faker
from fastapi.testclient import TestClient
import respx

from app.main import app


def test_create_offer(
    client: TestClient,
    fake: Faker,
    users_api,
    posts_api,
    offers_api,
    scores_api,
    routes_api,
):

    offer_data = {
        "description": fake.text(100),
        "size": "SMALL",
        "fragile": True,
        "offer": 1000,
    }

    post_id = "ccb66854-c240-4d2f-87e4-9ff0b386682f"

    response = client.post(
        "/rf004/posts/{}/offers".format(post_id),
        json=offer_data,
        headers={"Authorization": "OK"},
    )
    data = response.json()

    assert response.status_code == 201
    assert data["data"] is not None
    assert data["msg"] is not None
    assert data["data"]["id"] is not None
    assert data["data"]["userId"] is not None
    assert data["data"]["createdAt"] is not None
    assert data["data"]["postId"] is not None


def test_create_offer_own(
    client: TestClient, fake: Faker, users_api, posts_api, offers_api, scores_api
):

    offer_data = {
        "description": fake.text(100),
        "size": "SMALL",
        "fragile": True,
        "offer": 1000,
    }

    post_id = "abcdef12-c240-4d2f-87e4-9ff0b386682f"

    response = client.post(
        "/rf004/posts/{}/offers".format(post_id),
        json=offer_data,
        headers={"Authorization": "OK"},
    )

    assert response.status_code == 412


def test_create_offer_expired(
    client: TestClient, fake: Faker, users_api, posts_api, offers_api, scores_api
):

    offer_data = {
        "description": fake.text(100),
        "size": "SMALL",
        "fragile": True,
        "offer": 1000,
    }

    post_id = "aabbccdd-c240-4d2f-87e4-9ff0b386682f"

    response = client.post(
        "/rf004/posts/{}/offers".format(post_id),
        json=offer_data,
        headers={"Authorization": "OK"},
    )

    assert response.status_code == 412


def test_create_offer_without_token(
    client: TestClient, fake: Faker, users_api, posts_api, offers_api, scores_api
):
    offer_data = {
        "description": fake.text(100),
        "size": "SMALL",
        "fragile": True,
        "offer": 1000,
    }

    post_id = "abcdef12-c240-4d2f-87e4-9ff0b386682f"
    response = client.post("/rf004/posts/{}/offers".format(post_id), json=offer_data)

    assert response.status_code == 403


def test_create_offer_with_invalid_token(
    client: TestClient, fake: Faker, users_api, posts_api, offers_api, scores_api
):
    offer_data = {
        "description": fake.text(100),
        "size": "SMALL",
        "fragile": True,
        "offer": 1000,
    }

    post_id = "abcdef12-c240-4d2f-87e4-9ff0b386682f"
    response = client.post(
        "/rf004/posts/{}/offers".format(post_id),
        json=offer_data,
        headers={"Authorization": "NO"},
    )

    assert response.status_code == 401


def test_create_offer_post_not_exists(
    client: TestClient, fake: Faker, users_api, posts_api, offers_api, scores_api
):
    offer_data = {
        "description": fake.text(100),
        "size": "SMALL",
        "fragile": True,
        "offer": 1000,
    }

    post_id = "12345678-c240-4d2f-87e4-9ff0b386682f"
    response = client.post(
        "/rf004/posts/{}/offers".format(post_id),
        json=offer_data,
        headers={"Authorization": "OK"},
    )

    assert response.status_code == 404


def test_create_offer_incomplete(
    client: TestClient, fake: Faker, users_api, posts_api, offers_api, scores_api
):
    offer_data = {"description": fake.text(100), "size": "SMALL"}

    post_id = "ccb66854-c240-4d2f-87e4-9ff0b386682f"
    response = client.post(
        "/rf004/posts/{}/offers".format(post_id),
        json=offer_data,
        headers={"Authorization": "OK"},
    )

    assert response.status_code == 400
