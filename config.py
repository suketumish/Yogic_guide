import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Core Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database Configuration
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/yogic_guide')
    
    # Session Configuration
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Email Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', MAIL_USERNAME)
    
    # SMS Configuration (Twilio)
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
    
    # OAuth Configuration
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    FACEBOOK_APP_ID = os.getenv('FACEBOOK_APP_ID')
    FACEBOOK_APP_SECRET = os.getenv('FACEBOOK_APP_SECRET')
    
    # Redis Configuration (for caching and sessions)
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # File Upload Configuration
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm'}
    
    # API Rate Limiting
    RATELIMIT_STORAGE_URL = REDIS_URL
    RATELIMIT_DEFAULT = "100 per hour"
    
    # MediaPipe Configuration
    MEDIAPIPE_MODEL_COMPLEXITY = int(os.getenv('MEDIAPIPE_MODEL_COMPLEXITY', 1))
    MEDIAPIPE_MIN_DETECTION_CONFIDENCE = float(os.getenv('MEDIAPIPE_MIN_DETECTION_CONFIDENCE', 0.5))
    MEDIAPIPE_MIN_TRACKING_CONFIDENCE = float(os.getenv('MEDIAPIPE_MIN_TRACKING_CONFIDENCE', 0.5))
    
    # AI/ML Configuration
    POSE_ACCURACY_THRESHOLD = float(os.getenv('POSE_ACCURACY_THRESHOLD', 85.0))
    ANGLE_TOLERANCE = float(os.getenv('ANGLE_TOLERANCE', 15.0))
    
    # Health Integration
    APPLE_HEALTH_ENABLED = os.getenv('APPLE_HEALTH_ENABLED', 'False').lower() == 'true'
    GOOGLE_FIT_ENABLED = os.getenv('GOOGLE_FIT_ENABLED', 'False').lower() == 'true'
    FITBIT_CLIENT_ID = os.getenv('FITBIT_CLIENT_ID')
    FITBIT_CLIENT_SECRET = os.getenv('FITBIT_CLIENT_SECRET')
    
    # Notification Configuration
    PUSH_NOTIFICATIONS_ENABLED = os.getenv('PUSH_NOTIFICATIONS_ENABLED', 'True').lower() == 'true'
    FCM_SERVER_KEY = os.getenv('FCM_SERVER_KEY')
    
    # Analytics Configuration
    GOOGLE_ANALYTICS_ID = os.getenv('GOOGLE_ANALYTICS_ID')
    MIXPANEL_TOKEN = os.getenv('MIXPANEL_TOKEN')
    
    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-pro')  # Options: gemini-pro, gemini-pro-vision
    GEMINI_ENABLED = os.getenv('GEMINI_ENABLED', 'True').lower() == 'true'
    
    # Development/Production Settings
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    TESTING = os.getenv('TESTING', 'False').lower() == 'true'
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'yogic_guide.log')
    
    # Celery Configuration (for background tasks)
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', REDIS_URL)
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', REDIS_URL)
    
    # Security Configuration
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    
    # Content Security Policy
    CSP_DEFAULT_SRC = "'self'"
    CSP_SCRIPT_SRC = "'self' 'unsafe-inline' https://cdn.tailwindcss.com https://cdn.jsdelivr.net"
    CSP_STYLE_SRC = "'self' 'unsafe-inline' https://cdn.tailwindcss.com"
    CSP_IMG_SRC = "'self' data: https:"
    CSP_MEDIA_SRC = "'self'"
    
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    
class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    MONGO_URI = 'mongodb://localhost:27017/yogic_guide_test'
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
