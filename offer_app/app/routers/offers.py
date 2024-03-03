from uuid import uuid4, UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from sqlmodel import Session, select, text, delete

from ..dependencies import get_session, validate_user

from ..entities.offer import Offer, OfferCreateOut, OfferCreateIn, OfferViewFilterOut, SizeEnum
from pydantic import ValidationError

router = APIRouter(prefix="/offers")
    
@router.post("", status_code=status.HTTP_201_CREATED, response_model=OfferCreateOut)
async def create( *, session: Session = Depends(get_session), user=Depends(validate_user), offer: OfferCreateIn):
            
    offer_db = Offer(**offer.model_dump())
    offer_db.userId = user["id"]
    offer_db.id = uuid4()
    session.add(offer_db)
    session.commit()
    session.refresh(offer_db)
    return offer_db


@router.get("", response_model=list[OfferViewFilterOut])
async def get_offers(
    post: str = None,
    owner: str = None,
    session: Session = Depends(get_session),
    user=Depends(validate_user),
):
    filters = {}
    if post:
        filters["postId"] = str(post)
    if owner:
        if owner == "me":
            owner = user["id"]
        filters["userId"] = owner

    offers = session.exec(select(Offer).filter_by(**filters)).all()

    offers_data = []
    for offer in offers:
        offer_data = OfferViewFilterOut(
            id=offer.id,
            postId=str(offer.postId),
            description=offer.description,
            size=offer.size,
            fragile=offer.fragile,
            offer=offer.offer,
            createdAt=offer.createdAt,
            userId=offer.userId,
        )
        offers_data.append(offer_data)

    return offers_data


@router.get("/ping", status_code=status.HTTP_200_OK, response_class=PlainTextResponse)
async def ping(*, session: Session = Depends(get_session)):
    session.exec(text("SELECT 1"))
    return "PONG"


@router.post("/reset", status_code=status.HTTP_200_OK)
async def reset(*, session: Session = Depends(get_session)):
    session.exec(delete(Offer))
    session.commit()
    return {"msg": "Todos los datos fueron eliminados"}


@router.get("/{id}", response_model=OfferViewFilterOut)
async def get_offer(
    id: str, session: Session = Depends(get_session), user=Depends(validate_user)
):
    is_valid_uuid4(id)
    offer = session.exec(select(Offer).filter_by(id=id)).first()

    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La oferta con ese ID no existe.",
        )

    offer_data = OfferViewFilterOut(
        id=offer.id,
        postId=str(offer.postId),
        description=offer.description,
        size=offer.size,
        fragile=offer.fragile,
        offer=offer.offer,
        createdAt=offer.createdAt,
        userId=offer.userId,
    )

    return offer_data


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_offer(
    id: str, session: Session = Depends(get_session), user=Depends(validate_user)
):
    is_valid_uuid4(id)    
    offer = session.exec(select(Offer).filter_by(id=id)).first()

    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La oferta con ese ID no existe.",
        )

    session.delete(offer)
    session.commit()

    return {"msg": "la oferta fue eliminada"}


def is_valid_uuid4(id):
    try:
        UUID(id, version=4)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El id no es un valor string con formato uuid.",
        )
