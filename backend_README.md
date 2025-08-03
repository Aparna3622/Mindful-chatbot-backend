# STAN Chatbot Backend

A lightweight Flask API backend for the STAN conversational chatbot.

## 🚀 Features

- RESTful API endpoints for chat functionality
- In-memory session management
- Sentiment analysis
- CORS enabled for frontend integration
- Health monitoring endpoints
- JSON response format with metadata

## 📋 Requirements

- Python 3.7+
- Flask 3.1.1
- Flask-CORS 4.0.0

## 🔧 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/stan-chatbot-backend.git
   cd stan-chatbot-backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

### Local Development
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Production Deployment

#### Railway
1. Connect this repository to Railway
2. Deploy automatically

#### Heroku
1. Create Heroku app:
   ```bash
   heroku create your-stan-backend
   ```
2. Deploy:
   ```bash
   git push heroku main
   ```

## 📊 API Endpoints

### POST /chat
Send a message to the chatbot.

**Request:**
```json
{
    "message": "Hello!",
    "session_id": "optional-session-id"
}
```

**Response:**
```json
{
    "response": "Hello! I'm STAN, your AI assistant. How can I help you today?",
    "session_id": "session_123",
    "sentiment": "positive",
    "context": "Conversation has 1 exchanges"
}
```

### GET /health
Check API health status.

**Response:**
```json
{
    "status": "healthy",
    "model_loaded": true,
    "storage_type": "In-Memory",
    "active_sessions": 5,
    "total_sessions": 10,
    "timestamp": "2025-08-03T12:00:00"
}
```

### GET /stats
Get session statistics.

**Response:**
```json
{
    "total_sessions": 10,
    "active_sessions": 5,
    "total_messages": 42,
    "storage_type": "In-Memory"
}
```

### GET /data
View all stored conversation data (development only).

## 🔒 CORS Configuration

The backend is configured to accept requests from:
- `https://*.vercel.app`
- `https://*.netlify.app`
- `https://*.github.io`
- `http://localhost:3000`
- `http://localhost:8080`

## 🌍 Environment Variables

- `PORT` - Server port (default: 5000)
- `FLASK_ENV` - Environment (production/development)

## 📁 Project Structure

```
stan-chatbot-backend/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── Procfile           # Heroku deployment config
├── runtime.txt        # Python version (optional)
└── README.md          # This file
```

## 🧪 Testing

Test the health endpoint:
```bash
curl https://your-backend-url.railway.app/health
```

Test the chat API:
```bash
curl -X POST https://your-backend-url.railway.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "session_id": "test"}'
```

## 🔄 Integration

This backend is designed to work with the STAN Chatbot frontend. Update your frontend configuration:

```javascript
const CONFIG = {
    API_BASE_URL: 'https://your-backend-url.railway.app'
};
```

## 📝 License

This project is part of the STAN Internship Challenge.

## 🆘 Support

For issues and questions, please check the API endpoints and ensure CORS is properly configured for your frontend domain.
