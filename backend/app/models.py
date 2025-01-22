from sqlalchemy import Column, Integer, String, Text, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database import get_database_connection

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
        return f"<User(user_id={self.user_}, email={self.email})>"

class Tag(Base):
    __tablename__ = 'tags'

    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

    # Relationship to tasks that are tagged with this tag
    tasks = relationship('Task', back_populates='tag')

    def __repr__(self):
        return f"<Tag(tag_id={self.tag_id}, name={self.name})>"

class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)  # Link to User table
    tag_id = Column(Integer, ForeignKey('tags.tag_id'), nullable=False)  # Link to Tag table
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum('Pending', 'In Progress', 'Completed', 'Overdue', name="task_status"), default='Pending')
    due_date = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
    priority = Column(Enum('Low', 'Medium', 'High', name="task_priority"), default='Medium')

    # Relationship to the User model and Tag Model
    user = relationship('User', back_populates='tasks')
    tag = relationship('Tag', back_populates='tasks')

    def __repr__(self):
        return f"<Task(task_id={self.task_id}, title={self.title}, status={self.status})>"


if __name__=="__main__":
    from sqlalchemy.orm import sessionmaker

    # Set up the database engine and session
    engine = get_database_connection()

    Session = sessionmaker(bind=engine)
    session = Session()

    # # Create a new user
    # new_user = User(email="user2@xyz.com", password_hash="hashedpassword")
    # session.add(new_user)

    # session.commit()
    # # Create a new tag
    # new_tag = Tag(name="Personal")
    # session.add(new_tag)

    # session.commit()

    # # Create a new task
    # new_task = Task(
    #     user_id=new_user.user_id, 
    #     tag_id=new_tag.tag_id, 
    #     title="Complete project", 
    #     description="Random", 
    #     status="Pending", 
    #     priority="High"
    # )
    # session.add(new_task)

    # # Commit the transaction
    # session.commit()

    # Query and print tasks for the user
    tasks_for_user = session.query(Task).all()
    for task in tasks_for_user:
        breakpoint()
        print(task)
