

from fastapi import APIRouter, HTTPException
from backend.app.database import UserData
from backend.app.schemas import User
from backend.app.utils import hash_password
import jwt
from config_file import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from backend.app.models import Token
from datetime import datetime, timedelta, timezone

router = APIRouter()

@router.post("/register")
async def register_user(email: str, password: str):
    user_data_obj = UserData()
    response = user_data_obj.add_user(email=email, password=password) # Password hasing is taken care of
    if "error" in response:
        raise HTTPException(status_code=response["status_code"], detail=response["error"])
    
    return response


@router.post("/login", response_model=Token, status_code=200)
async def login(username: str, password: str):
    """Returns a JWT token if the user is authenticated"""
    breakpoint()
    user_data_obj = UserData()
    data: User = user_data_obj.get_user(email=username)
    
    if isinstance(data, User):
        hashed_password = hash_password(password)
        
        try:
            assert hashed_password == data.password_hash
            
            token_data = {
                "sub": username,
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            }
            token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

            return {"access_token": token, "token_type": "bearer"}

        except AssertionError:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/logout")
async def logout():
    return {"message": "Logout successful", "status_code": 200}


@router.patch("/update/{user_id}")
def update_user(user_id: int, new_email: str=None, new_password: str=None):
    user_data_obj = UserData()
    response = user_data_obj.update_user(user_id=user_id, new_email=new_email, new_password=new_password)
    if "error" in response:
        raise HTTPException(status_code=response["status_code"], detail=response["error"])
    
    return response


@router.delete("/delete/{user_id}")
def delete_user(user_id: int):
    user_data_obj = UserData()
    response = user_data_obj.delete_user(user_id=user_id)
    if "error" in response:
        raise HTTPException(status_code=response["status_code"], detail=response["error"])
    
    return response
