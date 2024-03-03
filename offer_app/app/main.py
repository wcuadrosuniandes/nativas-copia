from dotenv import load_dotenv

loaded = load_dotenv('.env.development')

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


from .dependencies import create_db_and_tables
from .routers import offers


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_message = {
        "detail": "Alguno de los campos no está presente en la solicitud, o no tienen el formato esperado."
    }
    for error in exc.errors():
        if ("size" in error["loc"] and error["type"] == "enum") or (
            "offer" in error["loc"] and error["type"] == "greater_than"
        ):
            return JSONResponse(
                status_code=status.HTTP_412_PRECONDITION_FAILED, content=error_message
            )
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_message)

app.include_router(offers.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)