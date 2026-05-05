from fastapi import FastAPI
from routes.jobs import router as jobs_router
from routes.auth import router as auth_router

app = FastAPI()

@app.get("/")
def home():
    return {"message": "My backend is running"}

app.include_router(jobs_router)
app.include_router(auth_router)