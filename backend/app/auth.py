# Third-Party Imports
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

# Local Imports
from backend.app.database import AdminData, UserData, TokenData
from backend.auth_utils import get_current_user, generate_token, raise_exception

router = APIRouter()

@router.post("/register", status_code=201)
async def register_user(username: str, password: str):
    """Register a new if the user doesn't already exist"""

    # Don't allow to register a new user if the creds match with an admin
    if AdminData().is_admin(username=username, password=password):
        return {"error": "User already exists", "status_code": 409}
    
    response = UserData().add_user(username=username, password=password) # Password hasing is taken care of
    if "error" in response:
        raise HTTPException(status_code=response["status_code"], detail=response["error"])
    
    return response


@router.post("/login", status_code=200)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):  
    """Returns a JWT token if the user is authenticated"""
    username = form_data.username
    password = form_data.password
    
    token = generate_token(username=username)

    if AdminData().is_admin(username=username, password=password):
        return {"access_token": token, "token_type": "bearer"}
        
    elif UserData().is_user(username=username, password=password):
        return {"access_token": token, "token_type": "bearer"}

    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/logout", status_code=200)
@raise_exception
async def logout(current_user: dict=Depends(get_current_user)):
    TokenData().revoke_token(current_user["token"])
    return {"message": "Logout successful", "status_code": 200}


@router.post("/delete", status_code=200)
@raise_exception
async def delete_user(current_user: dict=Depends(get_current_user)):
    response = UserData().delete_user(user_id=current_user["user"].user_id)
    if "error" in response:
        raise HTTPException(status_code=response["status_code"], detail=response["error"])
    
    return response
