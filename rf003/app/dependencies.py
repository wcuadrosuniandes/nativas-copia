import os
from typing import Annotated
import httpx

from fastapi import Header, HTTPException, status
from pydantic import TypeAdapter

from .entities.entities import (
    Route,
    CreateRouteIn,
    CreateRouteOut,
    CreatePostIn,
    PostCreateOut,
)

async def validate_user(authorization: Annotated[str | None, Header()] = None):
    if authorization is None:
        raise HTTPException(status_code=403, detail="No hay token en la solicitud")
    return await user_request(authorization)


async def user_request(auth: str):
    client = httpx.AsyncClient(base_url=os.environ["USERS_PATH"])
    headers = {"Authorization": auth}
    r = await client.get("/users/me", headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        raise HTTPException(status_code=401, detail="El token no es válido o está vencido.")
    

async def get_route(auth: str, flight_id):
    client = httpx.AsyncClient(base_url=os.environ["ROUTES_PATH"])
    headers = {"Authorization": auth}
    r = await client.get("/routes?flight="+ flight_id, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        raise HTTPException(status_code=401, detail=r.status_code)
    
async def get_routeAssociatedPost(auth: str, route_id):
    client = httpx.AsyncClient(base_url=os.environ["POSTS_PATH"])
    headers = {"Authorization": auth}
    r = await client.get("/posts?route="+ route_id, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        raise HTTPException(status_code=401, detail=r.status_code)
    

async def create_route(authorization, route: CreateRouteIn):
    if authorization is None:
        raise HTTPException(status_code=403, detail="No hay token en la solicitud")
    client = httpx.AsyncClient(base_url=os.environ["ROUTES_PATH"])
    headers = {"Authorization": authorization}

    try:
        adapter = TypeAdapter(CreateRouteOut)
        r = await client.post("/routes", headers=headers, json=route.model_dump())
        if r.is_success:
            return adapter.validate_json(r.text)
        else:
            raise HTTPException(status_code=r.status_code, detail=r.json())
    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error de conexión al microservicio rutas",
        )
    
async def delete_route(authorization, routeId):
    if authorization is None:
        raise HTTPException(status_code=403, detail="No hay token en la solicitud")
    client = httpx.AsyncClient(base_url=os.environ["ROUTES_PATH"])
    headers = {"Authorization": authorization}
    try:
        r = await client.delete("/routes/{}".format(routeId), headers=headers)
        if not r.is_success:
            raise HTTPException(status_code=r.status_code, detail=r.json())
    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error de conexión al microservicio publicación",
        )
    
async def create_post(authorization, post: CreatePostIn):
    if authorization is None:
        raise HTTPException(status_code=403, detail="No hay token en la solicitud")
    client = httpx.AsyncClient(base_url=os.environ["POSTS_PATH"])
    headers = {"Authorization": authorization}

    try:
        adapter = TypeAdapter(PostCreateOut)
        r = await client.post("/posts", headers=headers, json=post.model_dump())
        if r.is_success:
            return adapter.validate_json(r.text)
        else:
            delete_route(authorization, post.routeId)
            raise HTTPException(status_code=r.status_code, detail=r.json())
    except httpx.RequestError:
        delete_route(authorization, post.routeId)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error de conexión al microservicio publicaciones",
        )
    
