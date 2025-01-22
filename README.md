# Todo
Create a Todo App

<!-- Conda Environment -->
conda activate dev_env


<!-- Set Path -->
export PYTHONPATH=$PYTHONPATH:/Users/abhisekrout/Desktop/Todo

<!-- Alembic Commands-->
# alembic.ini added to root dir and the following line was added under [alembic] section
# sqlalchemy.url = postgresql://postgres:admin@localhost:5432/postgres

1. Create Migration
alembic revision --autogenerate -m "Description of the migration"

2. Apply Migration
alembic upgrade head

3. Downgrade Migration
alembic downgrade -1
