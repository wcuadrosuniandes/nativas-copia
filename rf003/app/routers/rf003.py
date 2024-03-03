from datetime import datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Header
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, PlainTextResponse

from ..dependencies import (
    validate_user,
    get_route,
    get_routeAssociatedPost,
    create_route,
    create_post,
    delete_route,
)

from ..entities.entities import (
    CreatePostIn,
    Route,
    RouteA,
    CreateRouteIn,
    CreateRouteOut,
    PostData,
    Rf003In,
    Rf003Out,
)

router = APIRouter(prefix="/rf003")


@router.get("/ping", status_code=status.HTTP_200_OK, response_class=PlainTextResponse)
async def ping():
    return "PONG"

@router.post(
    "/posts",
    status_code=status.HTTP_201_CREATED,
    response_model=Rf003Out,
)
async def create(
    *,
    user=Depends(validate_user),
    rf003: Rf003In,
    authorization: Annotated[str | None, Header()] = None
):

    planned_start_date = rf003.plannedStartDate.replace(tzinfo=timezone.utc).isoformat()
    planned_end_date = rf003.plannedEndDate.replace(tzinfo=timezone.utc).isoformat()

    current_time = datetime.now(timezone.utc).isoformat()

    if (
        planned_start_date <= current_time
        or planned_end_date <= current_time
        or planned_start_date >= planned_end_date
    ):
        return JSONResponse(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            content=jsonable_encoder({"msg": "Las fechas del trayecto no son válidas"}),
        )

    route = await get_route(authorization, rf003.flightId)

    if route:
        for routes in route:
            id = routes["id"]
            validatePostinroute = await get_routeAssociatedPost(authorization, id)

        if not validatePostinroute:
            formatted_expire_at = rf003.expireAt.strftime("%Y-%m-%dT%H:%M:%S")
            current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            if formatted_expire_at <= current_time:
                return JSONResponse(
                    status_code=status.HTTP_412_PRECONDITION_FAILED,
                    content=jsonable_encoder(
                        {"msg": "La fecha expiración no es válida"}
                    ),
                )

            post = CreatePostIn(
                routeId=id,
                expireAt=formatted_expire_at,
            )
            post_create_response = await create_post(authorization, post)

            routea = RouteA(id=id, createdAt=formatted_expire_at)

            data = PostData(
                id=post_create_response.id,
                userId=post_create_response.userId,
                createdAt=post_create_response.createdAt,
                expireAt=formatted_expire_at,
                route=routea,
            )
            return Rf003Out(data=data, msg="Publicación creada con éxito")

        else:
            return JSONResponse(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                content=jsonable_encoder(
                    {"msg": "El usuario ya tiene una publicación para la misma fecha"}
                ),
            )

    else:
        formatted_expire_at = rf003.expireAt.strftime("%Y-%m-%dT%H:%M:%S")
        current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        if formatted_expire_at <= current_time:
            return JSONResponse(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                content=jsonable_encoder({"msg": "La fecha expiración no es válida"}),
            )
        route = CreateRouteIn(
            flightId=rf003.flightId,
            sourceAirportCode=rf003.origin.airportCode,
            sourceCountry=rf003.origin.country,
            destinyAirportCode=rf003.destiny.airportCode,
            destinyCountry=rf003.destiny.country,
            bagCost=rf003.bagCost,
            plannedStartDate=rf003.plannedStartDate.isoformat(),
            plannedEndDate=rf003.plannedEndDate.isoformat(),
        )

        route_create_response = await create_route(authorization, route)

        post = CreatePostIn(
            routeId=route_create_response.id, expireAt=formatted_expire_at
        )
        post_create_response = await create_post(authorization, post)

        routea = RouteA(id=route_create_response.id, createdAt=formatted_expire_at)

        data = PostData(
            id=post_create_response.id,
            userId=post_create_response.userId,
            createdAt=post_create_response.createdAt,
            expireAt=formatted_expire_at,
            route=routea,
        )
        return Rf003Out(data=data, msg="Publicación creada con éxito")
