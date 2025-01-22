# Standard Imports
from typing import Union

# Local Imports
from config_file import DB_CONFIG
from backend.app.utils import SessionManager, hash_password
from backend.app.schemas import User, Tag, Task


class UserData:
    def __init__(self):
        self.session = SessionManager(**DB_CONFIG).get_session()

    def get_user(self, user_id: int=None, email: str=None) -> Union[User, dict]:
        """Read and return data from the db filter by email"""
        if email:
            data = self.session.query(User).filter_by(email=email).first()

        if user_id:
            data = self.session.query(User).filter_by(user_id=user_id).first()

        if not data:
            return {"error":"User doesn't exist", "status_code": 404}
        
        return data

    def add_user(self, email: str, password: str) -> dict:
        """Adds new user to the db if the user doesn't already exist"""
        data = self.get_user(email)
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
        data = self.get_user(user_id)
        if isinstance(data, dict):
            return data
        
        if new_email:
            data.email = new_email
        
        if new_password:
            new_password_hash = hash_password(new_password)
            data.password_hash = new_password_hash
        
        self.session.commit()
        return {"message": "Password updated successfully", "status_code": 200}
    
    def delete_user(self, user_id: int) -> dict:
        """Delete user from the database by user_id"""
        data = self.get_user(user_id)
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
        
    def get_tag(self, name: str) -> Union[Tag, dict]:
        """Read and return data from the db filter by name"""
        data = self.session.query(Tag).filter_by(name=name).first()
        if not data:
            return {"error":"Tag doesn't exist", "status_code": 404}
        return data
    
    def add_tag(self, name: str) -> dict:
        """Adds new tag to the db if the tag doesn't already exist"""
        data = self.get_tag(name)
        if isinstance(data, Tag):
            return {"error": "Tag already exists", "status_code": 409}

        try:
            new_tag = Tag(name=name)
            self.session.add(new_tag)
            self.session.commit()
            return {"message": "Tag added successfully", "status_code": 201}
        
        except Exception as e:
            return {"error": f"Error adding new tag - {e}", "status_code": 400}

    def update_tag(self, name: str, new_name: str=None) -> dict:
        """Updates the tag with the new name if the tag exists"""
        data = self.get_tag(name)
        if isinstance(data, dict):
            return data

        if new_name:
            data.name = new_name

        self.session.commit()
        return {"message": "Tag updated successfully", "status_code": 200}
    
    def delete_tag(self, name: str) -> dict:
        """Delete tag from the database by tag_id"""
        data = self.get_tag(name)
        if isinstance(data, Tag):
            try:
                self.session.delete(data)
                self.session.commit()
                return {"message": "Tag deleted successfully", "status_code": 200}
            
            except Exception as e:
                return {"error": f"Error deleting tag - {e}", "status_code": 400}
        
        return {"error": "Tag doesn't exist", "status_code": 404}


if __name__=="__main__":
    obj = UserData()
    
    # obj.add_user("user1@gmail.com", "password")
    # breakpoint
    # obj.add_user("user2@gmail.com", "password")
    
    data = obj.get_user(email="user1@gmail.com")
    data = obj.get_user(email="user2@gmail.com")

    breakpoint()
    obj.update_user(user_id=1, new_email="user1_new@gmail.com", new_password="new_password")
    
    obj.update_user(user_id=2, new_password="new_password")    


   