def test_signup(client):

    user = {
        "username":"pytest_user2",
        "password":"password123"
    }

    response = client.post("/signup", json=user)

    assert response.status_code == 200
    assert response.json() == {
        "message": "User created:"
    }