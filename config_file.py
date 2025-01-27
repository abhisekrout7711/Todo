# Local Database Configuration
DB_CONFIG = {
    "username": "postgres",
    "password": "admin",
    "host": "localhost", 
    "port": "5432",
    "database": "postgres"
}

DB_URL = f"postgresql://{DB_CONFIG['username']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

SECRET_KEY = "random_secret_key_for_jwt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30