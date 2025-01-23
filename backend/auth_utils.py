from fastapi.security import OAuth2PasswordBearer

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/api/user/login")

