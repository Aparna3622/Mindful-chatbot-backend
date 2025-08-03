# Backend Development Guide

This guide covers the backend architecture, API development, and customization options for the STAN Chatbot.

## Overview

The backend is a lightweight Flask application that provides AI-powered chat responses, sentiment analysis, and session management. It's designed to be simple, scalable, and easy to deploy.

## Architecture

```
Backend Structure
├── Flask Application
│   ├── Route Handlers
│   ├── CORS Configuration
│   └── Error Handling
├── Chatbot Engine
│   ├── Response Generation
│   ├── Sentiment Analysis
│   └── Pattern Matching
├── Session Management
│   ├── In-Memory Storage
│   ├── Session Tracking
│   └── History Management
└── API Endpoints
    ├── Chat (/chat)
    ├── Health (/health)
    ├── Stats (/stats)
    └── Data (/data)
```

## Core Components

### Flask Application

```python
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# CORS Configuration
CORS(app, 
     origins=[
         "https://mindful-chatbot.vercel.app",
         "https://*.vercel.app",
         # ... other origins
     ],
     methods=["GET", "POST", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True
)
```

### Chatbot Engine

The `SimpleChatbot` class handles all AI functionality:

```python
class SimpleChatbot:
    def __init__(self):
        self.responses = {
            'greeting': [
                "Hello! I'm STAN, your AI assistant. How can I help you today?",
                # ... more responses
            ],
            # ... other categories
        }
    
    def analyze_sentiment(self, text):
        """Simple sentiment analysis using keyword matching"""
        # Implementation details
    
    def generate_response(self, user_input, history=None):
        """Generate contextual responses based on patterns"""
        # Implementation details
```

### Session Management

```python
# Global session storage
chat_sessions = {}

def manage_session(session_id, user_message, bot_response, sentiment):
    """Store conversation in session history"""
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    
    history = chat_sessions[session_id]
    history.append({
        'user': user_message,
        'bot': bot_response,
        'timestamp': datetime.now().isoformat(),
        'sentiment': sentiment
    })
    
    # Keep only last 10 exchanges
    if len(history) > 10:
        history = history[-10:]
    
    chat_sessions[session_id] = history
```

## API Endpoints

### 1. Chat Endpoint

Handles incoming chat messages and returns bot responses.

```python
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Process message
        sentiment = chatbot.analyze_sentiment(user_message)
        bot_response = chatbot.generate_response(user_message, history)
        
        # Store in session
        manage_session(session_id, user_message, bot_response, sentiment)
        
        return jsonify({
            'response': bot_response,
            'session_id': session_id,
            'sentiment': sentiment,
            'context': f"Conversation has {len(history)} exchanges"
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500
```

### 2. Health Check Endpoint

Provides system status and monitoring information.

```python
@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'model_loaded': True,
        'storage_type': 'In-Memory',
        'active_sessions': len(chat_sessions),
        'total_sessions': len(chat_sessions),
        'timestamp': datetime.now().isoformat()
    })
```

### 3. Statistics Endpoint

Returns usage statistics and metrics.

```python
@app.route('/stats')
def stats():
    total_messages = sum(len(session) for session in chat_sessions.values())
    
    return jsonify({
        'total_sessions': len(chat_sessions),
        'active_sessions': len(chat_sessions),
        'total_messages': total_messages,
        'storage_type': 'In-Memory'
    })
```

### 4. Data Endpoint

Provides access to stored conversation data.

```python
@app.route('/data')
def view_data():
    return jsonify({
        'storage_type': 'In-Memory',
        'total_sessions': len(chat_sessions),
        'sessions': chat_sessions,
        'data_structure': {
            'session_id': 'Contains array of conversation exchanges',
            'each_exchange': {
                'user': 'User message',
                'bot': 'Bot response',
                'timestamp': 'When message was sent',
                'sentiment': 'Detected sentiment'
            }
        }
    })
```

## CORS Configuration

### Comprehensive CORS Setup

