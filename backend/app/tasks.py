# Third-Party Imports
from fastapi import Depends, HTTPException, APIRouter, Header

# Local Imports
from backend.auth_utils import get_current_user
from backend.app.database import UserData
from backend.app.schemas import User

router = APIRouter()

@router.get("/task/create")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"This is a protected route for {current_user.username}!"}
