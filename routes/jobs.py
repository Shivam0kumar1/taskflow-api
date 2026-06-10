from fastapi import APIRouter, HTTPException, Depends
from models import Job, JobResponse
from database import get_connection, get_cursor
from routes.auth import get_current_user
from logger import logger
import requests

def send_job_notification(job_id, status):
    payload = {
        "job_id": job_id,
        "status": status
    }
    response = requests.post(
        "https://jsonplaceholder.typicode.com/posts",  #fake API designed for testing
        json=payload,
        timeout = 5
    )
    logger.info(
        f"Notification sent for job {job_id}. Status code={response.status_code}"
    )
    return response.status_code

router = APIRouter()

# # Temporary storage
# jobs = []

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
    conn = get_connection()
    cursor = get_cursor(conn)

    cursor.execute("SELECT id FROM users where username = %s",(user,))
    result = cursor.fetchone()
    if not result:
        logger.error(f"User not found during job creation:{user}")
        raise HTTPException(status_code=404, detail="User not found")
    user_id = result["id"]

    cursor.execute(
        "INSERT INTO jobs (title, description, status, user_id) values (%s,%s,%s,%s) RETURNING id",
        (job.title, job.description, "queued", user_id)
    )
    job_id = cursor.fetchone()["id"]
    conn.commit()

    logger.info(f"Job created by user: {user}")
    conn.close()

    return{
        "id": job_id,
        "title": job.title,
        "description": job.description,
        "status": "queued"
    }

# Get all jobs
# @router.get("/jobs", response_model=list[JobResponse])
@router.get("/jobs", response_model=list[JobResponse])
def get_jobs(page:int =1, limit: int=5, status: str=None, user: str=Depends(get_current_user)):
    conn = get_connection()
    cursor = get_cursor(conn)

    cursor.execute("SELECT id from users where username = %s",(user,))
    result = cursor.fetchone()
    if not result:
        logger.error(f"User not found:{user}")
        raise HTTPException(status_code=404, detail="User not found")
    user_id = result["id"]

    offset = (page-1)*limit

    if status not in [None, "queued", "processing", "completed", "failed"]:
        logger.warning(f"Invalid status filter used by user: {user}")
        raise HTTPException(status_code=400, detail="Invalid status.")
    if status:
        cursor.execute("SELECT * FROM jobs where user_id = %s ORDER BY id DESC AND status = %s LIMIT %s OFFSET %s", (user_id, status, limit, offset))
    else:
        cursor.execute("SELECT * FROM jobs where user_id = %s ORDER BY id DESC LIMIT %s OFFSET %s", (user_id, limit, offset))
    rows = cursor.fetchall()
    logger.info(f"Jobs fetched by user: {user}")
    conn.close()

    return [dict(row) for row in rows]

# Update job status
@router.put("/jobs/{job_id}", response_model=JobResponse)
def update_jobs(job_id:int, status:str, user: str=Depends(get_current_user)):
    if status not in VALID_STATUSES:
        logger.warning(f"Invalid status update attempted by user: {user}")
        raise HTTPException(status_code=400, detail="Invalid Job Status")

    conn = get_connection()
    cursor = get_cursor(conn)

    cursor.execute("SELECT id from users where username = %s",(user,))
    result = cursor.fetchone()
    if not result:
        logger.error(f"User not found:{user}")
        raise HTTPException(status_code=404, detail="User not found")
    user_id = result["id"]

    cursor.execute("SELECT * FROM jobs WHERE id = %s and user_id=%s", (job_id,user_id))
    row = cursor.fetchone()

    if not row:
        logger.warning(f"Job update failed. Job not found for user: {user}")
        conn.close()
        raise HTTPException(status_code=404, detail="Job not found")
        # return {"message": "Job not found"}
    current_status = row["status"]

    if status not in VALID_TRANSITIONS[current_status]:
        logger.warning(f"Invalid transition attempted by {user}: {current_status} -> {status}")
        conn.close()
        raise HTTPException(
            status_code=400,
            detail= f"Cannot change status from {current_status} to {status}"
        )

    cursor.execute("UPDATE jobs SET status = %s WHERE id = %s and user_id=%s", (status, job_id, user_id))
    conn.commit()

    notification_status = None
    if status == "completed":
        try:
            notification_status = send_job_notification(job_id, status)
        except Exception as e:
            logger.error(f"Notification failed for job {job_id}: {str(e)}")

    cursor.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
    updated_job = cursor.fetchone()
    logger.info(f"Job {job_id} updated to {status} by user: {user}")
    conn.close()

    job_data = dict(updated_job)
    # job_data["notification_status"] = notification_status  #only for testing
    return job_data

@router.delete("/jobs/{job_id}")
def delete_jobs(job_id: int, user: str=Depends(get_current_user)):
    conn= get_connection()
    cursor = get_cursor(conn)

    cursor.execute("SELECT id from users where username = %s",(user,))
    result = cursor.fetchone()
    if not result:
        logger.error(f"User not found:{user}")
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    user_id = result["id"]

    cursor.execute("SELECT * FROM jobs WHERE id = %s and user_id = %s", (job_id, user_id))
    row = cursor.fetchone()

    if not row:
        logger.warning(f"Delete failed. Job not found for user: {user}")
        conn.close()
        raise HTTPException(status_code=404, detail="Job not found")

    cursor.execute("DELETE FROM jobs WHERE id = %s and user_id = %s", (job_id, user_id))
    conn.commit()
    logger.info(f"Job {job_id} deleted by user: {user}")
    conn.close()

    return {"message": f"Job {job_id} deleted successfully"}