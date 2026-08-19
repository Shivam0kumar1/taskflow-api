import requests

API_URL = "http://localhost:8000"

def get_jobs(token:str, page:int=1, limit:int=5, status:str=None):
    params = {
        "page": page,
        "limit": limit
    }
    if status:
        params["status"] = status
    return requests.get(f"{API_URL}/jobs", headers = {"Authorization": f"Bearer {token}"}, params = params)

def create_jobs(token:str, title:str, description:str):
    response = requests.post(f"{API_URL}/jobs", headers = {"Authorization": f"Bearer {token}"}, json={"title": title, "description": description})
    return response

def update_jobs(token:str, job_id:str, status:str):
    response = requests.put(f"{API_URL}/jobs/{job_id}", headers={"Authorization": f"Bearer {token}"} ,params = {"status": status})
    return response

def delete_jobs(token:str, job_id:str):
    return requests.delete(f"{API_URL}/jobs/{job_id}", headers={"Authorization": f"Bearer {token}"})
