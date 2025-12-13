"""
Configuration file for Password Generator Application
Centralizes all configurable values for easy management
"""

import os

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    TESTING = False
    
    # Server Configuration
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5001))
    
    # Rate Limiting Configuration
    RATELIMIT_ENABLED = os.environ.get('RATELIMIT_ENABLED', 'True').lower() == 'true'
    RATELIMIT_DEFAULT = os.environ.get('RATELIMIT_DEFAULT', '100 per minute')
    RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI', 'memory://')
    
    # Password Generation Constraints
    PASSWORD_MIN_LENGTH = int(os.environ.get('PASSWORD_MIN_LENGTH', 4))
    PASSWORD_MAX_LENGTH = int(os.environ.get('PASSWORD_MAX_LENGTH', 128))
    
    # Passphrase Generation Constraints
    PASSPHRASE_MIN_WORDS = int(os.environ.get('PASSPHRASE_MIN_WORDS', 2))
    PASSPHRASE_MAX_WORDS = int(os.environ.get('PASSPHRASE_MAX_WORDS', 20))
    PASSPHRASE_API_MIN_WORDS = int(os.environ.get('PASSPHRASE_API_MIN_WORDS', 3))
    PASSPHRASE_API_MAX_WORDS = int(os.environ.get('PASSPHRASE_API_MAX_WORDS', 6))
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False
    # In production, these should be set via environment variables
    RATELIMIT_ENABLED = True


class TestingConfig(Config):
    """Testing environment configuration"""
    DEBUG = False
    TESTING = True
    RATELIMIT_ENABLED = False  # Disable rate limiting for tests


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """
    Get configuration based on environment.
    
    Args:
        env: Environment name ('development', 'production', 'testing')
             If None, uses FLASK_ENV environment variable or 'default'
    
    Returns:
        Configuration class
    """
    if env is None:
        env = os.environ.get('FLASK_ENV', 'default')
    return config.get(env, config['default'])