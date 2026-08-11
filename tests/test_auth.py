def test_signup(client):

    user = {
        "username":"pytest_user2",
        "password":"password123"
    }

    response = client.post("/signup", json=user)

    assert response.status_code == 200
    assert response.json() == {
        "message": "User created."
    }

def test_login(auth_headers):
    assert "Authorization" in auth_headers

def test_duplicate_signup(client):
    user = {"username":"duplicate_user2", "password":"password123"}

    first_response = client.post("/signup",json=user)
    assert first_response.status_code == 200

    second_response = client.post("/signup",json=user)
    assert second_response.status_code == 400
    assert second_response.json()["detail"]=="User already exists"

def test_invalid_login(client):
    user = {"username":"user1", "password":"password123"}
    signup_response = client.post("/signup",json=user)
    assert signup_response.status_code == 200

    login_response = client.post("/login",json={"username":"invaliduser", "password":"password123"})
    assert login_response.status_code == 401
    assert login_response.json()["detail"]=="Invalid credentials"

    login_response = client.post("/login",json={"username":"user1", "password":"invalid_password"})
    assert login_response.status_code == 401
    assert login_response.json()["detail"]=="Invalid credentials"

