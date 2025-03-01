# Standard Imports
from functools import wraps
from datetime import datetime, timedelta, timezone
from typing import Tuple

# Third-Party Imports
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

# Local Imports
from config_file import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from backend.app.database import AdminData, UserData, TokenData
from backend.app.schemas import Admin, User

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/api/user/login")


def get_current_user(access_token: str = Depends(OAUTH2_SCHEME)) -> dict:
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

    user = UserData().get_user(username=username)

    return {"user": user, "token": access_token}


def get_current_admin(access_token: str = Depends(OAUTH2_SCHEME)) -> Admin:
    """Decode the JWT token and retrieve the current admin."""
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Unauthorized Access")
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Unauthorized Access")

    admin = AdminData().get_admin(username=username)
    return admin


def generate_token(username: str) -> str:
    """
    Generates a JWT token for a given username.
    The token includes the username as the subject and an expiration time.
    If the user is an admin, an admin token is returned; otherwise, a user tokenis returned.
    """
    token_data = {
        "sub": username,
        "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return token


def raise_exception(func):
    """Raises an exception if the current user is not authorised"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        user = kwargs.get("current_user").get("user")
        token = kwargs.get("current_user").get("token")

        if not user:
            raise HTTPException(status_code=403, detail="Unauthorized User")
        
        if TokenData().check_if_token_revoked(token):
            raise HTTPException(status_code=401, detail="Token expired - Please login again")
        
        return await func(*args, **kwargs)
    return wrapper


def only_admin(func):
    """Raises an exception if the current admin is not authorised"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not kwargs.get("current_admin"):
            raise HTTPException(status_code=403, detail="Unauthorized User")
        return await func(*args, **kwargs)
    return wrapper
