from fastapi import FastAPI
from routes.jobs import router as jobs_router

app = FastAPI()

@app.get("/")
def home():
    return {"message": "My backend is running"}

app.include_router(jobs_router)