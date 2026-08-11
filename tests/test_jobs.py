def test_create_job(client, auth_headers):
    response = client.post(
        "/jobs",
        headers=auth_headers,
        json={
            "title":"Learn FastAPI",
            "description":"Complete pytest tutorial"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"]=="Learn FastAPI"
    assert data["description"]=="Complete pytest tutorial"
    assert data["status"]=="queued"
    assert "id" in data

def test_get_jobs(client,auth_headers):
    response=client.post("/jobs", headers=auth_headers, json={"title":"Job 1", "description":"First Job."})
    assert response.status_code == 200
    response=client.post("/jobs", headers=auth_headers, json={"title":"Job 2", "description":"Second Job."})
    assert response.status_code == 200

    response = client.get(
        "/jobs",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data)==2

    assert data[0]["title"]=="Job 2"
    assert data[1]["title"]=="Job 1"

    assert data[0]["status"]=="queued"
    assert data[1]["status"]=="queued"

def test_update_job(client, auth_headers):
    create_response = client.post("/jobs", headers=auth_headers, json={"title":"Job 1", "description":"First Job."})
    assert create_response.status_code == 200
    job_id = create_response.json()["id"]

    update_response = client.put(f"/jobs/{job_id}", headers=auth_headers, params={"status": "processing"})
    assert update_response.status_code == 200

    data = update_response.json()
    assert data["title"] == "Job 1"
    assert data["description"] == "First Job."
    assert data["status"] == "processing"

    update_response = client.put(f"/jobs/{job_id}", headers=auth_headers, params={"status": "completed"})
    assert update_response.status_code == 200

    data = update_response.json()
    assert data["status"] == "completed"

def test_delete_jobs(client, auth_headers):
    create_response = client.post("/jobs", headers=auth_headers, json={"title":"Job 1", "description":"First Job."})
    assert create_response.status_code == 200
    # print(create_response.json()["id"])
    first_job = create_response.json()["id"]
    create_response = client.post("/jobs", headers=auth_headers, json={"title":"Job 2", "description":"second Job."})
    assert create_response.status_code == 200
    # print(create_response.json()["id"])

    job_id = first_job

    delete_response =  client.delete(f"/jobs/{job_id}", headers=auth_headers)
    assert delete_response.status_code == 200

    get_response = client.get("/jobs", headers = auth_headers)
    assert get_response.status_code == 200
    data = get_response.json()

    assert len(data)==1
    assert data[0]["title"] == "Job 2"
    assert data[0]["description"] == "second Job."

def test_unauthorized_get_jobs(client):
    response = client.get("/jobs")
    assert response.status_code == 401

def test_update_nonexistent_job(client,auth_headers):
    response = client.put("/jobs/999999", headers=auth_headers, params={"status": "queued"})
    assert response.status_code == 404

def test_delete_nonexistent_job(client,auth_headers):
    response = client.delete("/jobs/999999", headers=auth_headers)
    assert response.status_code == 404

def test_user_cannot_modify_other_users_job(client):
    user_a={"username":"user1", "password":"password123"}
    user_b={"username":"user2", "password":"password123"}

    signup_response_a = client.post("/signup",json=user_a)
    signup_response_b = client.post("/signup",json=user_b)

    assert signup_response_a.status_code == 200
    assert signup_response_b.status_code == 200

    login_response_a = client.post("/login",json=user_a)
    assert login_response_a.status_code == 200
    jwt_a = login_response_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {jwt_a}"}
    login_response_b = client.post("/login",json=user_b)
    assert login_response_b.status_code == 200
    jwt_b = login_response_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {jwt_b}"}

    createjob_response_a = client.post("/jobs", headers = headers_a , json={"title":"Job 1", "description":"First Job."})
    assert createjob_response_a.status_code == 200
    job_id_a = createjob_response_a.json()["id"]

    update_job_response_a = client.put(f"/jobs/{job_id_a}", headers = headers_b, params={"status":"processing"})
    assert update_job_response_a.status_code == 404