from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, DATE, ForeignKey, Enum, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

import enum

Base = declarative_base()

# Enum Definitions
class TaskStatus(enum.Enum):
    Pending = "Pending"
    Completed = "Completed"
    Overdue = "Overdue"


class TaskPriority(enum.Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"


# Admin Model
class Admin(Base):
    __tablename__ = 'admins'

    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<Admin(user_id={self.admin_id}, username={self.username})>"
    

# User Model
class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationship to access tasks of the user
    tasks = relationship('Task', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User(user_id={self.user_id}, username={self.username})>"


# Tag Model
class Tag(Base):
    __tablename__ = 'tags'

    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    tag = Column(String(255), nullable=False)

    # Relationship to access tasks of the tag
    tasks = relationship('Task', back_populates='tag_relation')

    def __repr__(self):
        return f"<Tag(id={self.tag_id}, tag={self.tag})>"


# Task Model
class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    tag_id = Column(Integer, ForeignKey('tags.tag_id', ondelete='SET NULL'), nullable=True)
    tag = Column(String(255), nullable=True)
    due_date = Column(DATE, nullable=True)
    priority = Column(Enum(TaskPriority), default=TaskPriority.Medium.value, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.Pending.value, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationship to the User model
    user = relationship('User', back_populates='tasks')

    # Relationship to the Tag model
    tag_relation = relationship('Tag', back_populates='tasks')

    def __repr__(self):
        return f"<Task(task_id={self.task_id}, title={self.title}, status={self.status}, tag={self.tag_id})>"


class RevokedToken(Base):
    __tablename__ = 'revoked_tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(255), nullable=False)
