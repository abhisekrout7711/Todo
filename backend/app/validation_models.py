from pydantic import BaseModel

class UserModel(BaseModel):
    email: str
    password: str

class TagModel(BaseModel):
    name: str

class TaskModel(BaseModel):
    user_id: int
    tag_id: int
    title: str
    description: str
    status: str
    priority: str