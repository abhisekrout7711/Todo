from sqlalchemy import Column, Integer, String, Text, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationship to access tasks of the user
    tasks = relationship('Task', back_populates='user')

    def __repr__(self):
        return f"<User(user_id={self.user_id}, email={self.email})>"


class Tag(Base):
    __tablename__ = 'tags'

    name = Column(String(255), primary_key=True, nullable=False)

    # Relationship to access tasks of the tag
    tasks = relationship('Task', back_populates='tag')

    def __repr__(self):
        return f"<Tag(tag={self.name})>"


class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)  # Link to User table
    tag = Column(String(255), ForeignKey('tags.name', ondelete='SET NULL'))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum('Pending', 'In Progress', 'Completed', 'Overdue', name="todo_task_status"), default='Pending')
    due_date = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
    priority = Column(Enum('Low', 'Medium', 'High', name="todo_task_priority"), default='Medium')

    # Relationship to the User model
    user = relationship('User', back_populates='tasks')

    # Relationship to the Tag model
    tag_relation = relationship('Tag', back_populates='tasks')

    def __repr__(self):
        return f"<Task(task_id={self.task_id}, title={self.title}, status={self.status}, tag={self.tag})>"