```python
# Primary CORS configuration
CORS(app, 
     origins=[
         "https://mindful-chatbot.vercel.app",  # Production frontend
         "https://*.vercel.app",                # Vercel wildcards
         "https://*.netlify.app",               # Netlify support
         "https://*.github.io",                 # GitHub Pages
         "http://localhost:3000",               # Local development
         "http://127.0.0.1:3000",              # Local development
         "http://localhost:8080"                # Alternative local port
     ],
     methods=["GET", "POST", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True
)

# Additional CORS headers
@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    if origin in ['https://mindful-chatbot.vercel.app', 'http://localhost:3000']:
        response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Preflight request handlers
@app.route('/chat', methods=['OPTIONS'])
def chat_options():
    return jsonify({}), 200

@app.route('/health', methods=['OPTIONS'])
def health_options():
    return jsonify({}), 200
```

## Chatbot Intelligence

### Response Categories

The chatbot recognizes several message types:

1. **Greetings**
   ```python
   'greeting': [
       "Hello! I'm STAN, your AI assistant. How can I help you today?",
       "Hi there! I'm here to assist you. What can I do for you?",
       "Welcome! I'm STAN. What would you like to know?",
   ]
   ```

2. **How are you**
   ```python
   'how_are_you': [
       "I'm doing great, thank you for asking! How are you?",
       "I'm functioning well and ready to help! How can I assist you?",
   ]
   ```

3. **Jokes**
   ```python
   'jokes': [
       "Why don't scientists trust atoms? Because they make up everything! 😄",
       "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾",
       # ... more jokes
   ]
   ```

### Pattern Matching

```python
def generate_response(self, user_input, history=None):
    user_input_lower = user_input.lower()
    
    # Greeting patterns
    if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return random.choice(self.responses['greeting'])
    
    # Joke patterns
    elif any(phrase in user_input_lower for phrase in ['joke', 'funny', 'make me laugh']):
        return random.choice(self.responses['jokes'])
    
    # Default response
    else:
        return random.choice(self.responses['default'])
```

### Sentiment Analysis

Simple keyword-based sentiment analysis:

```python
def analyze_sentiment(self, text):
    positive_words = ['good', 'great', 'excellent', 'happy', 'love', 'wonderful', 'amazing']
    negative_words = ['bad', 'terrible', 'sad', 'hate', 'awful', 'horrible', 'angry']
    
    text_lower = text.lower()
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return 'positive'
    elif negative_count > positive_count:
        return 'negative'
    else:
        return 'neutral'
```

## Error Handling

### Exception Management

```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Route-specific error handling
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Route logic
        pass
    except ValidationError as e:
        return jsonify({'error': f'Validation error: {str(e)}'}), 400
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500
```

### Logging

```python
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Usage in routes
logger.info("✅ Lightweight chatbot initialized")
logger.error(f"Error in chat endpoint: {e}")
```

## Testing

### Unit Tests

```python
import unittest
from app_backend_only import chatbot

class TestChatbot(unittest.TestCase):
    def test_sentiment_analysis(self):
        # Test positive sentiment
        result = chatbot.analyze_sentiment("I love this app!")
        self.assertEqual(result, 'positive')
        
        # Test negative sentiment
        result = chatbot.analyze_sentiment("This is terrible")
        self.assertEqual(result, 'negative')
        
        # Test neutral sentiment
        result = chatbot.analyze_sentiment("Hello there")
        self.assertEqual(result, 'neutral')
    
    def test_response_generation(self):
        response = chatbot.generate_response("hello")
        self.assertIn("Hello", response)
```

### API Testing

```python
import requests

def test_health_endpoint():
    response = requests.get('http://localhost:5000/health')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'healthy'

def test_chat_endpoint():
    response = requests.post('http://localhost:5000/chat', json={
        'message': 'Hello',
        'session_id': 'test-session'
    })
    assert response.status_code == 200
    data = response.json()
    assert 'response' in data
    assert 'sentiment' in data
```

## Performance Optimization

### Memory Management

