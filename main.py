from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes.jobs import router as jobs_router
from routes.auth import router as auth_router
from logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    from init_postgres import init_postgresql
    # init_db() # PostgreSQL tables already created
    init_postgresql()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"message": "My backend is running"}

app.include_router(jobs_router)
app.include_router(auth_router)