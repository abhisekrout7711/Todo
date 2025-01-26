# Standard Imports
from datetime import datetime

# Third-Party Imports
from fastapi import Depends, HTTPException, APIRouter

# Local Imports
from backend.auth_utils import get_current_user, raise_exception
from backend.app.database import TagData
from backend.app.schemas import User
from backend.app.models import TagResponse, TagsResponse

router = APIRouter()

@router.get("/all", response_model=TagsResponse, status_code=200)
@raise_exception
async def get_all_tags(current_user: dict = Depends(get_current_user)):
    """Returns all tags for the current user"""
    tags = TagData().get_all_tags(user_id=current_user["user"].user_id)
    if not tags:
       return TagsResponse(tag_count=0, tags=[])
    
    tags = [TagResponse(**tag.__dict__) for tag in tags]

    return TagsResponse(tag_count=len(tags), tags=tags)


@router.post("/create", status_code=201)
@raise_exception
async def create_tag(tag: str, current_user: dict = Depends(get_current_user)):
    """Creates a new tag for the current user"""
    response = TagData().add_tag(user_id=current_user["user"].user_id, tag=tag)
    if "error" in response:
        raise HTTPException(status_code=response["status_code"], detail=response["error"])
    
    return response


@router.delete("/{tag}", status_code=200)
@raise_exception
async def delete_tag(tag: str, current_user: dict = Depends(get_current_user)):
    """Deletes a tag for the current user"""
    response = TagData().delete_tag(user_id=current_user["user"].user_id, tag=tag)
    if "error" in response:
        raise HTTPException(status_code=response["status_code"], detail=response["error"])
    
    return response


@router.patch("/{tag}", status_code=200)
@raise_exception
async def update_tag(tag: str, new_tag: str, current_user: dict = Depends(get_current_user)):
    """Updates a tag for the current user"""
    response = TagData().update_tag(user_id=current_user["user"].user_id, tag=tag, new_tag=new_tag)
    if "error" in response:
        raise HTTPException(status_code=response["status_code"], detail=response["error"])
    
    return response
