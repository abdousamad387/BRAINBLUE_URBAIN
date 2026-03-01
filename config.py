"""
BRAINBLUE URBAIN - Configuration centralisée
"""

import os
from datetime import timedelta

class Config:
    """Configuration de base"""
    
    # Application
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://brainblue_user:secure_password_2026@localhost:5432/brainblue_urbain'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': int(os.getenv('CONNECTION_POOL_SIZE', 10)),
        'pool_recycle': int(os.getenv('CONNECTION_POOL_RECYCLE', 3600)),
        'pool_pre_ping': True,
    }
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 24)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 30)))
    
    # Redis
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5000')
    
    # File Upload
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 52428800))  # 50MB
    UPLOAD_FOLDER = os.getenv('UPLOAD_DIR', './uploads')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', './logs/brainblue.log')
    
    # ML Models
    MODEL_PATH = os.getenv('MODEL_PATH', './ml_models')
    
    # Cache
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 300))
    CACHE_REDIS_URL = REDIS_URL
    
    # Sentry
    SENTRY_DSN = os.getenv('SENTRY_DSN', None)
    
    # Email Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    
    # Debug & Testing
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    TESTING = os.getenv('TESTING', 'False').lower() == 'true'


class DevelopmentConfig(Config):
    """Configuration développement"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Configuration production"""
    DEBUG = False
    TESTING = False
    # En production, vérifier que SECRET_KEY est défini
    assert os.getenv('SECRET_KEY'), 'SECRET_KEY doit être défini en production'
    assert os.getenv('JWT_SECRET_KEY'), 'JWT_SECRET_KEY doit être défini en production'


class TestingConfig(Config):
    """Configuration testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)


# Sélectionner config basée sur environnement
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Obtenir la config appropriée"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
