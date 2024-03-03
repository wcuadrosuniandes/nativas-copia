from datetime import datetime, timedelta
import pytz
import hashlib
import os
import re
from typing import Annotated
from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, HTTPException, Header, status
from fastapi.responses import PlainTextResponse
from sqlmodel import Session, or_, select, text, delete
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from ..dependencies import get_session, validate_user

from ..entities import queries
from ..entities.route import (
    Route,
    RouteCreateIn,
    RouteCreateOut,
    RouteOut
)

router = APIRouter(prefix="/routes")

@router.post("", status_code=201, response_model=RouteCreateOut)
async def create(*, session: Session = Depends(get_session), user = Depends(validate_user), route: RouteCreateIn):
    flightId_exist = session.exec(
        select(Route).where(
            Route.flightId == route.flightId
        )
    )
    if flightId_exist.first() is not None:
        return JSONResponse(
            status_code=412,
            content=jsonable_encoder({"msg":"Ya existe una ruta con ese mismo flightid"}),
        )
    try:
        start_date = route.plannedStartDate
        end_date = route.plannedEndDate
        date_now = datetime.now(pytz.utc)
        if (start_date > end_date or start_date < date_now or end_date < date_now ):
            return JSONResponse(
                status_code=412,
                content=jsonable_encoder({"msg":"Las fechas del trayecto no son válidas"}),
            )
    except ValueError:
        return JSONResponse(
            status_code=412,
            content=jsonable_encoder({"msg":"Las fechas del trayecto no son válidas"}),
        )
    route_db = Route(**route.model_dump())
    route_db.id = uuid4()
    session.add(route_db)
    session.commit()
    session.refresh(route_db)
    return route_db

@router.get("/ping", status_code=200, response_class=PlainTextResponse)
async def ping(*, session: Session = Depends(get_session)):
    session.exec(text("SELECT 1"))
    return "pong"

@router.post("/reset", status_code=200)
async def reset(*, session: Session = Depends(get_session)):
    session.exec(delete(Route))
    session.commit()
    return {"msg": "Todos los datos fueron eliminados"}

@router.get("", status_code=200, response_model= list[RouteOut])
async def get_routes( flight:str | None = None ,  session: Session = Depends(get_session), user = Depends(validate_user)):
    db_routes = queries.get_routes(session, flight)
    if len(db_routes) == 0:
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder(""),
        )
    return db_routes
    


@router.get("/{id_route}", status_code=200, response_model= RouteOut)
async def get_route( id_route, session: Session = Depends(get_session), user = Depends(validate_user)):
    if not is_valid_uuid4(id_route):
        raise HTTPException(
            status_code=400, detail="El id no corresponde a un valor UUID"
        )
    db_route = queries.get_route(session, id_route)
    if db_route is None:
        raise HTTPException(
            status_code=404, detail="El trayecto con ese id no existe."
        )
    return db_route
        
@router.delete("/{id_route}", status_code=200)
async def delete_route( id_route, session: Session = Depends(get_session), user = Depends(validate_user)):
    if not is_valid_uuid4(id_route):
        raise HTTPException(
            status_code=400, detail="El id no corresponde a un valor UUID"
        )
    if queries.get_route(session, id_route) is None:
        raise HTTPException(
            status_code=404, detail="El trayecto con ese id no existe."
        )
    else:
        queries.delete_route(session, id_route)
    return {"msg": "el trayecto fue eliminado"}



def is_valid_uuid4(input):
    try:
        uuid_obj = UUID(input, version=4)
        return uuid_obj.version == 4
    except ValueError:
        return False

