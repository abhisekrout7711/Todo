from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Task API Response Models
class TaskResponse(BaseModel):
    """Response model to return Single Task"""
    user_id: int
    task_id: int
    title: str
    description: Optional[str]
    tag_id: Optional[int]
    due_date: Optional[datetime]
    priority: str
    status: str

class TasksResponse(BaseModel):
    """Response model to return multiple tasks"""
    task_count : int
    tasks: List[TaskResponse]


# Tag API Response Models
class TagResponse(BaseModel):
    """Response model to return single tag"""
    tag_id: int
    tag: str

class TagsResponse(BaseModel):
    """Response Model to return multiple tags"""
    tag_count : int
    tags: List[TagResponse]


# Admin API Response Models
class UserResponse(BaseModel):
    """Response model to return single user"""
    user_id: int
    username: str

class UsersResponse(BaseModel):
    """Response model to return multiple users"""
    user_count : int
    users: List[UserResponse]
