from pydantic import BaseModel
from typing import Optional, List
from datetime import date

# Local Imports
from backend.app.schemas import TaskStatus, TaskPriority


# TAsk API Request Models
class CreateTaskRequest(BaseModel):
    title: str
    description: str | None = None
    tag: str | None = None
    due_date: date | None = None
    priority: TaskPriority | None = None

    # class Config:
    #     json_schema_extra = {
    #         "example": {
    #             "title" : "Task Title",
    #             "description" : "Task Description",
    #             "tag" : "Tag Name",
    #             "due_date" : "2025-01-27",
    #             "priority" : "Medium"
    #         }
    #     }

class UpdateTaskRequest(CreateTaskRequest):
    title: str | None = None
    status: TaskStatus | None = None


# User API Request Models
class UpdateUserRequest(BaseModel):
    new_username: str | None = None
    new_password: str | None = None

# Task API Response Models
class TaskResponse(BaseModel):
    """Response model to return Single Task"""
    user_id: int
    task_id: int
    title: str
    description: Optional[str]
    tag_id: Optional[int]
    tag: Optional[str]
    due_date: Optional[date]
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
