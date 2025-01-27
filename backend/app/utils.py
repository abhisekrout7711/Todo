# Standard Imports
import hashlib

# Third-Party Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


class SessionManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url, pool_size=5, max_overflow=10)
        self.Session = sessionmaker(bind=self.engine)

    def __enter__(self):
        # Create and return a session when the context is entered
        self.session = self.Session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup session and engine only if session is not None
        if self.session:
            self.session.close()
        if self.engine:
            self.engine.dispose()


def hash_password(password: str):
        """Hashes and returns the user's password deterministically"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
