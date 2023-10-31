from fastapi import FastAPI

from fastapi_kafka.routers import user
from fastapi_kafka.routers import auth
from fastapi_kafka.database import Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(user.routes)
app.include_router(auth.routes)


@app.get("/")
async def root():
    return {'message': 'Hello World'}
