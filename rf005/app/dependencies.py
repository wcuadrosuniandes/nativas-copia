import os
from typing import Annotated
import httpx
from fastapi import Header, HTTPException, status

base_url = {
    "post": os.environ["POSTS_PATH"]+"/posts/",
    "route":os.environ["ROUTES_PATH"]+"/routes/",
    "offer":os.environ["OFFERS_PATH"]+"/offers?post=",
    "score":os.environ["SCORES_PATH"]+"/scores?post="
}



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
    

async def get_request(service ,id, auth):
    print(auth)
    if auth is None:
        raise HTTPException(status_code=403, detail="No hay token en la solicitud")
    url = base_url[service]+id
    print(url)
    client = httpx.AsyncClient(base_url=url)
    headers = {"Authorization": auth}
    try:
        r = await client.get( url, headers=headers)
        print(r)
        if r.is_success:
            return r.json()
        else:
            raise HTTPException(status_code=r.status_code, detail=service)
    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error de conexión al microservicio rutas",
        )
