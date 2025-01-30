# Inside backend/Dockerfile
FROM python:3.12.8-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app/backend"

# Install system dependencies (if needed for psycopg2, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Set workdir and copy files
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Expose port and run the app
EXPOSE 8080
CMD ["uvicorn", "backend.app.main:application", "--host", "0.0.0.0", "--port", "8080"]
