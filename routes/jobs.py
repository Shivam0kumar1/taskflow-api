from fastapi import APIRouter, HTTPException, Depends
from models import Job, JobResponse
from database import get_connection
from routes.auth import get_current_user

router = APIRouter()

# Temporary storage
jobs = []

VALID_STATUSES=["queued","processing","completed","failed"]

VALID_TRANSITIONS = {
    "queued": ["processing"],
    "processing": ["completed", "failed"],
    "completed": [],
    "failed": []
}

# Create Job
@router.post("/jobs", response_model = JobResponse)
def create_job(job:Job, user: str=Depends(get_current_user)):
    comm = get_connection()
    cursor = comm.cursor()

    cursor.execute(
        "INSERT INTO jobs (title, description, status) values (?,?,?)",
        (job.title, job.description, "queued")
    )
    comm.commit()

    job_id = cursor.lastrowid
    comm.close()

    return{
        "id": job_id,
        "title": job.title,
        "description": job.description,
        "status": "queued"
    }

# Get all jobs
# @router.get("/jobs", response_model=list[JobResponse])
@router.get("/jobs", response_model=list[JobResponse])
def get_jobs(user: str=Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs")
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

# Update job status
@router.put("/jobs/{job_id}", response_model=JobResponse)
def update_jobs(job_id:int, status:str, user: str=Depends(get_current_user)):
    if status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid Job Status")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Job not found")
        # return {"message": "Job not found"}
    current_status = row["status"]

    if status not in VALID_TRANSITIONS[current_status]:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail= f"Cannot change status from {current_status} to {status}"
        )

    cursor.execute("UPDATE jobs SET status = ? WHERE id = ?", (status, job_id))
    conn.commit()

    cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    updated_job = cursor.fetchone()
    conn.close()
    return dict(updated_job)

@router.delete("/jobs/{jobs_id}")
def delete_jobs(job_id: int, user: str=Depends(get_current_user)):
    conn= get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Job not found")

    cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()

    return {"message": f"Job {job_id} deleted successfully"}