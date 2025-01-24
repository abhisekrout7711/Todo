from pydantic import BaseModel

# Response Models
class Token(BaseModel):
    """Model for login api token response"""
    access_token: str
    token_type: str
