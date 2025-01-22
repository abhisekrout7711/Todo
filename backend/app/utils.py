from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


class SessionManager:
    # Class for handling database sessions
    def __init__(self, username: str, password: str, host: str, port: str, database: str):
        self.engine = None
        self.session = None
        self.__db_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"

    @property
    def session(self) -> Session:
        """
        A property that returns the session object if it exists, otherwise creates a new session and returns it

        Raises:
            RuntimeError: If session creation fails
        """
        if self.session:
            return self.session
        
        # Create a new session if there is no existing session
        try:
            engine = create_engine(self.__db_url)
            self.session = sessionmaker(bind=engine).Session()
            return self.session
        
        except Exception as e:
            raise RuntimeError("Session creation failed") from e
    
    def close_session(self):
        """Closes the database session and disposes the engine"""
        if self.session:
            self.session.close()
            self.session = None
        
        if self.engine:
            self.engine.dispose()
            self.engine = None
    

def hash_password(password: str):
    """Hashes the user's password"""
    return password
