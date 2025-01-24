# Third-Party Imports
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

# Local Imports
from config_file import SECRET_KEY, ALGORITHM
from backend.app.database import UserData

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/api/user/login")

def get_current_user(access_token: str = Depends(OAUTH2_SCHEME)):
    """Decode the JWT token and retrieve the current user."""
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Retrieve user from database (optional)
    user_data_obj = UserData()
    user = user_data_obj.get_user(username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user