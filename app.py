from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import json
import uuid
import re
from datetime import datetime
import os
import random

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Enable CORS
CORS(app, origins=[
    "https://mindful-chatbot.vercel.app",
    "https://*.vercel.app",
    "http://localhost:3000"
], methods=["GET", "POST", "OPTIONS"])

# In-memory storage
chat_sessions = {}
user_data = {}

def generate_enhanced_response(user_input, session_id):
    """Enhanced response generation with intelligent patterns"""
    user_input_lower = user_input.lower().strip()
    
    # Handle name introduction
    name_match = re.search(r'my name is (\w+)', user_input_lower)
    if name_match:
        name = name_match.group(1).title()
        user_data[session_id] = user_data.get(session_id, {})
        user_data[session_id]['name'] = name
        return f"Nice to meet you, {name}! I'll remember that. How can I help you today?"
    
    # Handle favorite color
    color_match = re.search(r'my (?:favorite|fav) color is (\w+)', user_input_lower)
    if color_match:
        color = color_match.group(1)
        user_data[session_id] = user_data.get(session_id, {})
        user_data[session_id]['favorite_color'] = color
        return f"{color.title()} is a lovely color! I'll remember that you like {color}."
    
    # Handle memory questions
    if 'what did i say' in user_input_lower or 'did i say' in user_input_lower:
        if session_id in user_data:
            data = user_data[session_id]
            if 'name' in data and 'name' in user_input_lower:
                return f"You told me your name is {data['name']}!"
            elif 'favorite_color' in data and 'color' in user_input_lower:
                return f"You said your favorite color is {data['favorite_color']}!"
        return "I don't recall you mentioning that. Could you tell me again?"
    
    # Greetings
    if any(greeting in user_input_lower for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
        return "Hello! I'm STAN, your AI assistant. How can I help you today?"
    
    # ⭐ FIXED: Casual greetings - THIS WAS THE MISSING PIECE!
    elif any(phrase in user_input_lower for phrase in ["what's up", 'whats up', 'wassup', 'sup', "how's it going"]):
        return "Not much, just here ready to chat with you! What's going on with you?"
    
    # Bot identity questions
    elif ('name' in user_input_lower and any(word in user_input_lower for word in ['your', 'what', 'called'])) or "what's your name" in user_input_lower:
        return "I'm STAN, your AI assistant! It's nice to meet you. What's your name?"
    
    # Bot confirmation
    elif any(phrase in user_input_lower for phrase in ['are you a bot', 'are you real', 'are you human', 'are you ai']):
        return "Yes, I'm STAN, an AI chatbot assistant! I'm here to help and chat with you."
    
    # How are you questions
    elif any(phrase in user_input_lower for phrase in ['how are you', 'how do you feel', 'how is it going']):
        return "I'm doing great, thank you for asking! I'm ready to help you with whatever you need. How are you doing today?"
    
    # Emotional support
    elif any(word in user_input_lower for word in ['sad', 'down', 'depressed', 'upset']):
        return "I'm sorry you're feeling down. Would you like to talk about what's bothering you? I'm here to listen."
    
    elif any(word in user_input_lower for word in ['happy', 'excited', 'great', 'awesome']):
        return "That's wonderful! I love hearing when people are happy. What's made your day so great?"
    
    # Jokes
    elif any(word in user_input_lower for word in ['joke', 'funny', 'humor', 'laugh']):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything! 😄",
            "What do you call a fake noodle? An impasta! 🍝",
            "Why did the scarecrow win an award? He was outstanding in his field! 🌾"
        ]
        return random.choice(jokes)
    
    # Capabilities
    elif any(phrase in user_input_lower for phrase in ['what can you do', 'help me', 'your capabilities']):
        return "I can help with conversations, answer questions, tell jokes, provide support, and much more! What would you like to try?"
    
    # Boredom
    elif any(word in user_input_lower for word in ['bored', 'boring', 'nothing to do']):
        return "Let's fix that boredom! We could chat about your interests, I could tell you a joke, or help you brainstorm activities!"
    
    # Thank you
    elif any(word in user_input_lower for word in ['thank', 'thanks', 'appreciate']):
        return "You're very welcome! I'm glad I could help. Is there anything else you'd like to know or discuss?"
    
    # Goodbye
    elif any(word in user_input_lower for word in ['bye', 'goodbye', 'see you', 'talk later']):
        return "Goodbye! It was great chatting with you. Feel free to come back anytime!"
    
    # Default responses
    else:
        responses = [
            "That's interesting! Tell me more about that.",
            "I see. What else would you like to discuss?", 
            "Thanks for sharing that with me. How can I help you further?",
            "I understand. What would you like to know more about?"
        ]
        return random.choice(responses)

def analyze_sentiment(message):
    """Simple sentiment analysis"""
    positive_words = ['happy', 'good', 'great', 'awesome', 'love', 'like', 'wonderful']
    negative_words = ['sad', 'bad', 'awful', 'hate', 'dislike', 'terrible', 'upset']
    
    message_lower = message.lower()
    positive_count = sum(1 for word in positive_words if word in message_lower)
    negative_count = sum(1 for word in negative_words if word in message_lower)
    
    if positive_count > negative_count:
        return 'positive'
    elif negative_count > positive_count:
        return 'negative'
    return 'neutral'

@app.route('/')
def home():
    return jsonify({
        "message": "STAN Chatbot Backend API",
        "version": "2.0.0",
        "endpoints": {
            "/": "API information",
            "/chat": "Chat with STAN (POST)",
            "/health": "Health check",
            "/stats": "Session statistics",
            "/data": "View session data"
        }
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        message = data['message']
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        # Generate enhanced response
        response = generate_enhanced_response(message, session_id)
        sentiment = analyze_sentiment(message)
        
        # Store conversation
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []
        
        chat_sessions[session_id].append({
            'user': message,
            'bot': response,
            'timestamp': datetime.now().isoformat(),
            'sentiment': sentiment
        })
        
        exchange_count = len(chat_sessions[session_id])
        context = f"Conversation has {exchange_count} exchanges"
        
        logger.info(f"Chat - Session: {session_id}, Message: {message}, Response: {response[:50]}...")
        
        return jsonify({
            'response': response,
            'session_id': session_id,
            'sentiment': sentiment,
            'context': context
        })
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'STAN Chatbot Backend is running',
        'active_sessions': len(chat_sessions),
        'storage': 'in-memory',
        'model': 'enhanced-pattern-based'
    })

@app.route('/stats')
def stats():
    return jsonify({
        'total_sessions': len(chat_sessions),
        'total_messages': sum(len(session) for session in chat_sessions.values()),
        'storage_type': 'in-memory'
    })

@app.route('/data')
def view_data():
    return jsonify({
        'sessions': chat_sessions,
        'user_data': user_data,
        'total_sessions': len(chat_sessions)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

