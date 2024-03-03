import os
from typing import Annotated
import httpx
import logging
from fastapi import Header, HTTPException, status
from pydantic import TypeAdapter

from .entities.entities import (
    CreateOfferIn,
    CreateOfferOut,
    PostGetOut,
    RouteOut,
    ScoreCreateIn,
    UserMeOut,
)


def log_and_raise_error(name):
    logging.error("Error de conexión al microservicio {}".format(name))
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Error de conexión al microservicio {}".format(name),
    )


async def validate_user(authorization: Annotated[str | None, Header()] = None):
    if authorization is None:
        raise HTTPException(status_code=403, detail="No hay token en la solicitud")
    client = httpx.AsyncClient(base_url=os.environ["USERS_PATH"], timeout=5.0)
    headers = {"Authorization": authorization}
    try:
        adapter = TypeAdapter(UserMeOut)
        r = await client.get("/users/me", headers=headers)
        if r.is_success:
            return adapter.validate_json(r.text)
        elif r.status_code >= 400 and r.status_code < 500:
            raise HTTPException(status_code=r.status_code, detail=r.json())
        else:
            log_and_raise_error("usuarios")
    except httpx.RequestError:
        log_and_raise_error("usuarios")


async def get_post(id, authorization: Annotated[str | None, Header()] = None):
    if authorization is None:
        raise HTTPException(status_code=403, detail="No hay token en la solicitud")
    client = httpx.AsyncClient(base_url=os.environ["POSTS_PATH"])
    headers = {"Authorization": authorization}
    try:
        adapter = TypeAdapter(PostGetOut)
        r = await client.get("/posts/{}".format(id), headers=headers)
        if r.is_success:
            return adapter.validate_json(r.text)
        elif r.status_code >= 400 and r.status_code < 500:
            raise HTTPException(status_code=r.status_code, detail=r.json())
        else:
            log_and_raise_error("publicaciones")
    except httpx.RequestError:
        log_and_raise_error("publicaciones")


async def get_route(authorization, id):
    if authorization is None:
        raise HTTPException(status_code=403, detail="No hay token en la solicitud")
    client = httpx.AsyncClient(base_url=os.environ["ROUTES_PATH"])
    headers = {"Authorization": authorization}
    try:
        adapter = TypeAdapter(RouteOut)
        r = await client.get("/routes/{}".format(id), headers=headers)
        if r.is_success:
            return adapter.validate_json(r.text)
        elif r.status_code >= 400 and r.status_code < 500:
            raise HTTPException(status_code=r.status_code, detail=r.json())
        else:
            log_and_raise_error("rutas")
    except httpx.RequestError:
        log_and_raise_error("rutas")


async def create_offer(authorization, offer: CreateOfferIn):
    if authorization is None:
        raise HTTPException(status_code=403, detail="No hay token en la solicitud")
    client = httpx.AsyncClient(base_url=os.environ["OFFERS_PATH"])
    headers = {"Authorization": authorization}
    try:
        offer.size = offer.size.value
        adapter = TypeAdapter(CreateOfferOut)
        r = await client.post("/offers", headers=headers, json=offer.model_dump())
        if r.is_success:
            return adapter.validate_json(r.text)
        elif r.status_code >= 400 and r.status_code < 500:
            raise HTTPException(status_code=r.status_code, detail=r.json())
        else:
            log_and_raise_error("ofertas")
    except httpx.RequestError:
        log_and_raise_error("ofertas")


async def delete_offer(authorization, offerId):
    if authorization is None:
        raise HTTPException(status_code=403, detail="No hay token en la solicitud")
    client = httpx.AsyncClient(base_url=os.environ["OFFERS_PATH"])
    headers = {"Authorization": authorization}
    try:
        r = await client.delete("/offers/{}".format(offerId), headers=headers)
        if not r.is_success:
            raise HTTPException(status_code=r.status_code, detail=r.json())
    except httpx.RequestError:
        log_and_raise_error("ofertas")


async def create_score(authorization, score: ScoreCreateIn):
    if authorization is None:
        raise HTTPException(status_code=403, detail="No hay token en la solicitud")
    client = httpx.AsyncClient(base_url=os.environ["SCORES_PATH"])
    headers = {"Authorization": authorization}
    try:
        r = await client.post("/scores", headers=headers, json=score.model_dump())
        if not r.is_success:
            await delete_offer(authorization, score.id)
            raise HTTPException(status_code=r.status_code, detail=r.json())
    except Exception:
        log_and_raise_error("score")
