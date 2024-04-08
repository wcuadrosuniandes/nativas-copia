from os import environ
from httpx import Response
import pytest
from faker import Faker
from fastapi.testclient import TestClient
import respx

from  app.main  import app

from .mock_data import ( user, post, post_alt)

def test_get_post(
    client: TestClient,
    fake: Faker,
    posts_api,
    offers_api,
    scores_api,
    routes_api,
):
    response = client.get(
        "/rf005/posts/{}".format(post['id']),
        headers={"Authorization": "bearer"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["data"] is not None
    assert data["data"]["route"] is not None
    assert data["data"]["offers"] is not None

def test_get_post_other_owner(
    client: TestClient,
    fake: Faker,
    posts_api,
    offers_api,
    scores_api,
    routes_api,
):
    response = client.get(
        "/rf005/posts/{}".format(post_alt['id']),
        headers={"Authorization": "bearer"},
    )
    data = response.json()
    assert response.status_code == 403
    
    