# Messaging API

## Overview
This API enables users to register, log in, and engage in conversations by sending messages. JWT authentication is required for most endpoints.

## Authentication
- The API uses JWT tokens for authentication.
- Users receive an `access_token` after login for authorization.

## Notes
- Users can register and log in to access the messaging system.
- Conversations are created between users.
- Messages can be sent within conversations.
- Authentication is required for most actions.
- Pagination is available for listing messages.
- JWT tokens can be refreshed to maintain authentication.

## Response Format
All responses are in JSON format.

