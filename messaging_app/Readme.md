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

## Notes
- **Authentication Required**: JWT authentication is required for most endpoints. The token should be included in the `Authorization` header as a Bearer token.
- **Refresh Tokens**: When the `access_token` expires, a `refresh_token` can be used to obtain a new access token.
- **Anonymous Users**: Some endpoints are accessible to all users, including anonymous ones (like registration and login).

---
