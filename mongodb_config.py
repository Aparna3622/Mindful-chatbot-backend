"""
MongoDB Configuration for STAN Chatbot
"""

import os
from typing import Optional

class MongoDBConfig:
    """MongoDB configuration settings"""
    
    def __init__(self):
        # Default local MongoDB settings
        self.MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.DATABASE_NAME = os.getenv('MONGODB_DATABASE', 'stan_chatbot')
        self.SESSIONS_COLLECTION = 'sessions'
        self.PREFERENCES_COLLECTION = 'user_preferences'
        
        # Connection settings
        self.CONNECTION_TIMEOUT = 5000  # 5 seconds
        self.SERVER_SELECTION_TIMEOUT = 5000  # 5 seconds
        
    def get_connection_string(self) -> str:
        """Get the MongoDB connection string"""
        return self.MONGODB_URI
    
    def get_connection_options(self) -> dict:
        """Get MongoDB connection options"""
        return {
            'connectTimeoutMS': self.CONNECTION_TIMEOUT,
            'serverSelectionTimeoutMS': self.SERVER_SELECTION_TIMEOUT,
        }

# Production/Cloud MongoDB configurations
class MongoDBCloudConfig(MongoDBConfig):
    """MongoDB Atlas (Cloud) configuration"""
    
    def __init__(self, username: str, password: str, cluster: str):
        super().__init__()
        self.MONGODB_URI = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority"
        
# Docker MongoDB configuration
class MongoDBDockerConfig(MongoDBConfig):
    """MongoDB Docker configuration"""
    
    def __init__(self, host: str = 'localhost', port: int = 27017):
        super().__init__()
        self.MONGODB_URI = f"mongodb://{host}:{port}/"

# Example configurations for different environments
MONGODB_CONFIGS = {
    'local': MongoDBConfig(),
    'docker': MongoDBDockerConfig(),
    # 'cloud': MongoDBCloudConfig('username', 'password', 'cluster-name.mongodb.net')
}

def get_config(environment: str = 'local') -> MongoDBConfig:
    """Get MongoDB configuration for specified environment"""
    return MONGODB_CONFIGS.get(environment, MongoDBConfig())
