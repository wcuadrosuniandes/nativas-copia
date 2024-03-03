from uuid import uuid4
from datetime import datetime,timezone
from fastapi import APIRouter, Depends, status, HTTPException,Header
import re
from sqlmodel import Session, or_, select, text, delete

from typing import Optional,Annotated
from fastapi.responses import PlainTextResponse
from uuid import UUID, uuid4
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from ..dependencies import get_session,validate_user
from ..entities.post import Post, PostCreateOut, PostCreateIn,PostGetOut


router = APIRouter(prefix="/posts")

@router.post("", status_code=status.HTTP_201_CREATED, response_model=PostCreateOut)
async def create(*, session: Session = Depends(get_session), user = Depends(validate_user), post: PostCreateIn):
    print(user)
    current_utc_time = datetime.now(timezone.utc)
    
    if not post.expireAt or not post.routeId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El campo 'expireAt' no puede estar vacío."
        )
        
    try:
        expireAt_utc = post.expireAt.astimezone(timezone.utc)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El formato no es válido."
        )


    if expireAt_utc < current_utc_time:
        return JSONResponse(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            content=jsonable_encoder({"msg":"La fecha expiración no es válida"}),
        )
    post_db = Post(**post.model_dump())
    post_db.id = uuid4()
    post_db.userId = user["id"]
    session.add(post_db)
    session.commit()
    session.refresh(post_db)
    return post_db

@router.get("/ping", status_code=status.HTTP_200_OK, response_class=PlainTextResponse)
async def ping(*, session: Session = Depends(get_session)):
    session.exec(text("SELECT 1"))
    return "PONG"

@router.post("/reset", status_code=status.HTTP_200_OK)
async def reset(*, session: Session = Depends(get_session)):
    session.exec(delete(Post))
    session.commit()
    return {"msg": "Todos los datos fueron eliminados"}


@router.get("", status_code=status.HTTP_200_OK, response_model = list[PostGetOut])
async def get_posts(expire:Optional[bool] = None, route: Optional[str] = None,
                    owner: Optional[str] = None,session: Session = Depends(get_session),
                    user = Depends(validate_user),authorization: Optional[str] = Header(None)):
        
        query = select(Post)
        try: 
            if expire is not None:
                if expire:
                    query = query.where(Post.expireAt <= datetime.now())
                else:
                    query = query.where(Post.expireAt > datetime.now())

            if route is not None:
                query = query.where(Post.routeId == route)

            if owner is not None:
                if owner == "me":
                    owner_id = user["id"]
                else:
                    owner_id = owner
                
                query = query.where(Post.userId == owner_id)

            posts = session.exec(query).all()
            
            return posts
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El formato no es válido."
            )


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PostGetOut)
async def get_post(id,session: Session = Depends(get_session),
                    user = Depends(validate_user), authorization: Optional[str] = Header(None)):
    
    if not is_valid_uuid4(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El id no corresponde a un valor UUID"
        )
    
    post = session.exec(
            select(Post).where(
                Post.id == id
            )).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La publicación con ese id no existe.")
    return post
    
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_post(id, session: Session = Depends(get_session),user = Depends(validate_user)):
    if not is_valid_uuid4(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El id no corresponde a un valor UUID"
        )
    
    post = session.exec( select(Post).where( Post.id == id)).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La publicación con ese id no existe.")
    else:
        session.exec(delete(Post).where(Post.id == id))
        session.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder({"msg": "la publicación fue eliminada"}),
        )
    

def is_valid_uuid4(input):
    try:
        uuid_obj = UUID(input, version=4)
        return uuid_obj.version == 4
    except ValueError:
        return False