# Use the official Python 3.10 image from Docker Hub as the base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project code into the container
COPY messaging_app /app/

# Expose port 8000 for the Django app
EXPOSE 8000

# Set the environment variable to avoid Python writing .pyc files to disk
ENV PYTHONUNBUFFERED 1



# Copy the wait-for-it.sh script
COPY wait-for-it /app/

# Set execute permissions for the script
RUN chmod +x /app/wait-for-it.sh

# Run the Django app, ensuring MySQL is ready first
CMD ["bash", "/app/wait-for-it/wait-for-it.sh", "db:3306", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]
