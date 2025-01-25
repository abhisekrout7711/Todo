# Standard Imports
from datetime import datetime

# Third-Party Imports
from fastapi import Depends, HTTPException, APIRouter

# Local Imports
from backend.auth_utils import get_current_admin
from backend.app.database import UserData
from backend.app.schemas import Admin
from backend.app.models import UserResponse, UsersResponse

router = APIRouter()

# API Endpoints accessible only to admins
@router.get("/id/{user_id}", response_model=UserResponse, status_code=200)
async def get_user(user_id: int, current_admin: Admin = Depends(get_current_admin)):
    """Retrieves a specific user from the database"""
    if current_admin:
        user = UserData().get_user(user_id=user_id)
        return UserResponse(**user.__dict__)
    
    raise HTTPException(status_code=403, detail="Unauthorized")


@router.get("/", response_model=UsersResponse, status_code=200)
async def get_all_users(current_admin: Admin = Depends(get_current_admin)):
    """Retrieves all users from the database"""
    if current_admin:
        users = UserData().get_all_users()
        users = [UserResponse(**user.__dict__) for user in users]
        return UsersResponse(user_count=len(users), users=users)
    
    raise HTTPException(status_code=403, detail="Unauthorized")


@router.get("/admin", response_model=UsersResponse, status_code=200)
async def get_recently_active_users(updated_at: datetime, current_admin: Admin = Depends(get_current_admin)):
    """Retrieves all users those have been active recently"""
    if current_admin:
        users = UserData().get_recently_active_users(updated_at=updated_at)
        users = [UserResponse(**user.__dict__) for user in users]
        return UsersResponse(users_count=len(users), users=users)
    
    raise HTTPException(status_code=403, detail="Unauthorized")


@router.delete("/admin/{user_id}", status_code=200)
async def delete_user(user_id: int, current_admin: Admin = Depends(get_current_admin)):
    """Deletes users from the database as an admin"""
    if current_admin:
        response = UserData().delete_user(user_id=user_id)

        if "error" in response:
            raise HTTPException(status_code=response["status_code"], detail=response["error"])
        
        return response
    
    raise HTTPException(status_code=403, detail="Unauthorized")
