"""
Enhanced Authentication System for Zen_Align
Includes OAuth, 2FA, email verification, and security features
"""

import os
import secrets
import string
from datetime import datetime, timedelta
from functools import wraps
from typing import Dict, Optional, Tuple

import bcrypt
import jwt
from flask import current_app, request, jsonify, session
from flask_mail import Mail, Message
from twilio.rest import Client
import redis
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import facebook

class AuthManager:
    def __init__(self, app=None, db_manager=None, mail=None):
        self.app = app
        self.db = db_manager
        self.mail = mail
        self.redis_client = None
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize authentication manager with Flask app"""
        self.app = app
        
        # Initialize Redis for OTP storage
        try:
            self.redis_client = redis.from_url(app.config['REDIS_URL'])
        except:
            self.redis_client = None
        
        # Initialize Twilio for SMS
        if app.config.get('TWILIO_ACCOUNT_SID'):
            self.twilio_client = Client(
                app.config['TWILIO_ACCOUNT_SID'],
                app.config['TWILIO_AUTH_TOKEN']
            )
        else:
            self.twilio_client = None
    
    def generate_otp(self, length: int = 6) -> str:
        """Generate random OTP"""
        return ''.join(secrets.choice(string.digits) for _ in range(length))
    
    def store_otp(self, key: str, otp: str, expiry_minutes: int = 10):
        """Store OTP in Redis with expiry"""
        if self.redis_client:
            self.redis_client.setex(key, expiry_minutes * 60, otp)
    
    def verify_otp(self, key: str, provided_otp: str) -> bool:
        """Verify OTP against stored value"""
        if not self.redis_client:
            return False
        
        stored_otp = self.redis_client.get(key)
        if stored_otp and stored_otp.decode() == provided_otp:
            self.redis_client.delete(key)  # Delete after successful verification
            return True
        return False
    
    def send_email_otp(self, email: str, purpose: str = 'verification') -> bool:
        """Send OTP via email"""
        if not self.mail:
            return False
        
        otp = self.generate_otp()
        key = f"email_otp:{email}:{purpose}"
        
        try:
            msg = Message(
                subject=f'Zen_Align - {purpose.title()} Code',
                recipients=[email],
                body=f'Your verification code is: {otp}\n\nThis code will expire in 10 minutes.'
            )
            self.mail.send(msg)
            self.store_otp(key, otp)
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to send email OTP: {e}")
            return False
    
    def send_sms_otp(self, phone: str, purpose: str = 'verification') -> bool:
        """Send OTP via SMS"""
        if not self.twilio_client:
            return False
        
        otp = self.generate_otp()
        key = f"sms_otp:{phone}:{purpose}"
        
        try:
            message = self.twilio_client.messages.create(
                body=f'Your Zen_Align verification code is: {otp}',
                from_=current_app.config['TWILIO_PHONE_NUMBER'],
                to=phone
            )
            self.store_otp(key, otp)
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to send SMS OTP: {e}")
            return False
    
    def verify_email_otp(self, email: str, otp: str, purpose: str = 'verification') -> bool:
        """Verify email OTP"""
        key = f"email_otp:{email}:{purpose}"
        return self.verify_otp(key, otp)
    
    def verify_sms_otp(self, phone: str, otp: str, purpose: str = 'verification') -> bool:
        """Verify SMS OTP"""
        key = f"sms_otp:{phone}:{purpose}"
        return self.verify_otp(key, otp)
    
    def hash_password(self, password: str) -> bytes:
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    def verify_password(self, password: str, hashed: bytes) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    
    def generate_jwt_token(self, user_id: str, token_type: str = 'access') -> str:
        """Generate JWT token"""
        now = datetime.utcnow()
        
        if token_type == 'access':
            exp = now + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
        else:  # refresh
            exp = now + current_app.config['JWT_REFRESH_TOKEN_EXPIRES']
        
        payload = {
            'user_id': user_id,
            'type': token_type,
            'iat': now,
            'exp': exp
        }
        
        return jwt.encode(
            payload,
            current_app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )
    
    def verify_jwt_token(self, token: str) -> Optional[Dict]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=['HS256']
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def google_oauth_verify(self, token: str) -> Optional[Dict]:
        """Verify Google OAuth token"""
        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                current_app.config['GOOGLE_CLIENT_ID']
            )
            
            return {
                'email': idinfo['email'],
                'name': idinfo['name'],
                'picture': idinfo.get('picture'),
                'provider': 'google'
            }
        except ValueError:
            return None
    
    def facebook_oauth_verify(self, token: str) -> Optional[Dict]:
        """Verify Facebook OAuth token"""
        try:
            graph = facebook.GraphAPI(access_token=token)
            profile = graph.get_object('me', fields='name,email,picture')
            
            return {
                'email': profile.get('email'),
                'name': profile['name'],
                'picture': profile.get('picture', {}).get('data', {}).get('url'),
                'provider': 'facebook'
            }
        except facebook.GraphAPIError:
            return None
    
    def setup_2fa(self, user_id: str) -> str:
        """Setup 2FA for user and return secret"""
        import pyotp
        
        secret = pyotp.random_base32()
        key = f"2fa_secret:{user_id}"
        
        # Store secret temporarily (user needs to verify setup)
        if self.redis_client:
            self.redis_client.setex(key, 300, secret)  # 5 minutes
        
        return secret
    
    def verify_2fa_setup(self, user_id: str, token: str) -> bool:
        """Verify 2FA setup token"""
        import pyotp
        
        key = f"2fa_secret:{user_id}"
        if not self.redis_client:
            return False
        
        secret = self.redis_client.get(key)
        if not secret:
            return False
        
        totp = pyotp.TOTP(secret.decode())
        if totp.verify(token):
            # Save secret to user profile
            self.db.users.update_one(
                {'_id': user_id},
                {'$set': {
                    'twoFactorEnabled': True,
                    'twoFactorSecret': secret.decode()
                }}
            )
            self.redis_client.delete(key)
            return True
        
        return False
    
    def verify_2fa_token(self, user_id: str, token: str) -> bool:
        """Verify 2FA token for login"""
        import pyotp
        
        user = self.db.users.find_one({'_id': user_id})
        if not user or not user.get('twoFactorEnabled'):
            return False
        
        secret = user.get('twoFactorSecret')
        if not secret:
            return False
        
        totp = pyotp.TOTP(secret)
        return totp.verify(token)
    
    def generate_password_reset_token(self, email: str) -> str:
        """Generate password reset token"""
        token = secrets.token_urlsafe(32)
        key = f"password_reset:{email}"
        
        if self.redis_client:
            self.redis_client.setex(key, 3600, token)  # 1 hour expiry
        
        return token
    
    def verify_password_reset_token(self, email: str, token: str) -> bool:
        """Verify password reset token"""
        key = f"password_reset:{email}"
        if not self.redis_client:
            return False
        
        stored_token = self.redis_client.get(key)
        if stored_token and stored_token.decode() == token:
            self.redis_client.delete(key)
            return True
        
        return False
    
    def log_security_event(self, user_id: str, event_type: str, details: Dict):
        """Log security events"""
        self.db.security_logs.insert_one({
            'userId': user_id,
            'eventType': event_type,
            'details': details,
            'timestamp': datetime.now(),
            'ipAddress': request.remote_addr if request else None,
            'userAgent': request.headers.get('User-Agent') if request else None
        })

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check session-based auth
        if 'user_id' in session:
            return f(*args, **kwargs)
        
        # Check JWT token
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            auth_manager = current_app.auth_manager
            payload = auth_manager.verify_jwt_token(token)
            
            if payload and payload.get('type') == 'access':
                request.current_user_id = payload['user_id']
                return f(*args, **kwargs)
        
        return jsonify({'error': 'Authentication required'}), 401
    
    return decorated_function

def require_verified_email(f):
    """Decorator to require verified email"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id') or getattr(request, 'current_user_id', None)
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        user = current_app.db_manager.users.find_one({'_id': user_id})
        if not user or not user.get('emailVerified'):
            return jsonify({'error': 'Email verification required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

def rate_limit_by_ip(max_requests: int = 10, window_minutes: int = 1):
    """Rate limiting decorator by IP address"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_app.config.get('REDIS_URL'):
                return f(*args, **kwargs)  # Skip if Redis not available
            
            redis_client = redis.from_url(current_app.config['REDIS_URL'])
            ip = request.remote_addr
            key = f"rate_limit:{ip}:{f.__name__}"
            
            current_requests = redis_client.get(key)
            if current_requests and int(current_requests) >= max_requests:
                return jsonify({'error': 'Rate limit exceeded'}), 429
            
            # Increment counter
            pipe = redis_client.pipeline()
            pipe.incr(key)
            pipe.expire(key, window_minutes * 60)
            pipe.execute()
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator