from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from jose import jwt

router = APIRouter()

users=[]
SECRET_KEY = "mysecretkey"

class User(BaseModel):
    username: str
    password: str

@router.post("/signup")
def signup(user: User):
    for u in users:
        if u["username"]==user.username:
            raise HTTPException(status_code=400, detail="User already exists")
    users.append(user.model_dump())
    return {"message": "User created:"}

@router.post("/login")
def login(user: User):
    for u in users:
        if u["username"] == user.username and u["password"]==user.password:
            token = jwt.encode({"username": user.username}, SECRET_KEY, algorithm="HS256")
            return {"access_token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")
