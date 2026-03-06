from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone

from app.database import get_database
from app.security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

class UserCreate(BaseModel):
    email: str
    password: str
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    name: str

@router.post("/signup", response_model=Token)
async def signup(user_data: UserCreate):
    db = get_database()
    
    # Check if user exists
    existing_user = await db["users"].find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    # Create new user
    user_dict = {
        "email": user_data.email,
        "hashed_password": get_password_hash(user_data.password),
        "name": user_data.name,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    result = await db["users"].insert_one(user_dict)
    user_id = str(result.inserted_id)
    
    # Generate token
    token = create_access_token(subject=user_id)
    return {
        "access_token": token,
        "user_id": user_id,
        "name": user_data.name
    }

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    db = get_database()
    
    user = await db["users"].find_one({"email": credentials.email})
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
        
    if not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
        
    # Generate token
    user_id = str(user["_id"])
    token = create_access_token(subject=user_id)
    
    return {
        "access_token": token,
        "user_id": user_id,
        "name": user["name"]
    }
