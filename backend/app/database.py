# Standard Imports
from typing import Union, List
from datetime import datetime

# Local Imports
from config_file import DB_URL
from backend.app.utils import SessionManager, hash_password
from backend.app.schemas import Admin, User, Tag, Task, RevokedToken, User, TaskStatus, TaskPriority


class AdminData:
    """Class to read and write data from/to the admins table"""
    def get_admin(self, username: str) -> Admin:
        """Read and return data from the admins db filter by username"""
        with SessionManager(db_url=DB_URL) as session:
            admin = session.query(Admin).filter_by(username=username).first()
        return admin
    
    def is_admin(self, username: str, password: str) -> bool:
        """Check if the user is an admin and return True or False"""
        admin = self.get_admin(username=username)
    
        if admin and admin.password == password:
            return True

        return False


class UserData:
    """Class to read and write data from/to the users table"""
    def get_user(self, user_id: int=None, username: str=None) -> User:
        """Read and return data from the db filter by user_id or username"""
        with SessionManager(db_url=DB_URL) as session:
            if user_id:
                user = session.query(User).filter_by(user_id=user_id).first()

            if username:
                user = session.query(User).filter_by(username=username).first()
            
            return user
    
    def is_user(self, username: str, password: str) -> bool:
        """Check if the user exists and return True or False"""
        user = self.get_user(username=username)
        if user and user.password_hash == hash_password(password):
            return True

        return False
    
    def add_user(self, username: str, password: str) -> dict:
        """Adds new user to the db if the user doesn't already exist"""
        user = self.get_user(username=username)
        if user:
            return {"error": "User already exists", "status_code": 409}

        password_hash = hash_password(password)
        try:
            with SessionManager(db_url=DB_URL) as session:
                new_user = User(username=username, password_hash=password_hash)
                session.add(new_user)
                session.commit()

            return {"message": "User added successfully", "status_code": 201}
        
        except Exception as e:
            return {"error": f"Error adding new user - {e}", "status_code": 400}

    def update_user(self, user_id: int, new_username: str=None, new_password: str=None) -> dict:
        """Updates the user with the new username or/and new password if the user exists"""
        user = self.get_user(user_id=user_id)
        if not user:
            return {"error": "User doesn't exist", "status_code": 404}
        
        try:
            if new_username:
                user.username = new_username
            
            if new_password:
                new_password_hash = hash_password(new_password)
                user.password_hash = new_password_hash
            
            with SessionManager(db_url=DB_URL) as session:
                session.merge(user)
                session.commit()
            
            return {"message": "User details updated successfully", "status_code": 200}

        except Exception as e:
            return {"error": f"Error updating user details - {e}", "status_code": 400}
    
    def delete_user(self, user_id: int) -> dict:
        """Delete user from the database by user_id"""
        user = self.get_user(user_id=user_id)
        if not user:
            return {"error": "User doesn't exist", "status_code": 404}
        
        try:
            with SessionManager(db_url=DB_URL) as session:
                session.merge(user)
                session.delete(user)
                session.commit()

            return {"message": "User deleted successfully", "status_code": 200}
        
        except Exception as e:
            return {"error": f"Error deleting user - {e}", "status_code": 400}
        
    
    def get_all_users(self) -> List[User]:
        """Read and return all users from the users table as an admin"""
        with SessionManager(db_url=DB_URL) as session:
            users = session.query(User).all()
            return users
    
    def get_recently_active_users(self, updated_at: datetime) -> List[User]:
        """Read and return recently active users from the users table as an admin"""
        with SessionManager(db_url=DB_URL) as session:
            users = session.query(User).filter(User.updated_at > updated_at).all()
            return users

