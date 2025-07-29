FROM python:3.11-slim-buster

# Set the working directory inside the container
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port your FastAPI app will listen on
EXPOSE 8000
