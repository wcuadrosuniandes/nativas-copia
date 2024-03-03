from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select,delete,text
from fastapi.responses import JSONResponse,PlainTextResponse
from fastapi.encoders import jsonable_encoder

from ..dependencies import get_session, validate_user
from ..entities.score import Score, ScoreCreateIn, ScoreOut
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/scores")

@router.post("", status_code=status.HTTP_201_CREATED)
async def post_score(
    *,
    session: Session = Depends(get_session),
    user=Depends(validate_user),
    score: ScoreCreateIn
):

    existing_score = session.exec(select(Score).where(Score.id == score.id)).first()
    if existing_score:
        return JSONResponse(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            content=jsonable_encoder({"msg":"Ya existe un score con ese mismo id"}),
        )
    
    scoreDB = Score(**score.model_dump())
    scoreDB.userId = user["id"]
    scoreDB.calculate_profit()
    session.add(scoreDB)
    session.commit()
    session.refresh(scoreDB)
    return {"msg": "Score Calculado exitosamente"}

@router.get("/ping", status_code=status.HTTP_200_OK, response_class=PlainTextResponse)
async def ping(*, session: Session = Depends(get_session)):
    session.exec(text("SELECT 1"))
    return "PONG"


@router.post("/reset", status_code=status.HTTP_200_OK)
async def reset(*, session: Session = Depends(get_session)):
    session.exec(delete(Score))
    session.commit()
    return {"msg": "Todos los datos fueron eliminados"}


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ScoreOut)
async def get_post_by_offer(
    id, session: Session = Depends(get_session), _=Depends(validate_user)
):
    
    score = session.exec(select(Score).where(Score.id == id)).first()
    if score is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No tenemos información para esa oferta"
        )
    return score


@router.get("", status_code=status.HTTP_200_OK, response_model=list[ScoreOut])
async def get_scores(
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

    try:
        return session.exec(select(Score).filter_by(**filters)).all()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El formato no es válido."
        )
    