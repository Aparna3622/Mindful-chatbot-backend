import os

class Config:
    """Configuration settings for the STAN chatbot"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'stan-chatbot-secret-key-2024'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Model settings
    MODEL_NAME = os.environ.get('MODEL_NAME') or 'microsoft/DialoGPT-medium'
    MAX_CHAT_HISTORY = int(os.environ.get('MAX_CHAT_HISTORY', 20))
    MAX_INPUT_LENGTH = int(os.environ.get('MAX_INPUT_LENGTH', 512))
    MAX_RESPONSE_LENGTH = int(os.environ.get('MAX_RESPONSE_LENGTH', 50))
    
    # Generation parameters
    TEMPERATURE = float(os.environ.get('TEMPERATURE', 0.7))
    DO_SAMPLE = os.environ.get('DO_SAMPLE', 'True').lower() == 'true'
    
    # Server settings
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
