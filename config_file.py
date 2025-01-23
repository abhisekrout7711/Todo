# Local Database Configuration
DB_CONFIG = {
    "username": "postgres",
    "password": "admin",
    "host": "localhost", 
    "port": "5432",
    "database": "postgres"
}

SECRET_KEY = "random_secret_key_for_jwt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30