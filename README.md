# Todo App
This is a simple Todo App built with FastAPI and SQLAlchemy. It allows users to create, read, update, and delete tasks.

## Libraries Used
- FastAPI
- SQLAlchemy
- Alembic
- Passlib
- Uvicorn
- bcrypt
- PyJWT
- Python-multipart

## Installation

### Clone the repository
```bash
git clone https://github.com/abhisekrout7711/Todo
```

### Create a Conda environment and activate it
```bash
conda create --name todo-app python=3.8.2 -y
conda activate todo-app
```

### Install the dependencies
```bash
pip install -r requirements.txt
```

### Configure the database
Update the database connection string in `alembic.ini`.

### Apply database migrations
```bash
alembic upgrade head
```

### Set Python Path to your Project's root directory
```bash
export PYTHONPATH=$PYTHONPATH:/Users/abhisekrout/Desktop/Todo
```

### Run the application (Using Uvicorn)
```bash
uvicorn backend.main:application --reload
```
### Run the application (Simply running main.py)
```bash
python backend/main.py
```

## Usage

1. **Register a new user**
   - Send a `POST` request to `/api/user/register` with `username` and `password`.

2. **Login with the registered user**
   - Send a `POST` request to `/api/user/login` with `username` and `password`.
   - You will receive a JWT token in the response.

3. **Create, read, update, and delete tasks**
   - Use the appropriate API endpoints listed below and include the JWT token in the `Authorization` header as a bearer token.

## Contribution Guidelines

1. Fork the repository
2. Create a new branch
3. Make the changes
4. Create a pull request

## Alembic Commands
- Initialize Alembic:
  ```bash
  alembic init alembic
  ```
- Create a new migration:
  ```bash
  alembic revision --autogenerate -m "Description of the migration"
  ```
- Apply migrations:
  ```bash
  alembic upgrade head
  ```
- Rollback the last migration:
  ```bash
  alembic downgrade -1
  ```

## API Endpoints

### User
- **POST** `/api/user/register`: Register a new user
- **POST** `/api/user/login`: Login with the registered user
- **POST** `/api/user/logout`: Logout the current user
- **POST** `/api/user/delete`: Delete the current user

### Task
- **POST** `/api/task/create`: Create a new task
- **GET** `/api/task/all`: Get all tasks for the current user
- **GET** `/api/task/{task_id}`: Get a specific task for the current user
- **PATCH** `/api/task/{task_id}`: Update a specific task for the current user
- **DELETE** `/api/task/{task_id}`: Delete a specific task for the current user
- **GET** `/api/task/status`: Get all tasks for the current user filtered by a specific status
- **GET** `/api/task/priority`: Get all tasks for the current user filtered by a specific priority
- **GET** `/api/task/text`: Search for tasks by text

### Tag
- **GET** `/api/tag/all`: Get all tags for the current user
- **POST** `/api/tag/create`: Create a new tag for the current user
- **DELETE** `/api/tag/{tag}`: Delete a specific tag for the current user
- **PUT** `/api/tag/{tag}`: Update a specific tag for the current user

### Admin
- **GET** `/api/admin/{user_id}`: Get a specific user from the database (admin only)
- **GET** `/api/admin/all`: Get all users from the database (admin only)
- **GET** `/api/admin/recently_active`: Get recently active users (admin only)
- **DELETE** `/api/admin/{user_id}`: Delete a specific user from the database (admin only)