class TagData:
    """Class to read and write data from/to the tags table"""   
    def get_tag(self, user_id: int, tag_id: int=None, tag: str=None) -> Tag:
        """Return tag for a user filter by tag_id if tag exists"""
        with SessionManager(db_url=DB_URL) as session:
            if tag_id:
                tag_ = session.query(Tag).filter_by(user_id=user_id, tag_id=tag_id).first()
            
            elif tag:
                tag_ = session.query(Tag).filter_by(user_id=user_id, tag=tag).first()
            
            return tag_
    
    def get_all_tags(self, user_id: int) -> List[Tag]:
        """Returns all tags for a user"""
        with SessionManager(db_url=DB_URL) as session:
            tags = session.query(Tag).filter_by(user_id=user_id).all()
            return tags
    
    def add_tag(self, user_id: int, tag: str) -> dict:
        """Adds new tag to the db for a user if the tag doesn't already exist"""
        tag_= self.get_tag(user_id=user_id, tag=tag)
        if tag_:
            return {"error": f"Tag:{tag} already exists for User:{user_id}", "status_code": 409}

        try:
            with SessionManager(db_url=DB_URL) as session:
                new_tag = Tag(user_id=user_id, tag=tag)
                session.add(new_tag)
                session.commit()

            return {"message": "Tag added successfully", "status_code": 201}
        
        except Exception as e:
            return {"error": f"Error adding new tag - {e}", "status_code": 400}

    def update_tag(self, user_id: int, tag: str, new_tag: str=None) -> dict:
        """Updates the tag with the new name if the tag exists"""
        tag_ = self.get_tag(user_id=user_id, tag=tag)
        if not tag_:
            return {"error": f"Tag:{tag} doesn't exist for User:{user_id}", "status_code": 404}
        
        try:
            
            if new_tag:
                tag_.tag = new_tag
            
            with SessionManager(db_url=DB_URL) as session:
                session.merge(tag_)
                session.commit()

            return {"message": "Tag updated successfully", "status_code": 200}

        except Exception as e:
            return {"error": f"Error updating tag - {e}", "status_code": 400}
    
    def delete_tag(self, user_id: int, tag: str) -> dict:
        """Deletes a tag from the database for a user"""
        tag_ = self.get_tag(user_id=user_id, tag=tag)
        if not tag_:
            return {"error": f"Tag:{tag} doesn't exist for User:{user_id}", "status_code": 404}
    
        try:
            with SessionManager(db_url=DB_URL) as session:
                session.merge(tag_)
                session.delete(tag_)
                session.commit()
            
            return {"message": "Tag deleted successfully", "status_code": 200}
        
        except Exception as e:
            return {"error": f"Error deleting tag - {e}", "status_code": 400}


