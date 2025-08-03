from flask import Flask, render_template, request, jsonify
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
import logging
from flask_cors import CORS
import json
import uuid
import re
from datetime import datetime
import os
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Enable CORS
CORS(app, origins=[
    "https://mindful-chatbot.vercel.app",
    "https://*.vercel.app",
    "http://localhost:3000"
], methods=["GET", "POST", "OPTIONS"])

class ChatBot:
    def __init__(self):
        """Initialize the chatbot with a pre-trained model"""
        self.model = None
        self.tokenizer = None
        self.backup_model = None
        
        # Try to load primary model
        try:
            # Use a lightweight conversational model
            model_name = "microsoft/DialoGPT-medium"
            logger.info(f"Loading primary model: {model_name}")
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            
            # Set pad token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            logger.info("Primary model loaded successfully!")
            
        except Exception as e:
            logger.error(f"Error loading primary model: {e}")
            logger.info("Falling back to rule-based responses...")
            
        # Try backup model if primary fails
        if self.model is None:
            try:
                logger.info("Attempting to load backup model...")
                # Try a smaller, more reliable model
                from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
                self.backup_tokenizer = BlenderbotTokenizer.from_pretrained("facebook/blenderbot_small-90M")
                self.backup_model = BlenderbotForConditionalGeneration.from_pretrained("facebook/blenderbot_small-90M")
                logger.info("Backup model loaded successfully!")
            except Exception as e:
                logger.error(f"Error loading backup model: {e}")
                logger.info("Using rule-based responses only.")
    
    def generate_response(self, user_input, chat_history=None):
        """Generate a response to user input"""
        try:
            # Try primary model first
            if self.model is not None and self.tokenizer is not None:
                return self._generate_with_primary_model(user_input, chat_history)
            
            # Try backup model
            elif hasattr(self, 'backup_model') and self.backup_model is not None:
                return self._generate_with_backup_model(user_input)
            
            # Fall back to rule-based responses
            else:
                return self._fallback_response(user_input)
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._fallback_response(user_input)
    
    def _generate_with_primary_model(self, user_input, chat_history=None):
        """Generate response using DialoGPT"""
        # Prepare input with chat history
        if chat_history:
            # Combine chat history with current input
            input_text = " ".join(chat_history[-5:]) + f" {user_input}"
        else:
            input_text = user_input
        
        # Encode input
        input_ids = self.tokenizer.encode(
            input_text, 
            return_tensors='pt', 
            max_length=512, 
            truncation=True
        )
        
        # Generate response
        with torch.no_grad():
            output = self.model.generate(
                input_ids,
                max_length=input_ids.shape[1] + 50,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                attention_mask=torch.ones_like(input_ids)
            )
        
        # Decode response
        response = self.tokenizer.decode(
            output[0][input_ids.shape[1]:], 
            skip_special_tokens=True
        ).strip()
        
        return response if response else self._fallback_response(user_input)
    
    def _generate_with_backup_model(self, user_input):
        """Generate response using Blenderbot backup model"""
        inputs = self.backup_tokenizer(user_input, return_tensors="pt")
        
        with torch.no_grad():
            outputs = self.backup_model.generate(
                **inputs,
                max_length=100,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True
            )
        
        response = self.backup_tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response if response else self._fallback_response(user_input)
    
    def _fallback_response(self, user_input):
        """Provide fallback responses when the model fails"""
        user_input_lower = user_input.lower()
        
        # Greetings
        if any(greeting in user_input_lower for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            return "Hello! I'm STAN, your AI assistant. How can I help you today?"
        
        # Casual greetings
        elif any(phrase in user_input_lower for phrase in ["what's up", 'whats up', 'wassup', 'sup', "how's it going"]):
            return "Not much, just here ready to chat with you! What's going on with you?"
        
        # Questions about the bot itself
        elif any(phrase in user_input_lower for phrase in ['what are you', 'who are you', 'what is chatbot', 'about you']):
            return "I'm STAN, an AI chatbot designed to help answer questions and have conversations. I'm here to assist you with various topics!"
        
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
        
        # What questions
        elif 'what' in user_input_lower and any(word in user_input_lower for word in ['doing', 'up to', 'happening']):
            return "I'm here chatting with you and ready to help! I can answer questions, provide information, or just have a friendly conversation. What would you like to talk about?"
        
        # Capabilities questions
        elif any(phrase in user_input_lower for phrase in ['what can you do', 'your capabilities', 'help me with']):
            return "I can help you with many things! I can answer questions, provide information, help with problem-solving, have conversations, and assist with various topics. What specific help do you need?"
        
        # Name questions (specific patterns first)
        elif ('name' in user_input_lower and any(word in user_input_lower for word in ['your', 'what', 'called'])) or "what's your name" in user_input_lower:
            return "My name is STAN! It's nice to meet you. What's your name? Or if you prefer, I'm happy to just chat without names too!"
        
        # Age questions (specific patterns first)
        elif any(word in user_input_lower for word in ['age', 'old', 'born', 'created']) or 'how old' in user_input_lower:
            return "I'm a relatively new AI assistant! I don't age like humans do, but I'm constantly learning from our conversations. How long have you been interested in chatbots?"
        
        # Time questions (specific patterns first)
        elif any(word in user_input_lower for word in ['time', 'clock', 'hour', 'minute']) or 'what time' in user_input_lower:
            import datetime
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            return f"The current time is approximately {current_time}. How can I help you with your day? 🕐"
        
        # Weather questions (specific patterns first)
        elif 'weather' in user_input_lower:
            return "I don't have access to real-time weather data, but I'd suggest checking a weather app or website like weather.com for current conditions in your area! ☀️🌧️"
        
        # Jokes and humor (specific patterns first)
        elif any(word in user_input_lower for word in ['joke', 'funny', 'humor', 'laugh']):
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything! 😄",
                "Why did the programmer quit his job? Because he didn't get arrays! 💻",
                "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
                "What do you call a bear with no teeth? A gummy bear! 🐻",
                "Why don't eggs tell jokes? They'd crack each other up! 🥚",
                "What's the best thing about Switzerland? I don't know, but the flag is a big plus! 🇨🇭"
            ]
            import random
            return random.choice(jokes)
        
        # Compliments (specific patterns first)
        elif any(word in user_input_lower for word in ['smart', 'intelligent', 'good', 'great', 'awesome', 'amazing']):
            return "Thank you so much! That's very kind of you to say. I really enjoy our conversation and I'm here whenever you need help! 😊"
        
        # General questions (moved after specific patterns)
        elif any(word in user_input_lower for word in ['what', 'how', 'why', 'when', 'where', 'which', 'who']):
            return "That's an interesting question! I'd be happy to help you with that. Could you provide a bit more context or detail so I can give you a better answer?"
        
        # Thank you
        elif any(word in user_input_lower for word in ['thank', 'thanks', 'appreciate']):
            return "You're very welcome! I'm glad I could help. Is there anything else you'd like to know or discuss?"
        
        # Goodbye
        elif any(word in user_input_lower for word in ['bye', 'goodbye', 'see you', 'talk later', 'farewell']):
            return "Goodbye! It was great chatting with you. Feel free to come back anytime if you need help. Have a wonderful day!"
        
        # Help requests
        elif any(word in user_input_lower for word in ['help', 'assist', 'support']):
            return "I'm here to help! You can ask me questions about various topics, request information, or just have a conversation. What would you like assistance with?"
        
        # Default response
        else:
            responses = [
                "That's fascinating! Tell me more about what you're thinking. 💭",
                "I'd love to learn more about that topic. Could you share some details? 🤔",
                "That sounds really interesting! What aspects of it would you like to explore? 🌟",
                "I'm curious to know more! Could you help me understand what you mean? 💡",
                "That's a great topic to discuss! What specifically interests you about it? 🗣️",
                "I find that intriguing! Can you tell me what prompted that question? ❓",
                "That's worth exploring! What would you like to know more about? 🔍"
            ]
            import random
            return random.choice(responses)

