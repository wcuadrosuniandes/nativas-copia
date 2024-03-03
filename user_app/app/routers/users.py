from datetime import datetime, timedelta
import hashlib
import os
import re
from typing import Annotated
from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, HTTPException, Header, status
from fastapi.responses import PlainTextResponse
from sqlmodel import Session, or_, select, text, delete
from ..dependencies import get_session

from ..entities.user import (
    StatusEnum,
    User,
    UserCreateIn,
    UserCreateOut,
    UserAuthIn,
    UserAuthOut,
    UserMeOut,
    UserUpdateIn,
)

router = APIRouter(prefix="/users")


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserCreateOut)
async def create(*, session: Session = Depends(get_session), user: UserCreateIn):
    user_exists = session.exec(
        select(User).where(
            or_(User.username == user.username, User.email == user.email)
        )
    )

    if user_exists.first() is not None:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Ya existe un usuario con ese nombre o correo",
        )

    user_db = User(**user.model_dump())
    user_db.id = uuid4()
    user_db.salt = os.urandom(32).hex()
    user_db.password = hash_password(user_db.password, user_db.salt)
    user_db.status = StatusEnum.NO_VERIFICADO
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserMeOut)
async def me(
    *,
    session: Session = Depends(get_session),
    authorization: Annotated[str | None, Header()] = None,
):
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado"
        )
    match = re.search(r"Bearer\s+(.+)", authorization)
    if not is_valid_uuid4(match.group(1)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Acceso denegado"
        )
    db_user = session.exec(
        select(User).where(
            User.token == match.group(1), User.expireAt >= datetime.utcnow()
        )
    ).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Acceso denegado"
        )

    return db_user


@router.get("/ping", status_code=status.HTTP_200_OK, response_class=PlainTextResponse)
async def ping(*, session: Session = Depends(get_session)):
    session.exec(text("SELECT 1"))
    return "PONG"


@router.post("/reset", status_code=status.HTTP_200_OK)
async def reset(*, session: Session = Depends(get_session)):
    session.exec(delete(User))
    session.commit()
    return {"msg": "Todos los datos fueron eliminados"}


@router.post("/auth", status_code=status.HTTP_200_OK, response_model=UserAuthOut)
async def auth(*, session: Session = Depends(get_session), auth_data: UserAuthIn):
    db_user = session.exec(
        select(User).where(User.username == auth_data.username)
    ).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario / Contraseña no existe")
    input_hash = hash_password(auth_data.password, db_user.salt)
    if input_hash != db_user.password:
        raise HTTPException(status_code=404, detail="Usuario / Contraseña no existe")
    db_user.expireAt = datetime.utcnow() + timedelta(hours=1)
    db_user.token = uuid4()
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.patch("/{id}")
async def update(
    *, session: Session = Depends(get_session), id: UUID, user: UserUpdateIn
):
    db_user = session.get(User, id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    hero_data = user.model_dump(exclude_unset=True)
    if len(hero_data) == 0:
        raise HTTPException(
            status_code=400, detail="Debe enviar la modificación de al menos un campo"
        )
    for key, value in hero_data.items():
        setattr(db_user, key, value)
    db_user.updateAt = datetime.utcnow()
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return {"msg": "el usuario ha sido actualizado"}


def hash_password(password, salt_hex):
    salt = bytes.fromhex(salt_hex)
    hashed_password = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, 100000
    )
    return hashed_password.hex()


def is_valid_uuid4(input):
    try:
        uuid_obj = UUID(input, version=4)
        return uuid_obj.version == 4
    except ValueError:
        return False
