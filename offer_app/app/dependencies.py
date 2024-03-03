import os
from typing import Annotated
import httpx

from sqlalchemy import Engine
from sqlmodel import SQLModel, Session, create_engine
from fastapi import Header, HTTPException

class Database:
    _engine: Engine = None

    @staticmethod
    def get_engine() -> Engine:
        if not Database._engine:
            Database._engine = create_engine(
                f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
            )
        return Database._engine


def create_db_and_tables():
    SQLModel.metadata.create_all(Database.get_engine())


def get_session():
    with Session(Database.get_engine()) as session:
        yield session


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