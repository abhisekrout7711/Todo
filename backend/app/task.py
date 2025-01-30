# Standard Imports
from datetime import datetime

# Third-Party Imports
from fastapi import Depends, HTTPException, APIRouter, Header

# Local Imports
from backend.app.auth_utils import get_current_user, raise_exception
from backend.app.database import TaskData
from backend.app.schemas import TaskStatus, TaskPriority
from backend.app.models import TaskResponse, TasksResponse, CreateTaskRequest, UpdateTaskRequest

router = APIRouter()


@router.post("/create", status_code=201)
@raise_exception
async def create_task(
        request: CreateTaskRequest,
        current_user: dict = Depends(get_current_user)
    ):
    """Creates a new task for the current user"""
    priority = request.priority.value if request.priority else None
    response = TaskData().create_task(
        user_id=current_user["user"].user_id, title=request.title, description=request.description, 
        tag=request.tag, due_date=request.due_date, priority=priority
    )
    
    if "error" in response:
        raise HTTPException(status_code=response["status_code"], detail=response["error"])
    
    return response


@router.patch("/{task_id}", status_code=200)
@raise_exception
async def update_task(
        task_id: int,
        request: UpdateTaskRequest,
        current_user: dict = Depends(get_current_user)
    ):
    """Updates the task with the new title, description, status and tag if the task exists"""
    priority = request.priority.value if request.priority else None
    status = request.status.value if request.status else None
    response = TaskData().update_task(
        user_id=current_user["user"].user_id, task_id=task_id, title=request.title, 
        description=request.description, tag=request.tag, due_date=request.due_date, 
        priority=priority, status=status
    )
    if "error" in response:
        raise HTTPException(status_code=response["status_code"], detail=response["error"])
    
    return response


@router.delete("/{task_id}", status_code=200)
@raise_exception
async def delete_task(task_id: int, current_user: dict = Depends(get_current_user)):
    """Deletes a task for the current user"""
    response = TaskData().delete_task(user_id=current_user["user"].user_id, task_id=task_id)
    if "error" in response:
        raise HTTPException(status_code=response["status_code"], detail=response["error"])
    
    return response


@router.get("/task_id/{task_id}", response_model=TaskResponse, status_code=200)
@raise_exception
async def get_task(task_id: int, current_user: dict = Depends(get_current_user)):
    """Returns a task for a given task_id if the task exists"""
    task = TaskData().get_task(user_id=current_user["user"].user_id, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task:{task_id} not found for User:{current_user['user'].user_id}")
    
    return task


@router.get("/all/", response_model=TasksResponse, status_code=200)
@raise_exception
async def get_tasks(current_user: dict = Depends(get_current_user)):
    """Returns all tasks for a given user"""
    tasks = TaskData().get_all_tasks(user_id=current_user["user"].user_id)
    if not tasks:
        return TasksResponse(task_count=0,tasks=[])
    
    tasks = [TaskResponse(**task.__dict__) for task in tasks]

    return TasksResponse(task_count=len(tasks), tasks=tasks)


@router.get("/tag/{tag}", response_model=TasksResponse, status_code=200)
@raise_exception
async def get_tasks_by_tag(tag: str, current_user: dict = Depends(get_current_user)):
    """Retrieves all tasks for a given user filtered by a specific tag"""
    tasks = TaskData().get_tasks_by_tag(user_id=current_user["user"].user_id, tag=tag)
    if not tasks:
        return TasksResponse(task_count=0,tasks=[])
    
    tasks = [TaskResponse(**task.__dict__) for task in tasks]

    return TasksResponse(task_count=len(tasks), tasks=tasks)


@router.get("/status/", response_model=TasksResponse, status_code=200)
@raise_exception
async def get_tasks_by_status(status: TaskStatus, current_user: dict = Depends(get_current_user)):
    """Retrieves all tasks for a given user filtered by a specific status"""
    tasks = TaskData().get_tasks_by_status(user_id=current_user["user"].user_id, status=status.value)
    if not tasks:
        return TasksResponse(task_count=0,tasks=[])
    
    tasks = [TaskResponse(**task.__dict__) for task in tasks]

    return TasksResponse(task_count=len(tasks), tasks=tasks)



@router.get("/priority/", response_model=TasksResponse, status_code=200)
@raise_exception
async def get_tasks_by_priority(priority: TaskPriority, current_user: dict = Depends(get_current_user)):
    """Retrieves all tasks for a given user filtered by a specific priority"""
    tasks = TaskData().get_tasks_by_priority(user_id=current_user["user"].user_id, priority=priority.value)
    if not tasks:
        return TasksResponse(task_count=0,tasks=[])
    
    tasks = [TaskResponse(**task.__dict__) for task in tasks]

    return TasksResponse(task_count=len(tasks), tasks=tasks)


@router.get("/text/", response_model=TasksResponse, status_code=200)
@raise_exception
async def search_tasks_by_text(text: str, current_user: dict = Depends(get_current_user)):
    """Returns all tasks for a user by searching for a sub sting in the title or description"""
    tasks = TaskData().search_tasks_by_text(user_id=current_user["user"].user_id, text=text)
    if not tasks:
        return TasksResponse(task_count=0,tasks=[])
    
    tasks = [TaskResponse(**task.__dict__) for task in tasks]

    return TasksResponse(task_count=len(tasks), tasks=tasks)
