"""
Lightweight STAN Chatbot Backend - Separate Deployment Version
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging
import json
import uuid
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Enable CORS for frontend deployment
CORS(app, origins=[
    "https://*.vercel.app",
    "https://*.netlify.app", 
    "https://*.github.io",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080"
])

# Simple in-memory storage
chat_sessions = {}

class SimpleChatbot:
    """Lightweight chatbot without heavy ML models"""
    
    def __init__(self):
        self.responses = {
            'greeting': [
                "Hello! I'm STAN, your AI assistant. How can I help you today?",
                "Hi there! I'm here to assist you. What can I do for you?",
                "Welcome! I'm STAN. What would you like to know?",
            ],
            'how_are_you': [
                "I'm doing great, thank you for asking! How are you?",
                "I'm functioning well and ready to help! How can I assist you?",
            ],
            'capabilities': [
                "I can help you with conversations, answer questions, provide assistance with various topics, and even tell jokes!",
                "I'm here to chat, provide information, tell jokes, and help with any questions you might have!",
            ],
            'jokes': [
                "Why don't scientists trust atoms? Because they make up everything! 😄",
                "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾",
                "What do you call a fake noodle? An impasta! 🍝",
                "Why don't eggs tell jokes? They'd crack each other up! 🥚",
                "What do you call a bear with no teeth? A gummy bear! 🐻",
                "Why did the math book look so sad? Because it had too many problems! 📚",
                "What's the best thing about Switzerland? I don't know, but the flag is a big plus! 🇨🇭"
            ],
            'thanks': [
                "You're very welcome! Happy to help!",
                "My pleasure! Is there anything else I can assist you with?",
            ],
            'default': [
                "That's interesting! Tell me more about that.",
                "I understand. What would you like to know more about?",
                "Thanks for sharing that with me. How can I help you further?",
                "I see. What else would you like to discuss?",
            ]
        }
        logger.info("✅ Lightweight chatbot initialized")
    
    def analyze_sentiment(self, text):
        """Simple sentiment analysis"""
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
    
    def generate_response(self, user_input, history=None):
        """Generate response based on keywords"""
        user_input_lower = user_input.lower()
        
        # Greeting patterns
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            import random
            return random.choice(self.responses['greeting'])
        
        # How are you patterns
        elif any(phrase in user_input_lower for phrase in ['how are you', 'how are you doing']):
            import random
            return random.choice(self.responses['how_are_you'])
        
        # Joke patterns
        elif any(phrase in user_input_lower for phrase in ['joke', 'funny', 'make me laugh', 'tell me something funny']):
            import random
            return random.choice(self.responses['jokes'])
        
        # Capabilities patterns
        elif any(phrase in user_input_lower for phrase in ['what can you do', 'help me', 'capabilities']):
            import random
            return random.choice(self.responses['capabilities'])
        
        # Thanks patterns
        elif any(word in user_input_lower for word in ['thank', 'thanks', 'appreciate']):
            import random
            return random.choice(self.responses['thanks'])
        
        # Default response
        else:
            import random
            return random.choice(self.responses['default'])

# Initialize lightweight chatbot
chatbot = SimpleChatbot()

@app.route('/')
def index():
    """API info endpoint"""
    return jsonify({
        'message': 'STAN Chatbot Backend API',
        'version': '1.0.0',
        'endpoints': {
            '/chat': 'POST - Send message to chatbot',
            '/health': 'GET - Health check',
            '/stats': 'GET - Get statistics',
            '/data': 'GET - View stored data'
        }
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages with lightweight processing"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Simple sentiment analysis
        sentiment = chatbot.analyze_sentiment(user_message)
        
        # Get or create session
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []
        
        history = chat_sessions[session_id]
        
        # Generate response
        bot_response = chatbot.generate_response(user_message, history)
        
        # Store conversation
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
        
        # Create context summary
        context = f"Conversation has {len(history)} exchanges"
        
        return jsonify({
            'response': bot_response,
            'session_id': session_id,
            'sentiment': sentiment,
            'context': context
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': True,
        'storage_type': 'In-Memory',
        'active_sessions': len(chat_sessions),
        'total_sessions': len(chat_sessions),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/stats')
def stats():
    """Get session statistics"""
    try:
        total_messages = sum(len(session) for session in chat_sessions.values())
        
        return jsonify({
            'total_sessions': len(chat_sessions),
            'active_sessions': len(chat_sessions),
            'total_messages': total_messages,
            'storage_type': 'In-Memory'
        })
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': 'Failed to get statistics'}), 500

@app.route('/data')
def view_data():
    """View all stored conversation data"""
    try:
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
    except Exception as e:
        logger.error(f"Error viewing data: {e}")
        return jsonify({'error': 'Failed to retrieve data'}), 500

if __name__ == '__main__':
    import os
    # Production settings
    port = int(os.environ.get('PORT', 5000))
    logger.info("🚀 Starting STAN Chatbot Backend...")
    app.run(debug=False, host='0.0.0.0', port=port)
