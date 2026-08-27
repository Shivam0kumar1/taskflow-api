from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes.jobs import router as jobs_router
from routes.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # from init_postgres import init_postgresql
    # init_postgresql()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],   # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "My backend is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(jobs_router)
app.include_router(auth_router)