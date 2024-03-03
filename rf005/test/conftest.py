import os
import re
from typing import Annotated
from faker import Faker
from fastapi import HTTPException, Header
from fastapi.testclient import TestClient
from httpx import Request, Response
import pytest
import respx

from app.main import app
from app.dependencies import validate_user
from .mock_data  import user, post, route, offers, scores, post_alt

def post_get(request: Request):
    code = 200
    json = None
    postpattern = re.compile("/posts/(.*)")
    post_id = postpattern.search(request.url.path).group(1)
    print(post_id)
    response_token = validate_token(request)
    if response_token[0] != 200:
        code = response_token[0]
        json = response_token[1]
    elif post_id == "no_valido":
        code = 400
        json = {"msg": "El id de post es inválido"}
    if ( post_id != post['id'] and post_id != post_alt['id'] ):
        code = 404
        json = {"msg": "No existe la publicación"}
    elif post_id == post['id']:
        json = post
    elif post_id == post_alt['id']:
        json = post_alt
    return Response(code, json=json)


def route_get(request: Request):
    code = 200
    json = route
    return Response(code, json=json)


def offers_get(request: Request):
    code = 200
    response_token = validate_token(request)
    if response_token[0] != 200:
        code = response_token[0]
        json = response_token[1]
    else:
        json =  offers
    return Response(code, json=json)


def score_get(request: Request):
    code = 200
    response_token = validate_token(request)
    if response_token[0] != 200:
        code = response_token[0]
        json = response_token[1]
    else:
        json =  scores
    return Response(code, json=json)


@pytest.fixture(name="client")
def client_fixture():
    async def validate_user_override(
        authorization: Annotated[str | None, Header()] = None
    ):
        print('over')
        if authorization is None:
            raise HTTPException(status_code=500, detail="No hay token en la solicitud")
        elif authorization == "bearer":
            return user
        else:
            raise HTTPException(
                status_code=401, detail="El token no es válido o está vencido."
            )

    app.dependency_overrides[validate_user] = validate_user_override
    client = TestClient(app)
    yield client


@pytest.fixture
def fake():
    return Faker()



@pytest.fixture
def routes_api():
    with respx.mock(
        base_url=os.environ["ROUTES_PATH"], assert_all_called=False
    ) as respx_mock:
        respx_mock.get("/routes/"+route['id'], name="route_get").mock(side_effect=route_get)
        yield respx_mock



@pytest.fixture
def posts_api():
    with respx.mock(
        base_url=os.environ["POSTS_PATH"], assert_all_called=False
    ) as respx_mock:
        respx_mock.get("/posts/"+post['id'], name="post_get").mock(side_effect=post_get)
        respx_mock.get("/posts/"+post_alt['id'], name="post_get_other_owner").mock(side_effect=post_get)
        yield respx_mock


@pytest.fixture
def offers_api():
    with respx.mock(
        base_url=os.environ["OFFERS_PATH"], assert_all_called=False
    ) as respx_mock:
        respx_mock.get("/offers?post={}".format(post['id']), name="offers_get").mock(side_effect=offers_get)
        yield respx_mock


@pytest.fixture
def scores_api():
    with respx.mock(
        base_url=os.environ["SCORES_PATH"], assert_all_called=False
    ) as respx_mock:
        respx_mock.get("/scores?post={}".format(post['id']), name="score_get").mock(side_effect=score_get)
        yield respx_mock



def validate_token(request: Request):
    code = 200
    json = None
    print('validation')
    if "Authorization" not in request.headers:
        code = 404
        json = {"msg": "El token no existe"}
    elif request.headers["Authorization"] != "bearer":
        code = 408
        json = {"msg": "El token no es válidoss"}
    return [code, json]
    