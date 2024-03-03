from sqlmodel import Session, or_, select, text, delete
from ..entities.route import Route
from typing import Union

def get_route(session: Session, id_route: str):
    return  session.exec(
        select(Route).where(
            Route.id == id_route
        )
    ).first()

def get_routes(session: Session, flightid: Union[str, None] = None):
    if flightid is not None:
        return session.exec(
            select(Route).where(
                Route.flightId == flightid
            )
        ).all()
    else: 
        return session.exec(
            select(Route)
        ).all()
    
def delete_route(session: Session, id_route: str):
    session.exec(    
        delete(Route).where(
            Route.id == id_route
        )
    )
    session.commit()
      
    