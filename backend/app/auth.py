# Standard Imports
from datetime import datetime, timedelta, timezone

# Third-Party Imports
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
import jwt

# Local Imports
from backend.app.database import UserData
from backend.app.schemas import User
from backend.app.models import Token
from backend.app.utils import hash_password
from config_file import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/register", status_code=201)
async def register_user(username: str, password: str):
    user_data_obj = UserData()
    response = user_data_obj.add_user(username=username, password=password) # Password hasing is taken care of
    if "error" in response:
        raise HTTPException(status_code=response["status_code"], detail=response["error"])
    
    return response


@router.post("/login", response_model=Token, status_code=200)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):  
    """Returns a JWT token if the user is authenticated"""
    username = form_data.username
    password = form_data.password
    user_data_obj = UserData()
    data: User = user_data_obj.get_user(username=username)
    
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


@router.post("/logout", status_code=200)
async def logout():
    return {"message": "Logout successful", "status_code": 200}


@router.patch("/update/{user_id}", status_code=200)
def update_user(user_id: int, new_username: str=None, new_password: str=None):
    user_data_obj = UserData()
    response = user_data_obj.update_user(user_id=user_id, new_username=new_username, new_password=new_password)
    if "error" in response:
        raise HTTPException(status_code=response["status_code"], detail=response["error"])
    
    return response


@router.delete("/delete/{user_id}", status_code=200)
def delete_user(user_id: int):
    user_data_obj = UserData()
    response = user_data_obj.delete_user(user_id=user_id)
    if "error" in response:
        raise HTTPException(status_code=response["status_code"], detail=response["error"])
    
    return response
