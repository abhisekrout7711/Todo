# # # JWT Authentication 
# # from fastapi import FastAPI, Depends, HTTPException
# # from fastapi.security import OAuth2PasswordBearer
# # from pydantic import BaseModel
# # import jwt
# # from datetime import datetime, timedelta
# # from app.database import get_database_connection
# # import bcrypt
# # app = FastAPI()

# # oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# # # Model for token response
# # class Token(BaseModel):
# #     access_token: str
# #     token_type: str

# # # Route to obtain an access token
# # # @app.post("/login", response_model=Token)
# # async def login(username: str, password: str):
# #     password = password.encode('utf-8')  # Convert password to bytes
# #     salt = bcrypt.gensalt()  # Generate a salt
# #     hashed_password = bcrypt.hashpw(password, salt) 

# #     user = 'Read from database'
# #     if not user or user["password"] != password:
# #         raise HTTPException(status_code=401, detail="Invalid credentials")
    
# #     # Generate JWT token
# #     token_data = {"sub": username}
# #     token = jwt.encode(token_data, "SECRET_KEY", algorithm="HS256")
# #     return {"access_token": token, "token_type": "bearer"}

# # # @app.get("/protected")
# # # async def protected_route(token: str = Depends(oauth2_scheme)):
# # #     # Token will be passed as a Bearer token in Authorization header
# # #     return {"message": "This is a protected route!"}


# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from passlib.context import CryptContext

# # Initialize the app and password hashing context
# app = FastAPI()
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # In-memory "database" for demonstration purposes
# fake_users_db = {}

# # Pydantic model for the user data
# class User(BaseModel):
#     username: str
#     password: str

# # Function to hash a password
# def hash_password(password: str):
#     return pwd_context.hash(password)

# # API to register a new user
# @app.post("/register", response_model=User)
# async def register_user(user: UserCreate):
#     if user.username in fake_users_db:
#         raise HTTPException(status_code=400, detail="Username already registered")
    
#     hashed_password = hash_password(user.password)  # Hash the user's password
#     fake_users_db[user.username] = {
#         "username": user.username,
#         "email": user.email,
#         "hashed_password": hashed_password,
#     }

#     return User(username=user.username, email=user.email)
