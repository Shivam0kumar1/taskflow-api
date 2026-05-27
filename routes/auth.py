from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import jwt
from security import hash_password, verify_password
from database import get_connection
from config import SECRET_KEY, ALGORITHM
from logger import logger

router = APIRouter()
security = HTTPBearer()

# users=[]

class User(BaseModel):
    username: str
    password: str

@router.post("/signup")
def signup(user: User):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * from users where username = ?",(user.username,))
    existing_user = cursor.fetchone()

    if existing_user:
        logger.warning(f"Signup failed - user already exists: {user.username}")
        conn.close()
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user.password)

    cursor.execute("insert into users (username, password) values (?,?)", (user.username, hashed_password))
    conn.commit()
    logger.info(f"New user created: {user.username}")
    conn.close()
    return {"message": "User created:"}

@router.post("/login")
def login(user: User):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("select * from users where username = ?", (user.username,))
    db_user = cursor.fetchone()

    conn.close()

    if not db_user:
        logger.warning(f"Login failed - user doesn't exist: {user.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(user.password, db_user["password"]):
        logger.warning(f"Login failed - wrong password for user: {user.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({"username": user.username}, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"User logged in: {user.username}")
    return {"access_token": token}


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["username"]
    except:
        logger.error(f"Invalid JWT token")
        raise HTTPException(status_code=401, detail="Invalid credentials")