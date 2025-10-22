# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables to prevent generating .pyc files and to run
# Python in unbuffered mode, which is recommended for containers
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies that might be needed by your Python packages
# (e.g., mysqlclient needs libmysqlclient-dev)
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY ./vehicleassistance/vbams/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project into the container at /app
COPY ./vehicleassistance/vbams/ .

# Expose the port Render provides
EXPOSE 10000

# Define the command to run your application using Gunicorn
# This will be the entrypoint for your container
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "vbams.wsgi"]