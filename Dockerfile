# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8000 for the API
EXPOSE 8000

# Default command to run the FastAPI server
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
