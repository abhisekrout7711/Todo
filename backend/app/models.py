from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Response Models
class Token(BaseModel):
    """Model for login api token response"""
    access_token: str
    token_type: str

class TaskResponse(BaseModel):
    """Response model to return Single Task"""
    user_id: int
    task_id: int
    title: str
    description: Optional[str]
    tag: Optional[str]
    due_date: Optional[datetime]
    priority: str
    status: str


class TasksResponse(BaseModel):
    """Response model to return multiple tasks"""
    task_count : int
    tasks: List[TaskResponse]

class TagResponse(BaseModel):
    """Response model to return single tag"""
    id: int
    tag: str

class TagsResponse(BaseModel):
    """Response Model to return multiple tags"""
    tag_count : int
    tags: List[TagResponse]