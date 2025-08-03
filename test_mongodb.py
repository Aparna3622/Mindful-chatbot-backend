"""
Test MongoDB Integration for STAN Chatbot
"""

import sys
import time
from datetime import datetime
from enhanced_features import EnhancedMemoryManager, SentimentAnalyzer, EmpathyEngine
from mongodb_config import get_config

def test_mongodb_integration():
    """Test MongoDB integration with fallback to in-memory storage"""
    print("🧪 Testing MongoDB Integration for STAN Chatbot\n")
    
    # Test 1: Initialize EnhancedMemoryManager
    print("1️⃣ Initializing EnhancedMemoryManager...")
    try:
        # Try MongoDB first, fallback to in-memory
        config = get_config('local')
        memory_manager = EnhancedMemoryManager(
            max_sessions=100,
            session_timeout_hours=24,
            mongodb_uri=config.get_connection_string()
        )
        print("   ✅ EnhancedMemoryManager initialized successfully")
    except Exception as e:
        print(f"   ❌ Error initializing EnhancedMemoryManager: {e}")
        return False
    
    # Test 2: Check storage type
    print("\n2️⃣ Checking storage type...")
    stats = memory_manager.get_session_stats()
    print(f"   📊 Storage Type: {stats['storage_type']}")
    print(f"   📊 Total Sessions: {stats['total_sessions']}")
    print(f"   📊 Active Sessions (last hour): {stats['active_sessions_last_hour']}")
    
    # Test 3: Create test sessions
    print("\n3️⃣ Testing session creation...")
    test_sessions = ['user_123', 'user_456', 'user_789']
    
    for session_id in test_sessions:
        session = memory_manager.get_session(session_id)
        print(f"   ✅ Created session: {session_id}")
    
    # Test 4: Add messages with sentiment analysis
    print("\n4️⃣ Testing message storage with sentiment analysis...")
    sentiment_analyzer = SentimentAnalyzer()
    empathy_engine = EmpathyEngine()
    
    test_conversations = [
        ("user_123", "Hello! How are you today?", "positive"),
        ("user_123", "I'm feeling great!", "positive"),
        ("user_456", "I'm having a bad day", "negative"),
        ("user_456", "Can you help me with something?", "questioning"),
        ("user_789", "What's the weather like?", "questioning")
    ]
    
    for session_id, user_message, expected_sentiment in test_conversations:
        # Analyze sentiment
        detected_sentiment = sentiment_analyzer.analyze(user_message)
        
        # Generate empathetic response
        empathy_prefix = empathy_engine.get_empathetic_prefix(detected_sentiment)
        bot_response = f"{empathy_prefix} I'm STAN, and I'm here to help!"
        
        # Store in memory manager
        memory_manager.add_message(session_id, user_message, bot_response, detected_sentiment)
        
        print(f"   💬 {session_id}: '{user_message}' → Sentiment: {detected_sentiment}")
    
    # Test 5: Retrieve context summaries
    print("\n5️⃣ Testing context retrieval...")
    for session_id in test_sessions:
        context = memory_manager.get_context_summary(session_id)
        session_data = memory_manager.get_session(session_id)
        message_count = session_data.get('message_count', 0)
        
        print(f"   📝 {session_id}: {message_count} messages")
        print(f"      Context: {context}")
    
    # Test 6: Check final statistics
    print("\n6️⃣ Final statistics...")
    final_stats = memory_manager.get_session_stats()
    print(f"   📊 Total Sessions: {final_stats['total_sessions']}")
    print(f"   📊 Active Sessions: {final_stats['active_sessions_last_hour']}")
    print(f"   📊 Storage Type: {final_stats['storage_type']}")
    
    # Test 7: Cleanup
    print("\n7️⃣ Testing cleanup...")
    memory_manager._cleanup_old_sessions()
    print("   🧹 Cleanup completed")
    
    # Close connection if MongoDB
    memory_manager.close_connection()
    
    print("\n🎉 MongoDB Integration Test Completed Successfully!")
    return True

def test_mongodb_installation():
    """Test if MongoDB server is running"""
    print("🔍 Checking MongoDB Installation...\n")
    
    try:
        from pymongo import MongoClient
        
        # Try to connect to local MongoDB
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
        
        # Test connection
        client.admin.command('ping')
        
        print("✅ MongoDB server is running locally")
        print("✅ MongoDB connection successful")
        
        # Get server info
        server_info = client.server_info()
        print(f"📋 MongoDB Version: {server_info['version']}")
        
        client.close()
        return True
        
    except Exception as e:
        print("❌ MongoDB server not running or not installed")
        print(f"   Error: {e}")
        print("\n📖 To install MongoDB:")
        print("   • Windows: Download from https://www.mongodb.com/try/download/community")
        print("   • macOS: brew install mongodb-community")
        print("   • Ubuntu: sudo apt install mongodb")
        print("\n💡 The chatbot will work with in-memory storage as fallback")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("         STAN Chatbot - MongoDB Integration Test")
    print("=" * 60)
    
    # Test MongoDB installation
    mongodb_available = test_mongodb_installation()
    
    print("\n" + "=" * 60)
    
    # Test integration (works with or without MongoDB)
    success = test_mongodb_integration()
    
    if success:
        if mongodb_available:
            print("\n🚀 Ready for production with MongoDB storage!")
        else:
            print("\n🚀 Ready for development with in-memory storage!")
            print("💡 Install MongoDB for persistent storage")
    else:
        print("\n❌ Integration test failed")
        sys.exit(1)
