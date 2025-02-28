API endpoints 

### 1. **User Registration**

**POST** `/register/`

- **Request Body (JSON):**
```json
{
  "username": "new_user",
  "email": "new_user@example.com",
  "password": "password123",
  "bio": "This is a bio",
  "profile_picture": "image_url"  // Optional
}
```

- **Expected Response:**
```json
{
  "message": "User registered successfully!",
  "user_id": 1
}
```

### 2. **User Login**

**POST** `/login/`

- **Request Body (JSON):**
```json
{
  "username": "new_user",
  "password": "password123"
}
```

- **Expected Response:**
```json
{
  "user": {
    "id": 1,
    "username": "new_user",
    "email": "new_user@example.com",
    "bio": "This is a bio",
    "profile_picture": "image_url"  // Optional
  },
  "access": "access_token",
  "refresh": "refresh_token"
}
```

### 3. **Create Conversation**

**POST** `/api/conversations/`

- **Request Body (JSON):**
```json
{
  "participants": [1, 2]  // Replace with valid user IDs
}
```

- **Expected Response:**
```json
{
  "id": 1,
  "participants": [
    {
      "id": 1,
      "username": "user1",
      "email": "user1@example.com"
    },
    {
      "id": 2,
      "username": "user2",
      "email": "user2@example.com"
    }
  ],
  "messages": [],
  "created_at": "2025-02-28T12:34:56Z"
}
```

### 4. **List Conversations (Authenticated)**

**GET** `/api/conversations/`

- **Headers:**
  - `Authorization`: `Bearer access_token`

- **Expected Response:**
```json
[
  {
    "id": 1,
    "participants": [
      {
        "id": 1,
        "username": "user1",
        "email": "user1@example.com"
      },
      {
        "id": 2,
        "username": "user2",
        "email": "user2@example.com"
      }
    ],
    "messages": [],
    "created_at": "2025-02-28T12:34:56Z"
  }
]
```

### 5. **Send Message**

**POST** `/api/messages/`

- **Request Body (JSON):**
```json
{
  "conversation": 1,  // The conversation ID
  "text": "Hello, this is a message"
}
```

- **Expected Response:**
```json
{
  "id": 1,
  "sender": {
    "id": 1,
    "username": "user1",
    "email": "user1@example.com"
  },
  "conversation": 1,
  "text": "Hello, this is a message",
  "timestamp": "2025-02-28T12:34:56Z"
}
```

### 6. **List Messages in a Conversation (Authenticated)**

**GET** `/api/conversations/{conversation_id}/messages/`

- **Headers:**
  - `Authorization`: `Bearer access_token`

- **Expected Response:**
```json
[
  {
    "id": 1,
    "sender": {
      "id": 1,
      "username": "user1",
      "email": "user1@example.com"
    },
    "conversation": 1,
    "text": "Hello, this is a message",
    "timestamp": "2025-02-28T12:34:56Z"
  }
]
```

### 7. **Filter Messages (Optional)**

**GET** `/api/messages/`

- **Query Parameters:**
  - `conversation`: `1`  // Filter by conversation ID
  - `page_size`: `10`  // Limit to 10 messages per page

- **Headers:**
  - `Authorization`: `Bearer access_token`

- **Expected Response:**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "sender": {
        "id": 1,
        "username": "user1",
        "email": "user1@example.com"
      },
      "conversation": 1,
      "text": "Hello, this is a message",
      "timestamp": "2025-02-28T12:34:56Z"
    }
  ]
}
```

### 8. **Token Refresh**

**POST** `/api/token/refresh/`

- **Request Body (JSON):**
```json
{
  "refresh": "refresh_token"
}
```

- **Expected Response:**
```json
{
  "access": "new_access_token"
}
```

### 9. **Pagination for Messages (Optional)**

**GET** `/api/messages/`

- **Query Parameters:**
  - `page_size`: `20`
  - `page`: `2`  // For pagination

- **Headers:**
  - `Authorization`: `Bearer access_token`

- **Expected Response:**
```json
{
  "count": 50,
  "next": "http://example.com/api/messages/?page=3",
  "previous": "http://example.com/api/messages/?page=1",
  "results": [
    {
      "id": 21,
      "sender": {
        "id": 1,
        "username": "user1",
        "email": "user1@example.com"
      },
      "conversation": 1,
      "text": "Message 21",
      "timestamp": "2025-02-28T13:45:00Z"
    },
    ...
  ]
}
```
