# Standard Imports
from typing import Union
from datetime import datetime

# Local Imports
from config_file import DB_CONFIG
from backend.app.utils import SessionManager, hash_password
from backend.app.schemas import User, Tag, Task, TaskStatus, TaskPriority


class UserData:
    def __init__(self):
        self.session = SessionManager(**DB_CONFIG).get_session()

    def get_user(self, user_id: int=None, email: str=None) -> Union[User, dict]:
        """Read and return data from the db filter by user_id or email"""
        if user_id:
            data = self.session.query(User).filter_by(user_id=user_id).first()

        if email:
            data = self.session.query(User).filter_by(email=email).first()

        if not data:
            return {"error":"User doesn't exist", "status_code": 404}
        
        return data

    def add_user(self, email: str, password: str) -> dict:
        """Adds new user to the db if the user doesn't already exist"""
        data = self.get_user(email=email)
        if isinstance(data, User):
            return {"error": "User already exists", "status_code": 409}

        password_hash = hash_password(password)
        try:
            new_user = User(email=email, password_hash=password_hash)
            self.session.add(new_user)
            self.session.commit()
            return {"message": "User added successfully", "status_code": 201}
        
        except Exception as e:
            return {"error": f"Error adding new user - {e}", "status_code": 400}

    def update_user(self, user_id: int, new_email: str=None, new_password: str=None) -> dict:
        """Updates the user with the new email or/and new password if the user exists"""
        data = self.get_user(user_id=user_id)
        if isinstance(data, dict):
            return data
        
        try:
            if new_email:
                data.email = new_email
            
            if new_password:
                new_password_hash = hash_password(new_password)
                data.password_hash = new_password_hash
            
            self.session.commit()

        except Exception as e:
            return {"error": f"Error updating user details - {e}", "status_code": 400}
        
        return {"message": "Password updated successfully", "status_code": 200}
    
    def delete_user(self, user_id: int) -> dict:
        """Delete user from the database by user_id"""
        data = self.get_user(user_id=user_id)
        if isinstance(data, User):
            try:
                self.session.delete(data)
                self.session.commit()
                return {"message": "User deleted successfully", "status_code": 200}
            
            except Exception as e:
                return {"error": f"Error deleting user - {e}", "status_code": 400}
        
        return {"error": "User doesn't exist", "status_code": 404}
    

class TagData:
    def __init__(self):
        self.session = SessionManager(**DB_CONFIG).get_session()
        
    def get_tag(self, tag: str) -> Union[Tag, dict]:
        """Read and return data from the db filter by name"""
        data = self.session.query(Tag).filter_by(tag=tag).first()
        if not data:
            return {"error":"Tag doesn't exist", "status_code": 404}
        return data
    
    def add_tag(self, tag: str) -> dict:
        """Adds new tag to the db if the tag doesn't already exist"""
        data = self.get_tag(tag=tag)
        if isinstance(data, Tag):
            return {"error": "Tag already exists", "status_code": 409}

        try:
            new_tag = Tag(tag=tag)
            self.session.add(new_tag)
            self.session.commit()
            return {"message": "Tag added successfully", "status_code": 201}
        
        except Exception as e:
            return {"error": f"Error adding new tag - {e}", "status_code": 400}

    def update_tag(self, tag: str, new_tag: str=None) -> dict:
        """Updates the tag with the new name if the tag exists"""
        data = self.get_tag(tag=tag)
        if isinstance(data, dict):
            return data
        try:
            if new_tag:
                data.tag = new_tag

            self.session.commit()

        except Exception as e:
            return {"error": f"Error updating tag - {e}", "status_code": 400}

        return {"message": "Tag updated successfully", "status_code": 200}
    
    def delete_tag(self, tag: str) -> dict:
        """Delete tag from the database by tag_id"""
        data = self.get_tag(tag=tag)
        if isinstance(data, Tag):
            try:
                self.session.delete(data)
                self.session.commit()
                return {"message": "Tag deleted successfully", "status_code": 200}
            
            except Exception as e:
                return {"error": f"Error deleting tag - {e}", "status_code": 400}
        
        return {"error": "Tag doesn't exist", "status_code": 404}


