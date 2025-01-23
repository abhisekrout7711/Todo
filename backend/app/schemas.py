# Standard Imports
from enum import Enum as enum_Enum

# Third-Party Imports
from sqlalchemy import Column, Integer, String, Text, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class TaskStatus(enum_Enum):
    Pending = "Pending"
    Completed = "Completed"
    InProgress = "In Progress"
    Overdue = "Overdue"


class TaskPriority(enum_Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationship to access tasks of the user
    tasks = relationship('Task', back_populates='user')

    def __repr__(self):
        return f"<User(user_id={self.user_id}, username={self.username})>"


class Tag(Base):
    __tablename__ = 'tags'

    tag = Column(String(255), primary_key=True, nullable=False)

    # Relationship to access tasks of the tag
    tasks = relationship('Task', back_populates='tag_relation')

    def __repr__(self):
        return f"<Tag(tag={self.tag})>"


class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)  # Link to User table
    tag = Column(String(255), ForeignKey('tags.tag', ondelete='SET NULL'))  # Link to Tag table
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default='Pending')
    due_date = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
    priority = Column(Enum(TaskPriority), default='Medium', nullable=False)

    # Relationship to the User model
    user = relationship('User', back_populates='tasks')

    # Relationship to the Tag model
    tag_relation = relationship('Tag', back_populates='tasks', passive_deletes=True)

    def __repr__(self):
        return f"<Task(task_id={self.task_id}, title={self.title}, status={self.status}, tag={self.tag})>"
