# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt .

# Install the Python dependencies from the requirements.txt
RUN pip install -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