class TaskData:
    def __init__(self):
        self.session = SessionManager(**DB_CONFIG).get_session()

    def create_task(self, user_id: int, title: str, description: str=None, tag: str=None, due_date: str=None, priority: str=None) -> dict:
        """Creates a new task for a user"""
        
        user_data = UserData().get_user(user_id=user_id)
        if isinstance(user_data, dict):
            return user_data

        try:
            new_task = Task(user_id=user_id, title=title)
            
            # Optional Parameters
            if description:
                new_task.description = description

            if tag:
                tag_data = TagData().get_tag(tag=tag)
                if isinstance(tag_data, dict):
                    return tag_data
                
                new_task.tag = tag

            if due_date:
                new_task.due_date = due_date

            if priority:
                new_task.priority = priority
        
            self.session.add(new_task)
            self.session.commit()

            return {"message": "Task created successfully", "status_code": 201}
        
        except Exception as e:
            return {"error": f"Error adding new task - {e}", "status_code": 400}
    
    def update_task(
            self, user_id: int, task_id: int, title: str=None, description: str=None,
            tag: str=None, due_date: str=None, priority: str=None, status: str=None
        ) -> dict:
        """Updates the task with the new title, description, status and tag if the task exists"""
        
        data = self.get_task(user_id=user_id, task_id=task_id)
        if isinstance(data, dict):
            return data
        
        try:
            if title:
                data.title = title
            
            if description:
                data.description = description
            
            if tag:
                tag_data = TagData().get_tag(tag=tag)
                if isinstance(tag_data, dict):
                    return tag_data
                
                data.tag = tag
            
            if due_date:
                data.due_date = due_date
            
            if priority:
                data.priority = priority
            
            if status:
                data.status = status

            self.session.commit()

        except Exception as e:
            return {"error": f"Error updating task - {e}", "status_code": 400}
        
        return {"message": "Task updated successfully", "status_code": 200}
    
    def delete_task(self, user_id: int, task_id: int) -> dict:
        """Delete task from the database by user_id and task_id"""
        data = self.get_task(user_id=user_id, task_id=task_id)
        if isinstance(data, Task):
            try:
                self.session.delete(data)
                self.session.commit()
                return {"message": "Task deleted successfully", "status_code": 200}
            
            except Exception as e:
                return {"error": f"Error deleting task - {e}", "status_code": 400}
        
        return {"error": "Task doesn't exist", "status_code": 404}
    
    def get_task(self, user_id: int, task_id: int) -> Union[Task, dict]:
        """Read and return data from the db filter by user_id and task_id"""
        data = self.session.query(Task).filter_by(user_id=user_id, task_id=task_id).first()
        if not data:
            return {"error":"Task doesn't exist", "status_code": 404}
        return data
    
    def get_all_tasks(self, user_id: int) -> list:
        """Returns all tasks for a user"""
        data = self.session.query(Task).filter_by(user_id=user_id).all()
        return data
    
    def get_tasks_by_tag(self, user_id: int, tag: str) -> list:
        """Returns all tasks for a user for a specific tag"""
        data = self.session.query(Task).filter_by(user_id=user_id, tag=tag).all()
        return data
    
    def get_tasks_by_status(self, user_id: int, status: str) -> list:
        """Returns all tasks for a user for a specific status"""
        data = self.session.query(Task).filter_by(user_id=user_id, status=status).all()
        return data
    
    def get_tasks_by_priority(self, user_id: int, priority: str) -> list:
        """Returns all tasks for a user for a specific priority"""
        data = self.session.query(Task).filter_by(user_id=user_id, priority=priority).all()
        return data
    
    def search_tasks_by_text(self, user_id: int, text: str) -> list:
        """Returns all tasks for a user by searching for a sub sting in the title or description"""
        data1 = self.session.query(Task).filter(Task.user_id == user_id, Task.title.ilike(f"%{text}%")).all()
        data2 = self.session.query(Task).filter(Task.user_id == user_id, Task.description.ilike(f"%{text}%")).all()
        data = list(set(data1 + data2)) # Remove duplicates from data1 + data2
        return data
    
    def auto_update_task_status_to_overdue(self):
        """
        Auto updates task status to 'Overdue' if the current date (login date) is greater than 
        the due date and the task status is not 'Completed'

        Note: This function has to be called every time when the user logs in
        """

        tasks = self.get_all_tasks(user_id=1)
        current_date = datetime.now()

        for task in tasks:
            if task.due_date and task.status != 'Completed':
                if current_date > task.due_date:
                    task.status = 'Overdue'
                    self.session.commit()
        
        return {"message": "Tasks' status refreshed!", "status_code": 200}


if __name__=="__main__":
    obj = UserData()
    
    obj.add_user("user1@gmail.com", "password")
    obj.add_user("user2@gmail.com", "password")
    
    data = obj.get_user(email="user1@gmail.com")
    data = obj.get_user(email="user2@gmail.com")

    
    obj.update_user(user_id=1, new_email="user1_new@gmail.com", new_password="new_password")
    obj.update_user(user_id=2, new_password="new_password")    

    data= obj.delete_user(user_id=2)

    obj = TagData()
    obj.add_tag("Work")
    obj.add_tag("Personal")
    obj.add_tag("Home")

    data = obj.get_tag(tag="Work")
    data = obj.delete_tag(tag="Personal")

    obj = TagData()
    data = obj.update_tag(tag="Home", new_tag="Family")

    print(data)

    obj = TaskData()
    data = obj.get_task(user_id=1, task_id=1)
    print(data)
    
    data = obj.create_task(user_id=1, title="Task 1", description="Description 1", due_date="2023-01-01", tag="Work")
    data = obj.update_task(user_id=1, task_id=1, title="Random", description="Description Random", tag="Work", priority=TaskPriority.High.value, status=TaskStatus.Completed.value)
    
    data = obj.get_tasks_by_status(user_id=1, status=TaskStatus.Completed.value)
    print(data)
    
    data = obj.get_tasks_by_priority(user_id=1, priority=TaskPriority.High.value)
    print(data)
