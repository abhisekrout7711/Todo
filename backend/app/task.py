# Standard Imports
from datetime import datetime

# Third-Party Imports
from fastapi import Depends, HTTPException, APIRouter, Header

# Local Imports
from backend.auth_utils import get_current_user, raise_exception
from backend.app.database import TaskData
from backend.app.schemas import User, TaskStatus, TaskPriority
from backend.app.models import TaskResponse, TasksResponse

router = APIRouter()


@router.post("/create", status_code=201)
@raise_exception
async def create_task(
        title: str, description: str=None, tag_id: int=None, due_date: datetime=None, priority: TaskPriority=TaskPriority.Medium, 
        current_user: dict = Depends(get_current_user)
    ):
    """Creates a new task for the current user"""
    response = TaskData().create_task(
        user_id=current_user["user"].user_id, title=title, description=description, 
        tag_id=tag_id, due_date=due_date, priority=priority.value
    )
    if "error" in response:
        raise HTTPException(status_code=response["status_code"], detail=response["error"])
    
    return response


@router.patch("/{task_id}", status_code=200)
@raise_exception
async def update_task(
        task_id: int, # required query parameter
        title: str=None, description: str=None, tag_id: int=None, 
        due_date: str=None, priority:TaskPriority=TaskPriority.Medium, status: TaskStatus=TaskStatus.Pending,
        current_user: dict = Depends(get_current_user)
    ):
    """Updates the task with the new title, description, status and tag if the task exists"""
    task_data_obj = TaskData()
    response = task_data_obj.update_task(
        user_id=current_user["user"].user_id, task_id=task_id, 
        title=title, description=description, tag_id=tag_id, 
        due_date=due_date, priority=priority.value, status=status.value
    )
    if "error" in response:
        raise HTTPException(status_code=response["status_code"], detail=response["error"])
    
    return response


@router.delete("/{task_id}", status_code=200)
@raise_exception
async def delete_task(task_id: int, current_user: dict = Depends(get_current_user)):
    """Deletes a task for the current user"""
    task_data_obj = TaskData()
    response = task_data_obj.delete_task(user_id=current_user["user"].user_id, task_id=task_id)
    if "error" in response:
        raise HTTPException(status_code=response["status_code"], detail=response["error"])
    
    return response


@router.get("/{task_id}", response_model=TaskResponse, status_code=200)
@raise_exception
async def get_task(task_id: int, current_user: dict = Depends(get_current_user)):
    """Returns a task for a given task_id if the task exists"""
    task = TaskData().get_task(user_id=current_user["user"].user_id, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task:{task_id} not found for User:{current_user.user_id}")
    
    return task


@router.get("/all", response_model=TasksResponse, status_code=200)
@raise_exception
async def get_tasks(current_user: dict = Depends(get_current_user)):
    """Returns all tasks for a given user"""
    task_data_obj = TaskData()
    tasks = task_data_obj.get_all_tasks(user_id=current_user["user"].user_id)
    if not tasks:
        return TasksResponse(task_count=0,tasks=[])
    
    tasks = [TaskResponse(**task.__dict__) for task in tasks]

    return TasksResponse(task_count=len(tasks), tasks=tasks)


@router.get("/tag_id", response_model=TasksResponse, status_code=200)
@raise_exception
async def get_tasks_by_tag_id(tag_id: int, current_user: dict = Depends(get_current_user)):
    """Retrieves all tasks for a given user filtered by a specific tag"""
    task_data_obj = TaskData()
    tasks = task_data_obj.get_tasks_by_tag_id(user_id=current_user["user"].user_id, tag_id=tag_id)
    if not tasks:
        return TasksResponse(task_count=0,tasks=[])
    
    tasks = [TaskResponse(**task.__dict__) for task in tasks]

    return TasksResponse(task_count=len(tasks), tasks=tasks)


@router.get("/status", response_model=TasksResponse, status_code=200)
@raise_exception
async def get_tasks_by_status(status: TaskStatus, current_user: dict = Depends(get_current_user)):
    """Retrieves all tasks for a given user filtered by a specific status"""
    task_data_obj = TaskData()
    tasks = task_data_obj.get_tasks_by_status(user_id=current_user["user"].user_id, status=status.value)
    if not tasks:
        return TasksResponse(task_count=0,tasks=[])
    
    tasks = [TaskResponse(**task.__dict__) for task in tasks]

    return TasksResponse(task_count=len(tasks), tasks=tasks)



@router.get("/priority", response_model=TasksResponse, status_code=200)
@raise_exception
async def get_tasks_by_priority(priority: TaskPriority, current_user: dict = Depends(get_current_user)):
    """Retrieves all tasks for a given user filtered by a specific priority"""
    task_data_obj = TaskData()
    tasks = task_data_obj.get_tasks_by_priority(user_id=current_user["user"].user_id, priority=priority.value)
    if not tasks:
        return TasksResponse(task_count=0,tasks=[])
    
    tasks = [TaskResponse(**task.__dict__) for task in tasks]

    return TasksResponse(task_count=len(tasks), tasks=tasks)


@router.get("/text", response_model=TasksResponse, status_code=200)
@raise_exception
async def search_tasks_by_text(text: str, current_user: dict = Depends(get_current_user)):
    """Returns all tasks for a user by searching for a sub sting in the title or description"""
    task_data_obj = TaskData()
    tasks = task_data_obj.search_tasks_by_text(user_id=current_user["user"].user_id, text=text)
    if not tasks:
        return TasksResponse(task_count=0,tasks=[])
    
    tasks = [TaskResponse(**task.__dict__) for task in tasks]

    return TasksResponse(task_count=len(tasks), tasks=tasks)
