from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Header
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse

from ..dependencies import (
    create_offer,
    create_score,
    get_post,
    get_route,
    validate_user,
)

from ..entities.entities import (
    CreateOfferIn,
    OfferData,
    Rf004In,
    Rf004Out,
    ScoreCreateIn,
)


router = APIRouter(prefix="/rf004")


@router.get("/ping", status_code=status.HTTP_200_OK, response_class=PlainTextResponse)
async def ping():
    return "PONG"


@router.post(
    "/posts/{id}/offers",
    status_code=status.HTTP_201_CREATED,
    response_model=Rf004Out,
)
async def create(
    *,
    user=Depends(validate_user),
    post=Depends(get_post),
    rf004: Rf004In,
    authorization: Annotated[str | None, Header()] = None
):
    if user.id == post.userId:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="La publicación es del mismo usuario.",
        )

    if datetime.now() > post.expireAt:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="La publicación ya expiró.",
        )

    route = await get_route(authorization, post.routeId)
    offer = CreateOfferIn(**rf004.model_dump(), postId=str(post.id))
    offer_create_response = await create_offer(authorization, offer)

    score = ScoreCreateIn(
        id=str(offer_create_response.id),
        offer=offer.offer,
        postId=str(post.id),
        size=rf004.size,
        bagCost=route.bagCost,
    )
    await create_score(authorization, score)
    data = OfferData(**offer_create_response.model_dump(), postId=post.id)
    return Rf004Out(data=data, msg="Mensaje de prueba")
