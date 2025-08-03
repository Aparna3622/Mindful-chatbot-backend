# API Documentation

## Base URL
- **Production**: `https://mindful-chatbot-backend-2.onrender.com`
- **Local Development**: `http://localhost:5000`

## Authentication
No authentication required for current version.

## Content Type
All requests and responses use `application/json` content type.

## CORS
The API supports Cross-Origin Resource Sharing (CORS) for the following origins:
- `https://mindful-chatbot.vercel.app`
- `https://*.vercel.app`
- `https://*.netlify.app`
- `https://*.github.io`
- `http://localhost:3000`
- `http://127.0.0.1:3000`
- `http://localhost:8080`

## Endpoints

### 1. Root Endpoint
Get API information and available endpoints.

```http
GET /
```

**Response:**
```json
{
  "message": "STAN Chatbot Backend API",
  "version": "1.0.0",
  "endpoints": {
    "/chat": "POST - Send message to chatbot",
    "/health": "GET - Health check",
    "/stats": "GET - Get statistics",
    "/data": "GET - View stored data"
  }
}
```

### 2. Health Check
Check the health and status of the API server.

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "storage_type": "In-Memory",
  "active_sessions": 5,
  "total_sessions": 5,
  "timestamp": "2025-08-03T10:30:00.123456"
}
```

**Response Fields:**
- `status`: Server health status (`"healthy"` or `"unhealthy"`)
- `model_loaded`: Whether the chatbot model is loaded
- `storage_type`: Type of data storage being used
- `active_sessions`: Number of currently active chat sessions
- `total_sessions`: Total number of sessions created
- `timestamp`: Server timestamp in ISO format

### 3. Chat Message
Send a message to the chatbot and receive a response.

```http
POST /chat
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "Hello, how are you?",
  "session_id": "session_abc123"
}
```

**Request Fields:**
- `message` (required): The user's message text
- `session_id` (optional): Unique session identifier. If not provided, a new one will be generated.

**Response:**
```json
{
  "response": "Hello! I'm doing great, thank you for asking! How are you?",
  "session_id": "session_abc123",
  "sentiment": "positive",
  "context": "Conversation has 1 exchanges"
}
```

**Response Fields:**
- `response`: The chatbot's reply message
- `session_id`: The session identifier used for this conversation
- `sentiment`: Detected sentiment of the user's message (`"positive"`, `"negative"`, or `"neutral"`)
- `context`: Brief description of the conversation context

**Error Responses:**
```json
// Empty message
{
  "error": "Empty message"
}
// Status Code: 400

// Internal server error
{
  "error": "Internal server error"
}
// Status Code: 500
```

### 4. Statistics
Get usage statistics for the chatbot.

```http
GET /stats
```

**Response:**
```json
{
  "total_sessions": 10,
  "active_sessions": 10,
  "total_messages": 50,
  "storage_type": "In-Memory"
}
```

**Response Fields:**
- `total_sessions`: Total number of chat sessions created
- `active_sessions`: Number of currently active sessions
- `total_messages`: Total number of messages processed
- `storage_type`: Type of data storage being used

### 5. View Data
Retrieve all stored conversation data (for debugging/monitoring).

```http
GET /data
```

**Response:**
```json
{
  "storage_type": "In-Memory",
  "total_sessions": 2,
  "sessions": {
    "session_abc123": [
      {
        "user": "Hello",
        "bot": "Hi there! How can I help you?",
        "timestamp": "2025-08-03T10:30:00.123456",
        "sentiment": "neutral"
      },
      {
        "user": "Tell me a joke",
        "bot": "Why don't scientists trust atoms? Because they make up everything! 😄",
        "timestamp": "2025-08-03T10:31:00.123456",
        "sentiment": "positive"
      }
    ]
  },
  "data_structure": {
    "session_id": "Contains array of conversation exchanges",
    "each_exchange": {
      "user": "User message",
      "bot": "Bot response",
      "timestamp": "When message was sent",
      "sentiment": "Detected sentiment"
    }
  }
}
```

**Response Fields:**
- `storage_type`: Type of data storage being used
- `total_sessions`: Total number of sessions
- `sessions`: Object containing all session data
- `data_structure`: Description of the data format

## Chatbot Capabilities

### Message Categories
The chatbot can recognize and respond to the following types of messages:

1. **Greetings**: hello, hi, hey, greetings
2. **How are you**: how are you, how are you doing
3. **Jokes**: joke, funny, make me laugh, tell me something funny
4. **Capabilities**: what can you do, help me, capabilities
5. **Thanks**: thank, thanks, appreciate
6. **Default**: Any other message

### Sentiment Analysis
The chatbot performs simple sentiment analysis on user messages using keyword matching:

- **Positive words**: good, great, excellent, happy, love, wonderful, amazing
- **Negative words**: bad, terrible, sad, hate, awful, horrible, angry
- **Neutral**: Messages that don't contain significant positive or negative indicators

### Session Management
- Each session can store up to 10 conversation exchanges
- Older exchanges are automatically removed when the limit is exceeded
- Sessions are stored in memory and will be lost when the server restarts
- Session IDs are generated using UUID4 format

## Rate Limiting
Currently, no rate limiting is implemented. For production use, consider implementing rate limiting to prevent abuse.

## Error Handling
The API implements comprehensive error handling:

- **400 Bad Request**: Invalid or missing required fields
- **500 Internal Server Error**: Server-side errors
- All errors return JSON responses with an `error` field

## CORS Headers
The API includes the following CORS headers:
- `Access-Control-Allow-Origin`
- `Access-Control-Allow-Headers`
- `Access-Control-Allow-Methods`
- `Access-Control-Allow-Credentials`

## Example Usage

### JavaScript (Frontend)
```javascript
// Send a chat message
const response = await fetch('https://mindful-chatbot-backend-2.onrender.com/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Hello, how are you?',
    session_id: 'my-session-123'
  })
});

const data = await response.json();
console.log('Bot response:', data.response);
```

### Python
```python
import requests

# Send a chat message
response = requests.post(
    'https://mindful-chatbot-backend-2.onrender.com/chat',
    json={
        'message': 'Hello, how are you?',
        'session_id': 'my-session-123'
    }
)

data = response.json()
print('Bot response:', data['response'])
```

### cURL
```bash
# Send a chat message
curl -X POST \
  https://mindful-chatbot-backend-2.onrender.com/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "message": "Hello, how are you?",
    "session_id": "my-session-123"
  }'
```
