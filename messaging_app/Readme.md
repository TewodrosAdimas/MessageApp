---

# Messaging API

## Overview
The Messaging API allows users to register, log in, create conversations, and send messages. JWT (JSON Web Token) authentication is required for most endpoints to ensure secure access.

## Authentication
- **JWT Authentication**: This API uses JWT tokens for secure user authentication.
- **Access Tokens**: Upon login, users receive an `access_token` which is used for authorization in subsequent requests.
- **Token Expiry & Refresh**: The access token has an expiry, and users can refresh the token to maintain their session.

## Endpoints

### User Registration and Login
- **Register**: Allows new users to sign up with their details.
- **Login**: Users authenticate and receive a JWT `access_token` for accessing the system.

### Conversations
- **Create Conversation**: Users can create a new conversation with other participants.
- **List Conversations**: Retrieve a list of conversations that the authenticated user is a participant in.
- **Get Conversation Details**: View details of a specific conversation.

### Messages
- **Send Message**: Send a message to an existing conversation.
- **List Messages**: Retrieve messages from a conversation, with pagination support.

### Pagination
- Pagination is supported for listing messages in a conversation. The number of messages per page is configurable, and you can adjust the page size via query parameters.

## Features
- **User Authentication**: Register and log in using email and password, with JWT tokens for authentication.
- **Conversations**: Create, list, and manage conversations with multiple participants.
- **Message Management**: Send and list messages within conversations.
- **Pagination**: Messages are paginated to prevent overwhelming the client with large sets of data.
- **Request Logging Middleware**: All user requests are logged to a file with the timestamp, username (or "Anonymous" for unauthenticated users), and the request path.

## Middleware - Request Logging
We have added a custom middleware that logs each user’s requests to a file. This middleware records the following details:
- **Timestamp**: The time when the request was made.
- **User**: The username of the authenticated user, or "Anonymous" if not logged in.
- **Request Path**: The URL path that the user is accessing.

### How It Works
- The middleware captures the user request in the `__call__` method.
- It logs the details into a file called `user_requests.log` with the format:  
  `"{datetime.now()} - User: {user} - Path: {request.path}"`.

### File Location
The log entries are saved to `user_requests.log` in the root of your project directory. Each entry contains the timestamp, user, and the request path.

## Response Format
All responses are returned in **JSON** format. For example:

### Success Response:
```json
{
    "message": "User registered successfully!",
    "user_id": 123
}
```

### Error Response:
```json
{
    "error": "Invalid participant IDs."
}
```

## Docker & Docker Compose Implementation

This project is containerized using **Docker** and **Docker Compose** for easy deployment and scalability.

### Docker

The **Dockerfile** is used to define the steps for building the Docker image for the Messaging API service. Here's an overview of the key steps:

- **Base Image**: The Dockerfile starts by using the official Python 3.10 image from Docker Hub.
- **Install Dependencies**: It then installs the Python dependencies listed in the `requirements.txt` file.
- **Copy Application Code**: The application code (including Django) is copied into the container.
- **Expose Port**: The container exposes port `8000`, allowing access to the Django application.
- **Wait-for-it Script**: The `wait-for-it.sh` script is copied into the container, ensuring that the MySQL database is ready before starting the Django application.

Here is the relevant Dockerfile for this project:
```Dockerfile
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
```

### Docker Compose

We use **Docker Compose** to define and run multi-container applications. The `docker-compose.yml` file defines two services: `db` (MySQL) and `web` (the Django app). It ensures that the web service waits for the MySQL database service to be ready before starting the application.

Key components of the `docker-compose.yml` file:
- **db**: The MySQL database service, using the official `mysql:8.0` image. Environment variables are set for database credentials.
- **web**: The Django app service, which is built from the current directory. The `wait-for-it.sh` script ensures that MySQL is available before starting the Django app.
- **Volumes**: A volume is defined to persist MySQL data across container restarts.

Here's the relevant `docker-compose.yml` for this project:
```yaml
version: "3.8"

services:
  db:
    image: mysql:8.0
    container_name: messaging_db
    restart: always
    environment:
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"

  web:
    build: .
    container_name: messaging_app
    restart: always
    depends_on:
      - db
    environment:
      DB_NAME: ${MYSQL_DATABASE}
      DB_USER: ${MYSQL_USER}
      DB_PASSWORD: ${MYSQL_PASSWORD}
      DB_HOST: db
      DB_PORT: 3306
    ports:
      - "8000:8000"
    volumes:
      - ./messaging_app:/app
      - ./wait-for-it:/app/wait-for-it

    command: ["bash", "/app/wait-for-it/wait-for-it.sh", "db:3306", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]

volumes:
  mysql_data:
```

### Wait-for-it

The **`wait-for-it`** script is used to ensure that the web service (Django application) does not start until the database (MySQL) is fully ready to accept connections. This is particularly useful in containerized environments, where services may take time to initialize.

- The `wait-for-it.sh` script checks if the database is available at the specified address (`db:3306`). Once it confirms that the database is ready, it starts the Django application by running `python manage.py runserver`.

To learn more about how `wait-for-it` works, you can visit [this repository](https://github.com/vishnubob/wait-for-it).

## Notes
- **Docker & Docker Compose**: Docker and Docker Compose simplify the deployment of the application by containerizing the web and database services. These tools allow you to easily run, scale, and manage your application with minimal configuration.
- **Environment Variables**: Make sure to set the necessary environment variables in your `.env` file for both the web and db services to properly configure the MySQL database connection.
- **Starting the Application**: You can use `docker-compose up` to start the entire application stack (both the Django app and MySQL). The `wait-for-it` script ensures the proper startup order.

--- 

