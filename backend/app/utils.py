from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import hashlib


class SessionManager:
    # Class for handling database sessions
    def __init__(self, username: str, password: str, host: str, port: str, database: str):
        self.engine = None
        self.session = None
        self.__db_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"

    def get_session(self) -> Session:
        """
        A property that returns the session object if it exists, otherwise creates a new session and returns it

        Raises:
            RuntimeError: If session creation fails
        """
        if not self.session:
            # Create a new session if there is no existing session
            try:
                engine = create_engine(self.__db_url)
                self.session = sessionmaker(bind=engine)()
            
            except Exception as e:
                raise RuntimeError(f"Session creation failed - {e}") from e
            
        return self.session
    
    def close_session(self):
        """Closes the database session and disposes the engine"""
        if self.session:
            self.session.close()
            self.session = None
        
        if self.engine:
            self.engine.dispose()
            self.engine = None
    

def hash_password(password: str):
        """Hashes and returns the user's password deterministically"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
