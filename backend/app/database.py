from sqlalchemy import create_engine
from sqlalchemy.engine import Engine as sqlalchemy_engine

# Define the database configuration
db_config = {
    "username": "postgres",
    "password": "admin",
    "host": "localhost", 
    "port": "5432",
    "database": "postgres"
}

def get_database_connection(db_config: dict) -> sqlalchemy_engine:
    """Connects to the database and returns sqlalchemy engine instance"""
    db_url = f"postgresql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    engine = create_engine(db_url)
    return engine
