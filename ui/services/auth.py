import requests

API_URL = "http://localhost:8000"

def signup(username:str, password:str):
    response = requests.post(f"{API_URL}/signup", json={"username": username, "password": password})
    return response

def login(username:str, password:str):
    response = requests.post(f"{API_URL}/login", json={"username":username, "password":password})
    return response
