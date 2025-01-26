# Standard Imports
from datetime import datetime

# Third-Party Imports
from fastapi import Depends, HTTPException, APIRouter

# Local Imports
from backend.auth_utils import get_current_admin, only_admin
from backend.app.database import UserData
from backend.app.schemas import Admin
from backend.app.models import UserResponse, UsersResponse

router = APIRouter()

# API Endpoints accessible only to admins
@router.get("/{user_id}", response_model=UserResponse, status_code=200)
@only_admin
async def get_user(user_id: int, current_admin: Admin = Depends(get_current_admin)):
    """Retrieves a specific user from the database"""
    try:
        user = UserData().get_user(user_id=user_id)
        return UserResponse(**user.__dict__)
    
    except AttributeError as e:
        raise HTTPException(status_code=404, detail=f"User:{user_id} not found - {e}")


@router.get("/all", response_model=UsersResponse, status_code=200)
@only_admin
async def get_all_users(current_admin: Admin = Depends(get_current_admin)):
    """Retrieves all users from the database"""
    users = UserData().get_all_users()
    if not users:
        return UsersResponse(user_count=0, users=[])
    users = [UserResponse(**user.__dict__) for user in users]
    return UsersResponse(user_count=len(users), users=users)
    

@router.get("/recently_active", response_model=UsersResponse, status_code=200)
@only_admin
async def get_recently_active_users(updated_at: datetime, current_admin: Admin = Depends(get_current_admin)):
    """Retrieves all users those have been active recently"""
    users = UserData().get_recently_active_users(updated_at=updated_at)
    if not users:
        return UsersResponse(user_count=0, users=[])
    users = [UserResponse(**user.__dict__) for user in users]
    return UsersResponse(user_count=len(users), users=users)
    


@router.delete("/{user_id}", status_code=200)
@only_admin
async def delete_user(user_id: int, current_admin: Admin = Depends(get_current_admin)):
    """Deletes users from the database as an admin"""
    response = UserData().delete_user(user_id=user_id)
    if "error" in response:
        raise HTTPException(status_code=response["status_code"], detail=response["error"])
    
    return response