# Initialize chatbot and enhanced features
chatbot = ChatBot()

# Import enhanced features with MongoDB support
from enhanced_features import EnhancedMemoryManager, SentimentAnalyzer, EmpathyEngine
from mongodb_config import get_config

# Initialize enhanced memory manager with MongoDB
config = get_config('local')
memory_manager = EnhancedMemoryManager(
    max_sessions=1000,
    session_timeout_hours=24,
    mongodb_uri=config.get_connection_string()
)

# Initialize sentiment analysis and empathy engine
sentiment_analyzer = SentimentAnalyzer()
empathy_engine = EmpathyEngine()

# Store chat history (kept for backward compatibility, but using MongoDB now)
chat_sessions = {}

@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages with enhanced MongoDB storage and sentiment analysis"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Analyze sentiment
        sentiment = sentiment_analyzer.analyze(user_message)
        
        # Get session data from MongoDB
        session_data = memory_manager.get_session(session_id)
        chat_history = session_data.get('history', [])
        
        # Convert history to format expected by chatbot
        formatted_history = []
        for msg in chat_history[-10:]:  # Last 10 messages for context
            formatted_history.append(f"User: {msg['user']}")
            formatted_history.append(f"Bot: {msg['bot']}")
        
        # Generate empathetic prefix based on sentiment
        empathy_prefix = empathy_engine.get_empathetic_prefix(sentiment)
        
        # Generate response with context
        context_summary = memory_manager.get_context_summary(session_id)
        bot_response = chatbot.generate_response(user_message, formatted_history)
        
        # Add empathetic prefix if appropriate
        if empathy_prefix and sentiment in ['negative', 'positive']:
            bot_response = f"{empathy_prefix} {bot_response}"
        
        # Store message in MongoDB with enhanced tracking
        memory_manager.add_message(session_id, user_message, bot_response, sentiment)
        
        # Backward compatibility - also update in-memory sessions
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []
        
        chat_history = chat_sessions[session_id]
        chat_history.append(f"User: {user_message}")
        chat_history.append(f"Bot: {bot_response}")
        
        # Keep only last 10 exchanges to manage memory
        if len(chat_history) > 20:
            chat_history = chat_history[-20:]
        
        chat_sessions[session_id] = chat_history
        
        return jsonify({
            'response': bot_response,
            'session_id': session_id, 
            'sentiment': sentiment,
            'context': context_summary
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health():
    """Health check endpoint with MongoDB status"""
    stats = memory_manager.get_session_stats()
    return jsonify({
        'status': 'healthy', 
        'model_loaded': chatbot.model is not None,
        'storage_type': stats['storage_type'],
        'total_sessions': stats['total_sessions'],
        'active_sessions': stats['active_sessions_last_hour']
    })

@app.route('/stats')
def get_stats():
    """Get detailed session statistics"""
    try:
        stats = memory_manager.get_session_stats()
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': 'Failed to get statistics'}), 500

@app.route('/data')
def view_data():
    return jsonify({
        'sessions': chat_sessions,
        'user_data': user_data,
        'total_sessions': len(chat_sessions)
    })

def generate_enhanced_response(user_input, session_id):
    """Enhanced response generation with your improved patterns"""
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
    
    # Casual greetings - THIS WAS MISSING!
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
        "version": "2.0.0",  # Updated version
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
