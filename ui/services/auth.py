import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")
if not API_URL:
    raise RuntimeError("API_URL environment variable is not set")

def signup(username:str, password:str):
    response = requests.post(f"{API_URL}/signup", json={"username": username, "password": password})
    return response

def login(username:str, password:str):
    response = requests.post(f"{API_URL}/login", json={"username":username, "password":password})
    return response