```python
# Limit session history
MAX_HISTORY_LENGTH = 10

def manage_session(session_id, message, response, sentiment):
    # ... existing code ...
    
    # Keep only recent exchanges
    if len(history) > MAX_HISTORY_LENGTH:
        history = history[-MAX_HISTORY_LENGTH:]
```

### Response Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_response(message_hash):
    """Cache frequently requested responses"""
    # Implementation details
```

### Database Integration (Future Enhancement)

```python
# Example MongoDB integration
from pymongo import MongoClient

class DatabaseChatbot(SimpleChatbot):
    def __init__(self):
        super().__init__()
        self.db = MongoClient(os.environ.get('MONGODB_URI'))
    
    def store_session(self, session_id, data):
        """Store session data in database"""
        self.db.sessions.update_one(
            {'session_id': session_id},
            {'$set': data},
            upsert=True
        )
```

## Security Considerations

### Input Validation

```python
def validate_message(message):
    """Validate user input"""
    if not message or not isinstance(message, str):
        raise ValidationError("Invalid message format")
    
    if len(message) > 1000:  # Character limit
        raise ValidationError("Message too long")
    
    # Sanitize input
    message = message.strip()
    return message
```

### Rate Limiting (Future Enhancement)

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/chat', methods=['POST'])
@limiter.limit("10 per minute")
def chat():
    # Route implementation
```

## Deployment Configuration

### Environment Variables

```python
import os

# Production settings
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
PORT = int(os.environ.get('PORT', 5000))
HOST = os.environ.get('HOST', '0.0.0.0')

# Database configuration (if using external DB)
DATABASE_URL = os.environ.get('DATABASE_URL')
MONGODB_URI = os.environ.get('MONGODB_URI')

# API keys (for future AI integrations)
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
```

### Production Configuration

```python
if __name__ == '__main__':
    # Production settings
    logger.info("🚀 Starting STAN Chatbot Backend...")
    app.run(
        debug=DEBUG,
        host=HOST,
        port=PORT
    )
```

## Monitoring and Logging

### Health Monitoring

```python
import psutil
from datetime import datetime

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'uptime': get_uptime(),
        'memory_usage': psutil.virtual_memory().percent,
        'cpu_usage': psutil.cpu_percent(),
        'active_sessions': len(chat_sessions)
    })
```

### Request Logging

```python
@app.before_request
def log_request_info():
    logger.info(f'Request: {request.method} {request.url}')
    logger.info(f'Headers: {request.headers}')

@app.after_request
def log_response_info(response):
    logger.info(f'Response: {response.status_code}')
    return response
```

## Future Enhancements

### AI Integration

```python
# OpenAI GPT integration example
import openai

class AIEnhancedChatbot(SimpleChatbot):
    def __init__(self):
        super().__init__()
        openai.api_key = os.environ.get('OPENAI_API_KEY')
    
    def generate_ai_response(self, message, history):
        """Generate response using OpenAI GPT"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are STAN, a helpful AI assistant."},
                    {"role": "user", "content": message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return self.generate_response(message, history)  # Fallback
```

### Database Storage

```python
# PostgreSQL integration example
import psycopg2
from psycopg2.extras import RealDictCursor

class DatabaseManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            os.environ.get('DATABASE_URL'),
            cursor_factory=RealDictCursor
        )
    
    def store_conversation(self, session_id, user_message, bot_response, sentiment):
        """Store conversation in database"""
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO conversations (session_id, user_message, bot_response, sentiment, timestamp) VALUES (%s, %s, %s, %s, %s)",
                (session_id, user_message, bot_response, sentiment, datetime.now())
            )
            self.conn.commit()
```

## Contributing

When contributing to the backend:

1. Follow PEP 8 style guidelines
2. Add type hints for better code documentation
3. Write comprehensive tests for new features
4. Update API documentation
5. Ensure proper error handling
6. Add logging for debugging purposes

## Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-CORS Documentation](https://flask-cors.readthedocs.io/)
- [Python Logging](https://docs.python.org/3/library/logging.html)

### Tools
- [Postman](https://www.postman.com/) for API testing
- [pytest](https://pytest.org/) for testing
- [Black](https://black.readthedocs.io/) for code formatting
