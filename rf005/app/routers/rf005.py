import requests
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer
from ..dependencies import  validate_user, get_request

from ..entities.entities import (
    Point,
    Route,
    Rf005,
    DataOut
)

router = APIRouter(prefix="/rf005")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/ping", status_code=200)
async def ping():
    return "pong"


@router.get("/posts/{id_post}", status_code=200, response_model = DataOut)
async def get_post( *, id_post,  user = Depends(validate_user),  authorization: Annotated[str | None, Header()] = None):
    if not is_valid_uuid4(id_post):
        raise HTTPException(
            status_code=400, detail="El id no corresponde a un valor UUID"
        )
    post = await get_request("post", id_post, authorization)
    if(post['userId'] == user['id']):
        route = await get_request("route", post['routeId'], authorization)
        offers = await get_request("offer", id_post, authorization)
        scores = await get_request("score" ,id_post, authorization)
        route_model = Route(
            id=route['id'],
            flightId= route['flightId'],
            origin= Point(airportCode=route['sourceAirportCode'] , country=route['sourceCountry']),
            destiny= Point(airportCode=route['destinyAirportCode'] , country=route['destinyCountry']),
            bagCost= route['bagCost']
            )
        
        for offer in offers:
            for score in scores:
                if(offer["id"] == score["id"]):
                    offer['score'] =  score['profit']
                    break
                
        rf005 = Rf005(
            id= post['id'],
            expireAt= post['expireAt'],
            route= route_model, 
            plannedStartDate=route['plannedStartDate'],
            plannedEndDate=route['plannedEndDate'],
            createdAt=post['createdAt'],
            offers=sorted(offers, key=lambda x: x['score'], reverse=True ))
        
        return DataOut(data=rf005)
    else:
        raise HTTPException(
            status_code=403, detail="El usuario no tiene permiso para ver el contenido de la publicación"
        )
    
def is_valid_uuid4(input):
    try:
        uuid_obj = UUID(input, version=4)
        return uuid_obj.version == 4
    except ValueError:
        return False
    