class TaskData:
    """Class to read and write data from/to the tasks table"""
    def create_task(self, user_id: int, title: str, description: str=None, tag_id: int=None, due_date: datetime=None, priority: str=None) -> dict:
        """Creates a new task for a user"""
        user = UserData().get_user(user_id=user_id)
        if not user:
            return {"error": f"User:{user_id} doesn't exist", "status_code": 404}

        try:
            with SessionManager(db_url=DB_URL) as session:
                new_task = Task(user_id=user_id, title=title)
                
                # Optional Parameters
                if description:
                    new_task.description = description

                if tag_id:
                    try:
                        tag_data = TagData().get_tag(user_id=user_id, tag_id=tag_id)
                        new_task.tag_id = tag_data.tag_id
                
                    except AttributeError as e:
                        return {"error": f"Tag:{tag_id} doesn't exist for User:{user_id}", "status_code": 404}
                
                if due_date:
                    new_task.due_date = due_date

                if priority:
                    new_task.priority = priority.value
                
                session.add(new_task)
                session.commit()

            return {"message": "Task created successfully", "status_code": 201}
        
        except Exception as e:
            return {"error": f"Error adding new task - {e}", "status_code": 400}
    
    def update_task(
            self, user_id: int, task_id: int, title: str=None, description: str=None,
            tag_id: int=None, due_date: datetime=None, priority: TaskPriority=None, status: TaskStatus=None
        ) -> dict:
        """Updates the task with the new title, description, status and tag if the task exists"""
        
        task = self.get_task(user_id=user_id, task_id=task_id)
        if not task:
            return {"error": f"Task:{task_id} doesn't exist for User:{user_id}", "status_code": 404}
        
        try:
            if title:
                task.title = title
            
            if description:
                task.description = description
            
            if tag_id:
                try:
                    tag_data = TagData().get_tag(user_id=user_id, tag_id=tag_id)
                    task.tag_id = tag_data.tag_id

                except AttributeError as e:
                    return {"error": f"Tag:{tag_id} doesn't exist for User:{user_id}", "status_code": 404}
            
            if due_date:
                task.due_date = due_date
            
            if priority:
                task.priority = priority.value
            
            if status:
                task.status = status.value

            with SessionManager(db_url=DB_URL) as session:
                session.merge(task)
                session.commit()

            return {"message": "Task updated successfully", "status_code": 200}

        except Exception as e:
            return {"error": f"Error updating task - {e}", "status_code": 400}
    
    def delete_task(self, user_id: int, task_id: int) -> dict:
        """Delete task from the database by user_id and task_id"""
        task = self.get_task(user_id=user_id, task_id=task_id)
        if not task:
            return {"error": f"Task:{task_id} doesn't exist for User:{user_id}", "status_code": 404}
        
        try:
            with SessionManager(db_url=DB_URL) as session:
                session.merge(task)
                session.delete(task)
                session.commit()
            
            return {"message": "Task deleted successfully", "status_code": 200}
            
        except Exception as e:
            return {"error": f"Error deleting task - {e}", "status_code": 400}
    
    def get_task(self, user_id: int, task_id: int) -> Task:
        """Read and return data from the db filter by user_id and task_id"""
        with SessionManager(db_url=DB_URL) as session:
            task = session.query(Task).filter_by(user_id=user_id, task_id=task_id).first()
            return task
    
    def get_all_tasks(self, user_id: int) -> List[Task]:
        """Returns all tasks for a user"""
        with SessionManager(db_url=DB_URL) as session:
            tasks = session.query(Task).filter_by(user_id=user_id).all()
            breakpoint()
            return tasks
    
    def get_tasks_by_tag_id(self, user_id: int, tag_id: int) -> List[Task]:
        """Returns all tasks for a user for a specific tag"""
        with SessionManager(db_url=DB_URL) as session:
            tasks = session.query(Task).filter_by(user_id=user_id, tag_id=tag_id).all()
            return tasks
    
    def get_tasks_by_status(self, user_id: int, status: str) -> List[Task]:
        """Returns all tasks for a user for a specific status"""
        with SessionManager(db_url=DB_URL) as session:
            tasks = session.query(Task).filter_by(user_id=user_id, status=status).all()
            return tasks
        
    def get_tasks_by_priority(self, user_id: int, priority: str) -> List[Task]:
        """Returns all tasks for a user for a specific priority"""
        with SessionManager(db_url=DB_URL) as session:
            tasks = session.query(Task).filter_by(user_id=user_id, priority=priority).all()
            return tasks
        
    def search_tasks_by_text(self, user_id: int, text: str) -> List[Task]:
        """Returns all tasks for a user by searching for a sub sting in the title or description"""
        with SessionManager(db_url=DB_URL) as session:
            tasks1 = session.query(Task).filter(Task.user_id == user_id, Task.title.ilike(f"%{text}%")).all()
            task2 = session.query(Task).filter(Task.user_id == user_id, Task.description.ilike(f"%{text}%")).all()
            data = list(set(tasks1 + task2)) # Remove duplicates from tasks1 + tasks2
            return data
    
    def auto_update_task_status_to_overdue(self) -> dict:
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
                    with SessionManager(db_url=DB_URL) as session:
                        session.merge(task)
                        session.commit()
        
        return {"message": "Tasks' status refreshed!", "status_code": 200}


class TokenData:
    """Class to read and write data from/to the revoked_tokens table"""
    def revoke_token(self, token: str) -> dict:
        """Revoke a JWT token"""
        try:
            with SessionManager(db_url=DB_URL) as session:
                new_revoked_token = RevokedToken(token=token)
                session.add(new_revoked_token)
                session.commit()
            
            return {"message": "Token revoked successfully", "status_code": 200}
            
        except Exception as e:
            return {"error": f"Error revoking token - {e}", "status_code": 400}
        
    
    def check_if_token_revoked(self, token: str) -> bool:
        """Check if a token is revoked"""
        with SessionManager(db_url=DB_URL) as session:
            data = session.query(RevokedToken).filter_by(token=token).first()
        
        return bool(data)
