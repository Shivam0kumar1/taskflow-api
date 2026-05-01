from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Temporary storage
jobs = []

# Schema (data structure)
class Job(BaseModel):
    title: str
    description: str

@app.get("/")
def home():
    return {"message": "My backend is running"}

# Create Job
@app.post("/jobs")
def create_job(job:Job):
    job_data = job.model_dump()
    job_data["id"] = len(jobs)+1
    job_data["status"] = "queued"
    jobs.append(job_data)
    return job_data

# Get all jobs
@app.get("/jobs")
def get_jobs():
    return jobs


