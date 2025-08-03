"""
Enhanced Memory and Context Management for STAN Chatbot
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pymongo
from pymongo import MongoClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedMemoryManager:
    """Advanced memory management with MongoDB storage for better contextual awareness"""
    
    def __init__(self, max_sessions=1000, session_timeout_hours=24, mongodb_uri="mongodb://localhost:27017/"):
        # MongoDB connection
        try:
            self.client = MongoClient(mongodb_uri)
            self.db = self.client.stan_chatbot
            self.sessions_collection = self.db.sessions
            self.preferences_collection = self.db.user_preferences
            
            # Create indexes for better performance
            self.sessions_collection.create_index("session_id", unique=True)
            self.sessions_collection.create_index("last_active")
            
            logger.info("MongoDB connection established successfully")
        except Exception as e:
            logger.error(f"MongoDB connection failed: {e}")
            logger.info("Falling back to in-memory storage")
            # Fallback to in-memory storage
            self.client = None
            self.sessions = {}
            self.user_preferences = {}
        
        self.max_sessions = max_sessions
        self.session_timeout = timedelta(hours=session_timeout_hours)
        
    def get_session(self, session_id: str) -> Dict:
        """Get or create a session with enhanced tracking"""
        if self.client:  # MongoDB mode
            session = self.sessions_collection.find_one({"session_id": session_id})
            
            if not session:
                # Create new session
                session_data = {
                    'session_id': session_id,
                    'history': [],
                    'created_at': datetime.now(),
                    'last_active': datetime.now(),
                    'message_count': 0,
                    'user_info': {},
                    'conversation_topics': [],
                    'sentiment_history': []
                }
                self.sessions_collection.insert_one(session_data)
                session = session_data
            else:
                # Update last_active timestamp
                self.sessions_collection.update_one(
                    {"session_id": session_id},
                    {"$set": {"last_active": datetime.now()}}
                )
            
            # Clean up old sessions
            self._cleanup_old_sessions()
            return session
        else:  # Fallback to in-memory mode
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    'history': [],
                    'created_at': datetime.now(),
                    'last_active': datetime.now(),
                    'message_count': 0,
                    'user_info': {},
                    'conversation_topics': set(),
                    'sentiment_history': []
                }
            else:
                self.sessions[session_id]['last_active'] = datetime.now()
            
            # Clean up old sessions
            self._cleanup_old_sessions()
            return self.sessions[session_id]
    
    def add_message(self, session_id: str, user_message: str, bot_response: str, sentiment: str = None):
        """Add message with enhanced context tracking"""
        session = self.get_session(session_id)
        
        timestamp = datetime.now().isoformat()
        new_message = {
            'timestamp': timestamp,
            'user': user_message,
            'bot': bot_response,
            'sentiment': sentiment
        }
        
        if self.client:  # MongoDB mode
            # Add message to history
            self.sessions_collection.update_one(
                {"session_id": session_id},
                {
                    "$push": {"history": new_message},
                    "$inc": {"message_count": 1},
                    "$set": {"last_active": datetime.now()}
                }
            )
            
            # Extract topics and keywords
            self._extract_topics_mongodb(session_id, user_message)
            
            # Keep only recent history (last 20 messages)
            session_data = self.sessions_collection.find_one({"session_id": session_id})
            if len(session_data['history']) > 20:
                trimmed_history = session_data['history'][-20:]
                self.sessions_collection.update_one(
                    {"session_id": session_id},
                    {"$set": {"history": trimmed_history}}
                )
        else:  # Fallback to in-memory mode
            session['history'].append(new_message)
            session['message_count'] += 1
            
            # Extract topics and keywords
            self._extract_topics(session, user_message)
            
            # Keep only recent history
            if len(session['history']) > 20:
                session['history'] = session['history'][-20:]
    
    def get_context_summary(self, session_id: str) -> str:
        """Generate context summary for better responses"""
        session = self.get_session(session_id)
        
        if not session.get('history'):
            return ""
        
        # Recent conversation summary
        recent_messages = session['history'][-5:]
        
        if self.client:  # MongoDB mode
            topics = session.get('conversation_topics', [])[-3:]  # Recent topics (stored as list)
        else:  # In-memory mode
            topics = list(session.get('conversation_topics', set()))[-3:]  # Recent topics
        
        context = f"Recent topics: {', '.join(topics) if topics else 'general conversation'}"
        
        return context
    
    def _extract_topics(self, session: Dict, message: str):
        """Extract conversation topics for context (in-memory mode)"""
        # Simple keyword extraction (can be enhanced with NLP)
        topics = ['weather', 'time', 'jokes', 'help', 'technology', 'work', 'family']
        
        for topic in topics:
            if topic in message.lower():
                session['conversation_topics'].add(topic)
    
    def _extract_topics_mongodb(self, session_id: str, message: str):
        """Extract conversation topics for context (MongoDB mode)"""
        # Simple keyword extraction (can be enhanced with NLP)
        topics = ['weather', 'time', 'jokes', 'help', 'technology', 'work', 'family']
        
        new_topics = []
        for topic in topics:
            if topic in message.lower():
                new_topics.append(topic)
        
        if new_topics:
            # Add unique topics to the conversation_topics array
            self.sessions_collection.update_one(
                {"session_id": session_id},
                {"$addToSet": {"conversation_topics": {"$each": new_topics}}}
            )
    
    def _cleanup_old_sessions(self):
        """Remove expired sessions"""
        current_time = datetime.now()
        
        if self.client:  # MongoDB mode
            # Remove expired sessions
            cutoff_time = current_time - self.session_timeout
            result = self.sessions_collection.delete_many({
                "last_active": {"$lt": cutoff_time}
            })
            if result.deleted_count > 0:
                logger.info(f"Cleaned up {result.deleted_count} expired sessions")
            
            # Also cleanup if too many sessions
            total_sessions = self.sessions_collection.count_documents({})
            if total_sessions > self.max_sessions:
                # Remove oldest sessions
                sessions_to_remove = total_sessions - self.max_sessions
                oldest_sessions = self.sessions_collection.find().sort("last_active", 1).limit(sessions_to_remove)
                
                session_ids_to_remove = [session["session_id"] for session in oldest_sessions]
                if session_ids_to_remove:
                    result = self.sessions_collection.delete_many({
                        "session_id": {"$in": session_ids_to_remove}
                    })
                    logger.info(f"Cleaned up {result.deleted_count} oldest sessions to maintain max limit")
        else:  # Fallback to in-memory mode
            expired_sessions = []
            
            for session_id, session_data in self.sessions.items():
                if current_time - session_data['last_active'] > self.session_timeout:
                    expired_sessions.append(session_id)
            
            for session_id in expired_sessions:
                del self.sessions[session_id]
            
            # Also cleanup if too many sessions
            if len(self.sessions) > self.max_sessions:
                # Remove oldest sessions
                sorted_sessions = sorted(
                    self.sessions.items(),
                    key=lambda x: x[1]['last_active']
                )
                
                sessions_to_remove = len(self.sessions) - self.max_sessions
                for i in range(sessions_to_remove):
                    del self.sessions[sorted_sessions[i][0]]
    
    def get_session_stats(self) -> Dict:
        """Get statistics about stored sessions"""
        if self.client:  # MongoDB mode
            total_sessions = self.sessions_collection.count_documents({})
            active_sessions = self.sessions_collection.count_documents({
                "last_active": {"$gte": datetime.now() - timedelta(hours=1)}
            })
            return {
                "total_sessions": total_sessions,
                "active_sessions_last_hour": active_sessions,
                "storage_type": "MongoDB"
            }
        else:  # In-memory mode
            total_sessions = len(self.sessions)
            active_sessions = sum(1 for session in self.sessions.values() 
                                if datetime.now() - session['last_active'] < timedelta(hours=1))
            return {
                "total_sessions": total_sessions,
                "active_sessions_last_hour": active_sessions,
                "storage_type": "In-Memory"
            }
    
    def close_connection(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

class SentimentAnalyzer:
    """Simple sentiment analysis for empathetic responses"""
    
    def __init__(self):
        self.positive_words = ['good', 'great', 'awesome', 'amazing', 'wonderful', 'fantastic', 'love', 'like', 'happy', 'excited']
        self.negative_words = ['bad', 'terrible', 'awful', 'hate', 'sad', 'angry', 'frustrated', 'disappointed', 'upset']
        self.question_words = ['what', 'how', 'why', 'when', 'where', 'who', 'which']
    
    def analyze(self, text: str) -> str:
        """Analyze sentiment of user message"""
        text_lower = text.lower()
        
        positive_count = sum(1 for word in self.positive_words if word in text_lower)
        negative_count = sum(1 for word in self.negative_words if word in text_lower)
        has_question = any(word in text_lower for word in self.question_words)
        
        if negative_count > positive_count:
            return 'negative'
        elif positive_count > negative_count:
            return 'positive'
        elif has_question:
            return 'questioning'
        else:
            return 'neutral'

class EmpathyEngine:
    """Generate empathetic responses based on context and sentiment"""
    
    def __init__(self):
        self.empathetic_responses = {
            'negative': [
                "I'm sorry to hear that. I'm here to help if you'd like to talk about it.",
                "That sounds challenging. Would you like to share more about what's bothering you?",
                "I understand that might be frustrating. How can I assist you?"
            ],
            'positive': [
                "That's wonderful to hear! I'm glad you're feeling good.",
                "It sounds like things are going well for you! That's great.",
                "I'm happy to hear that! What's making your day so good?"
            ],
            'questioning': [
                "That's a great question! Let me help you with that.",
                "I'd be happy to help you understand that better.",
                "Interesting question! Let me think about the best way to explain that."
            ]
        }
    
    def get_empathetic_prefix(self, sentiment: str) -> str:
        """Get an empathetic prefix based on sentiment"""
        if sentiment in self.empathetic_responses:
            import random
            return random.choice(self.empathetic_responses[sentiment])
        return ""
