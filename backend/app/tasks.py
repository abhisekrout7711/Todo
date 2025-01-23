from fastapi import Depends, HTTPException, APIRouter
from backend.auth_utils import OAUTH2_SCHEME
from backend.app.database import UserData
import jwt
from config_file import SECRET_KEY, ALGORITHM

router = APIRouter()

def get_current_user(token: str = Depends(OAUTH2_SCHEME)):
    """Decode the JWT token and retrieve the current user."""
    breakpoint()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Retrieve user from database (optional)
    user_data_obj = UserData()
    user = user_data_obj.get_user(email=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/task/create")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"This is a protected route for {current_user.email}!"}

if __name__ == "__main__":
    get_current_user("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhYmhpc2VrIiwiZXhwIjoxNzM3NjYxODM3fQ.GsfTH85SXh3GYRaZ3UPztmU2EhpH9sEaLSSsRUyg51k")