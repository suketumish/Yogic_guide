import os
import logging
from datetime import datetime, timedelta
from bson import ObjectId

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_mail import Mail
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Optional imports with fallbacks
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

try:
    from config import config
except ImportError:
    # Fallback configuration
    class Config:
        SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
        MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/yogic_guide')
        REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        DEBUG = True
    
    config = {'development': Config, 'default': Config}

try:
    from models import DatabaseManager, UserModel, SessionModel, PoseModel, AchievementModel, SocialModel
except ImportError:
    # We'll create simplified models if the enhanced ones aren't available
    DatabaseManager = None

try:
    from auth import AuthManager, require_auth, require_verified_email, rate_limit_by_ip
except ImportError:
    # Fallback auth functions
    def require_auth(f):
        from functools import wraps
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    
    def require_verified_email(f):
        return require_auth(f)
    
    def rate_limit_by_ip(max_requests=10, window_minutes=1):
        def decorator(f):
            return f
        return decorator
    
    AuthManager = None

def create_app(config_name=None):
    """Application factory pattern with fallback support"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Load configuration
    if config_name in config:
        app.config.from_object(config[config_name])
    else:
        # Fallback configuration
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
        app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/yogic_guide')
        app.config['DEBUG'] = True
    
    # Initialize extensions
    mail = Mail(app)
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    # Initialize rate limiter (optional)
    try:
        limiter = Limiter(
            key_func=get_remote_address,
            default_limits=["200 per day", "50 per hour"]
        )
        limiter.init_app(app)
    except Exception as e:
        print(f"Warning: Rate limiter not initialized: {e}")
        limiter = None
    
    # Initialize database
    if DatabaseManager:
        db_manager = DatabaseManager(app.config['MONGO_URI'])
        
        # Initialize authentication
        if AuthManager:
            auth_manager = AuthManager(app, db_manager, mail)
        else:
            auth_manager = None
        
        # Initialize models
        user_model = UserModel(db_manager) if UserModel else None
        session_model = SessionModel(db_manager) if SessionModel else None
        pose_model = PoseModel(db_manager) if PoseModel else None
        achievement_model = AchievementModel(db_manager) if AchievementModel else None
        social_model = SocialModel(db_manager) if SocialModel else None
        
        # Create default achievements
        if achievement_model:
            try:
                achievement_model.create_default_achievements()
            except Exception as e:
                print(f"Warning: Could not create achievements: {e}")
    else:
        # Fallback to basic MongoDB connection
        from pymongo import MongoClient
        client = MongoClient(app.config['MONGO_URI'])
        db_manager = client.yogic_guide
        auth_manager = None
        user_model = None
        session_model = None
        pose_model = None
        achievement_model = None
        social_model = None
    
    # Store managers in app context
    app.db_manager = db_manager
    app.auth_manager = auth_manager
    app.socketio = socketio
    
    # Configure logging
    if not app.config.get('DEBUG', True):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s: %(message)s'
        )
    
    return app, socketio, db_manager, user_model, session_model, pose_model, achievement_model, social_model

# Create app instance
app, socketio, db_manager, user_model, session_model, pose_model, achievement_model, social_model = create_app()

# Import bcrypt for basic password hashing
import bcrypt

# ============================================================================
# BASIC ROUTES (Fallback functionality)
# ============================================================================

@app.route('/')
def index():
    """Landing page or redirect to dashboard if authenticated"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('landing.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Basic user registration"""
    if request.method == 'POST':
        try:
            name = request.form.get('name', '')
            email = request.form.get('email', '').lower().strip()
            password = request.form.get('password', '')
            age = request.form.get('age', 25)
            gender = request.form.get('gender', '')
            experience = request.form.get('experience', 'Beginner')
            
            if not email or not password:
                return render_template('register.html', error='Email and password are required')
            
            # Check if user exists
            if hasattr(db_manager, 'users'):
                existing_user = db_manager.users.find_one({'email': email})
            else:
                existing_user = db_manager.users.find_one({'email': email})
            
            if existing_user:
                return render_template('register.html', error='Email already registered')
            
            # Hash password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Create user document
            user_doc = {
                'name': name,
                'email': email,
                'password': hashed_password,
                'age': int(age) if age else 25,
                'gender': gender,
                'experience_level': experience,
                'created_at': datetime.now(),
                'emailVerified': True  # Skip verification for basic setup
            }
            
            # Insert user
            if hasattr(db_manager, 'users'):
                user_id = db_manager.users.insert_one(user_doc).inserted_id
            else:
                user_id = db_manager.users.insert_one(user_doc).inserted_id
            
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            print(f"Registration error: {e}")
            return render_template('register.html', error='Registration failed. Please try again.')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Basic login functionality"""
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            return render_template('login.html', error='Email and password are required')
        
        try:
            # Find user
            if hasattr(db_manager, 'users'):
                user = db_manager.users.find_one({'email': email})
            else:
                user = db_manager.users.find_one({'email': email})
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
                session['user_id'] = str(user['_id'])
                session['user_name'] = user.get('name', 'User')
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error='Invalid email or password')
                
        except Exception as e:
            print(f"Login error: {e}")
            return render_template('login.html', error='Login failed. Please try again.')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Basic logout"""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    """Basic dashboard"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Basic progress data
    progress = {
        'total_sessions': 0,
        'streak_days': 0,
        'total_minutes': 0
    }
    
    return render_template('dashboard.html', progress=progress)

@app.route('/profile')
def profile():
    """Basic profile page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        user_id = ObjectId(session['user_id'])
        if hasattr(db_manager, 'users'):
            user = db_manager.users.find_one({'_id': user_id})
        else:
            user = db_manager.users.find_one({'_id': user_id})
        
        sessions = []  # Empty sessions for now
        
        return render_template('profile.html', user=user, sessions=sessions)
    except Exception as e:
        print(f"Profile error: {e}")
        return redirect(url_for('dashboard'))

@app.route('/module/<module_type>')
def module_session(module_type):
    """Basic module session"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    modules = {
        'stretching': 'Full Body Stretching',
        'breathing': 'Breathing Exercises',
        'surya-namaskar': 'Surya Namaskar'
    }
    
    if module_type not in modules:
        return redirect(url_for('dashboard'))
    
    if module_type == 'breathing' and not request.args.get('exercise'):
        return render_template('breathing.html')
    
    return render_template('session.html', 
                         module_type=module_type, 
                         module_name=modules[module_type])

@app.route('/session-complete')
def session_complete():
    """Basic session completion page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('session-complete.html')

# Basic API endpoints
@app.route('/api/pose/validate', methods=['POST'])
def validate_pose():
    """Basic pose validation"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.json
        landmarks = data.get('landmarks', [])
        
        if not landmarks:
            return jsonify({'error': 'Missing landmarks'}), 400
        
        # Basic validation - just return success for now
        return jsonify({
            'valid': True,
            'accuracy': 85.0,
            'feedback': []
        })
        
    except Exception as e:
        return jsonify({'error': 'Validation failed'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Basic health check
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.route('/')
def index():
    """Landing page or redirect to dashboard if authenticated"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('landing.html')

@app.route('/home')
def landing():
    """Public landing page"""
    return render_template('landing.html')

@app.route('/register', methods=['GET', 'POST'])
@rate_limit_by_ip(max_requests=5, window_minutes=15)
def register():
    """Enhanced user registration with validation and verification"""
    if request.method == 'POST':
        try:
            # Extract form data
            user_data = {
                'firstName': request.form.get('firstName', ''),
                'lastName': request.form.get('lastName', ''),
                'email': request.form.get('email', '').lower().strip(),
                'password': request.form.get('password', ''),
                'phone': request.form.get('phone', ''),
                'dateOfBirth': request.form.get('dateOfBirth'),
                'gender': request.form.get('gender', ''),
                'height': float(request.form.get('height', 0) or 0),
                'weight': float(request.form.get('weight', 0) or 0),
                'experienceLevel': request.form.get('experienceLevel', 'Beginner'),
                'healthConditions': request.form.getlist('healthConditions'),
                'city': request.form.get('city', ''),
                'country': request.form.get('country', ''),
                'language': request.form.get('language', 'English')
            }
            
            # Validation
            if not user_data['email'] or not user_data['password']:
                return render_template('register.html', error='Email and password are required')
            
            if len(user_data['password']) < 6:
                return render_template('register.html', error='Password must be at least 6 characters')
            
            # Check if user already exists
            if db_manager.users.find_one({'email': user_data['email']}):
                return render_template('register.html', error='Email already registered')
            
            # Create user
            user_id = user_model.create_user(user_data)
            
            # Send verification email
            if app.auth_manager.send_email_otp(user_data['email'], 'registration'):
                flash('Registration successful! Please check your email for verification code.', 'success')
                session['pending_user_id'] = str(user_id)
                session['pending_email'] = user_data['email']
                return redirect(url_for('verify_email'))
            else:
                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('login'))
                
        except Exception as e:
            app.logger.error(f"Registration error: {e}")
            return render_template('register.html', error='Registration failed. Please try again.')
    
    return render_template('register.html')

@app.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    """Email verification page"""
    if 'pending_email' not in session:
        return redirect(url_for('register'))
    
    if request.method == 'POST':
        otp = request.form.get('otp', '').strip()
        email = session['pending_email']
        
        if app.auth_manager.verify_email_otp(email, otp, 'registration'):
            # Mark email as verified
            user_id = ObjectId(session['pending_user_id'])
            db_manager.users.update_one(
                {'_id': user_id},
                {'$set': {'emailVerified': True}}
            )
            
            # Clear pending session data
            session.pop('pending_user_id', None)
            session.pop('pending_email', None)
            
            flash('Email verified successfully! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid or expired verification code.', 'error')
    
    return render_template('verify_email.html', email=session['pending_email'])

@app.route('/resend-verification', methods=['POST'])
@rate_limit_by_ip(max_requests=3, window_minutes=5)
def resend_verification():
    """Resend email verification code"""
    if 'pending_email' not in session:
        return jsonify({'error': 'No pending verification'}), 400
    
    email = session['pending_email']
    if app.auth_manager.send_email_otp(email, 'registration'):
        return jsonify({'success': True, 'message': 'Verification code sent'})
    else:
        return jsonify({'error': 'Failed to send verification code'}), 500

@app.route('/login', methods=['GET', 'POST'])
@rate_limit_by_ip(max_requests=10, window_minutes=15)
def login():
    """Enhanced login with 2FA support"""
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password', '')
        remember_me = request.form.get('remember_me') == 'on'
        
        if not email or not password:
            return render_template('login.html', error='Email and password are required')
        
        # Authenticate user
        user = user_model.authenticate_user(email, password)
        
        if user:
            # Check if email is verified
            if not user.get('emailVerified', False):
                flash('Please verify your email before logging in.', 'warning')
                return render_template('login.html', error='Email verification required')
            
            # Check if 2FA is enabled
            if user.get('twoFactorEnabled', False):
                session['pending_2fa_user_id'] = str(user['_id'])
                return redirect(url_for('verify_2fa'))
            
            # Complete login
            session['user_id'] = str(user['_id'])
            session['user_name'] = user.get('profile', {}).get('firstName', user.get('name', 'User'))
            
            if remember_me:
                session.permanent = True
            
            # Log security event
            app.auth_manager.log_security_event(
                str(user['_id']), 
                'login_success', 
                {'method': 'password'}
            )
            
            return redirect(url_for('dashboard'))
        else:
            # Log failed attempt
            app.auth_manager.log_security_event(
                email, 
                'login_failed', 
                {'reason': 'invalid_credentials'}
            )
            return render_template('login.html', error='Invalid email or password')
    
    return render_template('login.html')

@app.route('/verify-2fa', methods=['GET', 'POST'])
def verify_2fa():
    """Two-factor authentication verification"""
    if 'pending_2fa_user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        token = request.form.get('token', '').strip()
        user_id = ObjectId(session['pending_2fa_user_id'])
        
        if app.auth_manager.verify_2fa_token(user_id, token):
            # Complete login
            user = db_manager.users.find_one({'_id': user_id})
            session['user_id'] = str(user_id)
            session['user_name'] = user.get('profile', {}).get('firstName', 'User')
            session.pop('pending_2fa_user_id', None)
            
            app.auth_manager.log_security_event(
                str(user_id), 
                'login_success', 
                {'method': '2fa'}
            )
            
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid 2FA code. Please try again.', 'error')
    
    return render_template('verify_2fa.html')

@app.route('/oauth/google', methods=['POST'])
def google_oauth():
    """Google OAuth login"""
    token = request.json.get('token')
    if not token:
        return jsonify({'error': 'Token required'}), 400
    
    user_info = app.auth_manager.google_oauth_verify(token)
    if not user_info:
        return jsonify({'error': 'Invalid token'}), 400
    
    # Find or create user
    user = db_manager.users.find_one({'email': user_info['email']})
    
    if not user:
        # Create new user from OAuth
        user_data = {
            'firstName': user_info['name'].split()[0] if user_info['name'] else '',
            'lastName': ' '.join(user_info['name'].split()[1:]) if user_info['name'] else '',
            'email': user_info['email'],
            'avatar': user_info.get('picture', ''),
            'emailVerified': True,  # OAuth emails are pre-verified
            'experienceLevel': 'Beginner'
        }
        user_id = user_model.create_user(user_data)
    else:
        user_id = user['_id']
    
    # Generate JWT tokens
    access_token = app.auth_manager.generate_jwt_token(str(user_id), 'access')
    refresh_token = app.auth_manager.generate_jwt_token(str(user_id), 'refresh')
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user_id': str(user_id)
    })

@app.route('/forgot-password', methods=['GET', 'POST'])
@rate_limit_by_ip(max_requests=3, window_minutes=15)
def forgot_password():
    """Password reset request"""
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        
        user = db_manager.users.find_one({'email': email})
        if user:
            # Generate reset token
            reset_token = app.auth_manager.generate_password_reset_token(email)
            
            # Send reset email (in production, send actual email)
            if app.auth_manager.send_email_otp(email, 'password_reset'):
                flash('Password reset instructions sent to your email.', 'info')
            else:
                flash('Failed to send reset email. Please try again.', 'error')
        else:
            # Don't reveal if email exists
            flash('If that email exists, you will receive reset instructions.', 'info')
        
        return redirect(url_for('login'))
    
    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Password reset with token"""
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        new_password = request.form.get('password', '')
        
        if len(new_password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return render_template('reset_password.html', token=token)
        
        if app.auth_manager.verify_password_reset_token(email, token):
            # Update password
            hashed_password = app.auth_manager.hash_password(new_password)
            db_manager.users.update_one(
                {'email': email},
                {'$set': {'password': hashed_password}}
            )
            
            flash('Password reset successfully. You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid or expired reset token.', 'error')
    
    return render_template('reset_password.html', token=token)

@app.route('/logout')
def logout():
    """Enhanced logout with security logging"""
    user_id = session.get('user_id')
    if user_id:
        app.auth_manager.log_security_event(
            user_id, 
            'logout', 
            {'method': 'manual'}
        )
    
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

# ============================================================================
# DASHBOARD & PROFILE ROUTES
# ============================================================================

@app.route('/dashboard')
@require_auth
def dashboard():
    """Enhanced dashboard with personalized recommendations"""
    user_id = ObjectId(session['user_id'])
    
    # Get user data
    user = db_manager.users.find_one({'_id': user_id})
    if not user:
        return redirect(url_for('logout'))
    
    # Get user progress
    progress = db_manager.user_progress.find_one({'userId': user_id}) or {}
    
    # Get recent sessions
    recent_sessions = list(db_manager.sessions.find(
        {'userId': user_id}
    ).sort('startTime', -1).limit(5))
    
    # Get today's stats
    today = datetime.now().date()
    today_sessions = list(db_manager.sessions.find({
        'userId': user_id,
        'startTime': {
            '$gte': datetime.combine(today, datetime.min.time()),
            '$lt': datetime.combine(today + timedelta(days=1), datetime.min.time())
        }
    }))
    
    today_stats = {
        'sessions': len(today_sessions),
        'minutes': sum(s.get('duration', 0) for s in today_sessions) // 60,
        'calories': sum(s.get('sessionStats', {}).get('caloriesBurned', 0) for s in today_sessions),
        'accuracy': sum(s.get('sessionStats', {}).get('totalAccuracy', 0) for s in today_sessions) / len(today_sessions) if today_sessions else 0
    }
    
    # Get weekly progress
    week_ago = datetime.now() - timedelta(days=7)
    weekly_sessions = list(db_manager.sessions.find({
        'userId': user_id,
        'startTime': {'$gte': week_ago}
    }))
    
    # Get achievements
    user_achievements = user.get('social', {}).get('achievements', [])
    achievements = list(db_manager.achievements.find({
        'code': {'$in': user_achievements}
    }))
    
    # Get recommendations (simplified AI)
    recommendations = get_user_recommendations(user_id, user, recent_sessions)
    
    # Get activity feed
    activity_feed = social_model.get_activity_feed(user_id, limit=10)
    
    return render_template('dashboard.html', 
                         user=user,
                         progress=progress,
                         today_stats=today_stats,
                         recent_sessions=recent_sessions,
                         weekly_sessions=weekly_sessions,
                         achievements=achievements,
                         recommendations=recommendations,
                         activity_feed=activity_feed)

@app.route('/profile')
@require_auth
def profile():
    """Enhanced user profile with detailed statistics"""
    user_id = ObjectId(session['user_id'])
    
    # Get user data
    user = db_manager.users.find_one({'_id': user_id})
    if not user:
        return redirect(url_for('logout'))
    
    # Get session history
    user_sessions = list(db_manager.sessions.find(
        {'userId': user_id}
    ).sort('startTime', -1).limit(20))
    
    # Calculate detailed statistics
    stats = calculate_user_statistics(user_id)
    
    # Get achievements
    user_achievements = user.get('social', {}).get('achievements', [])
    achievements = list(db_manager.achievements.find({
        'code': {'$in': user_achievements}
    }))
    
    # Get social stats
    social_stats = {
        'friends': len(user.get('social', {}).get('friends', [])),
        'followers': len(user.get('social', {}).get('followers', [])),
        'following': len(user.get('social', {}).get('following', []))
    }
    
    return render_template('profile.html', 
                         user=user,
                         sessions=user_sessions,
                         stats=stats,
                         achievements=achievements,
                         social_stats=social_stats)

@app.route('/profile/edit', methods=['GET', 'POST'])
@require_auth
def edit_profile():
    """Edit user profile"""
    user_id = ObjectId(session['user_id'])
    user = db_manager.users.find_one({'_id': user_id})
    
    if request.method == 'POST':
        update_data = {}
        
        # Profile updates
        if request.form.get('firstName'):
            update_data['profile.firstName'] = request.form.get('firstName')
        if request.form.get('lastName'):
            update_data['profile.lastName'] = request.form.get('lastName')
        if request.form.get('bio'):
            update_data['profile.bio'] = request.form.get('bio')
        if request.form.get('city'):
            update_data['profile.location.city'] = request.form.get('city')
        if request.form.get('country'):
            update_data['profile.location.country'] = request.form.get('country')
        
        # Physical updates
        if request.form.get('height'):
            height = float(request.form.get('height'))
            update_data['physical.height'] = height
            
            # Recalculate BMI if weight exists
            weight = user.get('physical', {}).get('weight', 0)
            if weight > 0:
                update_data['physical.bmi'] = round(weight / ((height/100) ** 2), 2)
        
        if request.form.get('weight'):
            weight = float(request.form.get('weight'))
            update_data['physical.weight'] = weight
            
            # Add to weight history
            db_manager.users.update_one(
                {'_id': user_id},
                {'$push': {'physical.weightHistory': {
                    'date': datetime.now(),
                    'weight': weight
                }}}
            )
            
            # Recalculate BMI
            height = user.get('physical', {}).get('height', 0)
            if height > 0:
                update_data['physical.bmi'] = round(weight / ((height/100) ** 2), 2)
        
        # Preferences
        if request.form.get('experienceLevel'):
            update_data['preferences.experienceLevel'] = request.form.get('experienceLevel')
        if request.form.get('language'):
            update_data['preferences.language'] = request.form.get('language')
        if request.form.get('theme'):
            update_data['preferences.theme'] = request.form.get('theme')
        
        # Update timestamp
        update_data['updatedAt'] = datetime.now()
        
        # Apply updates
        if update_data:
            db_manager.users.update_one({'_id': user_id}, {'$set': update_data})
            flash('Profile updated successfully!', 'success')
        
        return redirect(url_for('profile'))
    
    return render_template('edit_profile.html', user=user)

def get_user_recommendations(user_id: ObjectId, user: dict, recent_sessions: list) -> dict:
    """Generate personalized recommendations for user"""
    recommendations = {
        'next_session': None,
        'challenge': None,
        'pose_focus': None,
        'time_suggestion': None
    }
    
    # Analyze user's practice patterns
    experience_level = user.get('preferences', {}).get('experienceLevel', 'Beginner')
    
    # Recommend next session based on recent activity
    if not recent_sessions:
        recommendations['next_session'] = {
            'type': 'stretching',
            'name': 'Beginner Full Body Stretch',
            'duration': 15,
            'reason': 'Perfect for getting started!'
        }
    else:
        last_session = recent_sessions[0]
        last_module = last_session.get('module', 'stretching')
        
        # Rotate modules for variety
        module_rotation = {
            'stretching': 'breathing',
            'breathing': 'surya-namaskar',
            'surya-namaskar': 'stretching'
        }
        
        next_module = module_rotation.get(last_module, 'stretching')
        recommendations['next_session'] = {
            'type': next_module,
            'name': f'{next_module.replace("-", " ").title()}',
            'duration': 20 if experience_level != 'Beginner' else 15,
            'reason': 'Continue your balanced practice'
        }
    
    # Suggest optimal practice time based on user's history
    if recent_sessions:
        # Find most common practice hour
        practice_hours = [s['startTime'].hour for s in recent_sessions if 'startTime' in s]
        if practice_hours:
            most_common_hour = max(set(practice_hours), key=practice_hours.count)
            recommendations['time_suggestion'] = f"{most_common_hour:02d}:00"
    
    return recommendations

def calculate_user_statistics(user_id: ObjectId) -> dict:
    """Calculate comprehensive user statistics"""
    # Get all user sessions
    sessions = list(db_manager.sessions.find({'userId': user_id}))
    
    if not sessions:
        return {
            'total_sessions': 0,
            'total_minutes': 0,
            'average_accuracy': 0,
            'favorite_module': 'None',
            'best_streak': 0,
            'total_calories': 0,
            'improvement_rate': 0
        }
    
    # Calculate basic stats
    total_sessions = len(sessions)
    total_minutes = sum(s.get('duration', 0) for s in sessions) // 60
    total_calories = sum(s.get('sessionStats', {}).get('caloriesBurned', 0) for s in sessions)
    
    # Calculate average accuracy
    accuracies = [s.get('sessionStats', {}).get('totalAccuracy', 0) for s in sessions if s.get('sessionStats', {}).get('totalAccuracy', 0) > 0]
    average_accuracy = sum(accuracies) / len(accuracies) if accuracies else 0
    
    # Find favorite module
    modules = [s.get('module', '') for s in sessions]
    favorite_module = max(set(modules), key=modules.count) if modules else 'None'
    
    # Calculate improvement rate (accuracy trend)
    if len(accuracies) >= 2:
        recent_accuracy = sum(accuracies[-5:]) / min(5, len(accuracies[-5:]))
        early_accuracy = sum(accuracies[:5]) / min(5, len(accuracies[:5]))
        improvement_rate = ((recent_accuracy - early_accuracy) / early_accuracy * 100) if early_accuracy > 0 else 0
    else:
        improvement_rate = 0
    
    return {
        'total_sessions': total_sessions,
        'total_minutes': total_minutes,
        'average_accuracy': round(average_accuracy, 1),
        'favorite_module': favorite_module.replace('-', ' ').title(),
        'total_calories': int(total_calories),
        'improvement_rate': round(improvement_rate, 1),
        'sessions_this_week': len([s for s in sessions if s.get('startTime', datetime.min) > datetime.now() - timedelta(days=7)]),
        'sessions_this_month': len([s for s in sessions if s.get('startTime', datetime.min) > datetime.now() - timedelta(days=30)])
    }

# ============================================================================
# MODULE & SESSION ROUTES
# ============================================================================

@app.route('/module/<module_type>')
@require_auth
def module_session(module_type):
    """Enhanced module session with personalization"""
    user_id = ObjectId(session['user_id'])
    user = db_manager.users.find_one({'_id': user_id})
    
    modules = {
        'stretching': 'Full Body Stretching',
        'breathing': 'Breathing Exercises',
        'surya-namaskar': 'Surya Namaskar',
        'custom': 'Custom Routine',
        'challenge': 'Daily Challenge'
    }
    
    if module_type not in modules:
        return redirect(url_for('dashboard'))
    
    # Check if breathing exercise selection is needed
    if module_type == 'breathing' and not request.args.get('exercise'):
        return render_template('breathing.html')
    
    # Get module-specific poses
    poses = pose_model.get_poses_by_module(module_type)
    
    # Adjust difficulty based on user experience
    experience_level = user.get('preferences', {}).get('experienceLevel', 'Beginner')
    filtered_poses = [p for p in poses if p.get('difficulty', 'beginner').lower() == experience_level.lower()]
    
    if not filtered_poses:
        filtered_poses = poses  # Fallback to all poses
    
    # Get user's previous performance for this module
    recent_performance = db_manager.sessions.find_one({
        'userId': user_id,
        'module': module_type
    }, sort=[('startTime', -1)])
    
    session_data = {
        'module_type': module_type,
        'module_name': modules[module_type],
        'poses': filtered_poses,
        'user_experience': experience_level,
        'previous_accuracy': recent_performance.get('sessionStats', {}).get('totalAccuracy', 0) if recent_performance else 0,
        'exercise_type': request.args.get('exercise', 'default')
    }
    
    return render_template('session.html', **session_data)

@app.route('/custom-routine')
@require_auth
def custom_routine():
    """Custom routine builder"""
    user_id = ObjectId(session['user_id'])
    
    # Get user's saved routines
    user_routines = list(db_manager.custom_routines.find({'userId': user_id}))
    
    # Get all available poses
    all_poses = list(db_manager.poses.find({}))
    
    return render_template('custom_routine.html', 
                         routines=user_routines,
                         poses=all_poses)

@app.route('/challenges')
@require_auth
def challenges():
    """View available challenges"""
    user_id = ObjectId(session['user_id'])
    
    # Get active challenges
    active_challenges = list(db_manager.challenges.find({
        'endDate': {'$gte': datetime.now()}
    }).sort('startDate', -1))
    
    # Get user's challenge participation
    user_challenges = list(db_manager.challenges.find({
        'participants': user_id
    }))
    
    return render_template('challenges.html',
                         active_challenges=active_challenges,
                         user_challenges=user_challenges)

# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

@app.route('/session/start', methods=['POST'])
@require_auth
def start_session():
    """Start a new practice session with enhanced tracking"""
    try:
        user_id = ObjectId(session['user_id'])
        data = request.json
        
        module_type = data.get('module_type')
        module_name = data.get('module_name', module_type)
        difficulty = data.get('difficulty', 'medium')
        
        # Create session
        session_id = session_model.create_session(user_id, module_type, module_name)
        
        # Log session start
        app.logger.info(f"Session started: {session_id} for user {user_id}")
        
        return jsonify({
            'session_id': str(session_id),
            'start_time': datetime.now().isoformat(),
            'success': True
        })
        
    except Exception as e:
        app.logger.error(f"Error starting session: {e}")
        return jsonify({'error': 'Failed to start session'}), 500

@app.route('/session/<session_id>/update', methods=['POST'])
@require_auth
def update_session(session_id):
    """Update session progress in real-time"""
    try:
        data = request.json
        
        update_data = {}
        if 'poses' in data:
            update_data['poses'] = data['poses']
        if 'current_pose' in data:
            update_data['currentPose'] = data['current_pose']
        if 'accuracy' in data:
            update_data['sessionStats.totalAccuracy'] = data['accuracy']
        
        db_manager.sessions.update_one(
            {'_id': ObjectId(session_id)},
            {'$set': update_data}
        )
        
        return jsonify({'success': True})
        
    except Exception as e:
        app.logger.error(f"Error updating session: {e}")
        return jsonify({'error': 'Failed to update session'}), 500

@app.route('/session/<session_id>/complete', methods=['POST'])
@require_auth
def complete_session(session_id):
    """Complete session with comprehensive statistics"""
    try:
        user_id = ObjectId(session['user_id'])
        data = request.json
        
        # Calculate calories burned (simplified formula)
        duration_minutes = data.get('duration', 0) // 60
        user = db_manager.users.find_one({'_id': user_id})
        weight = user.get('physical', {}).get('weight', 70)  # Default 70kg
        
        # Yoga burns approximately 3-6 calories per minute depending on intensity
        intensity_multiplier = {
            'breathing': 2,
            'stretching': 4,
            'surya-namaskar': 6
        }
        
        module_type = data.get('module_type', 'stretching')
        calories = duration_minutes * intensity_multiplier.get(module_type, 4) * (weight / 70)
        
        completion_data = {
            'duration': data.get('duration', 0),
            'accuracy': data.get('accuracy', 0),
            'poses': data.get('poses', []),
            'calories': int(calories),
            'rating': data.get('rating', 0),
            'difficulty': data.get('difficulty', 'medium')
        }
        
        # Complete the session
        session_model.complete_session(ObjectId(session_id), completion_data)
        
        # Check for achievements
        check_session_achievements(user_id, completion_data)
        
        # Create social activity
        create_social_activity(user_id, 'session_complete', {
            'module': module_type,
            'duration': duration_minutes,
            'accuracy': completion_data['accuracy']
        })
        
        return jsonify({
            'success': True,
            'calories_burned': int(calories),
            'xp_gained': calculate_xp_gained(completion_data),
            'achievements_unlocked': []  # Will be populated by achievement check
        })
        
    except Exception as e:
        app.logger.error(f"Error completing session: {e}")
        return jsonify({'error': 'Failed to complete session'}), 500

@app.route('/session-complete')
@require_auth
def session_complete():
    """Session completion page with statistics"""
    return render_template('session-complete.html')

def check_session_achievements(user_id: ObjectId, session_data: dict):
    """Check and award achievements based on session performance"""
    user = db_manager.users.find_one({'_id': user_id})
    current_achievements = user.get('social', {}).get('achievements', [])
    
    # Check accuracy achievements
    accuracy = session_data.get('accuracy', 0)
    if accuracy >= 95 and 'accuracy_95' not in current_achievements:
        award_achievement(user_id, 'accuracy_95')
    
    # Check session count achievements
    total_sessions = user.get('stats', {}).get('totalSessions', 0)
    if total_sessions == 1 and 'first_session' not in current_achievements:
        award_achievement(user_id, 'first_session')

def award_achievement(user_id: ObjectId, achievement_code: str):
    """Award achievement to user"""
    achievement = db_manager.achievements.find_one({'code': achievement_code})
    if not achievement:
        return
    
    # Add to user's achievements
    db_manager.users.update_one(
        {'_id': user_id},
        {
            '$addToSet': {'social.achievements': achievement_code},
            '$inc': {'stats.xp': achievement.get('points', 0)}
        }
    )
    
    # Create social activity
    create_social_activity(user_id, 'achievement_unlock', {
        'achievement': achievement_code,
        'name': achievement.get('name', ''),
        'points': achievement.get('points', 0)
    })

def create_social_activity(user_id: ObjectId, activity_type: str, data: dict):
    """Create social activity for feed"""
    db_manager.social_activities.insert_one({
        'userId': user_id,
        'type': activity_type,
        'data': data,
        'createdAt': datetime.now()
    })

def calculate_xp_gained(session_data: dict) -> int:
    """Calculate XP gained from session"""
    base_xp = (session_data.get('duration', 0) // 60) * 2  # 2 XP per minute
    accuracy_bonus = int(session_data.get('accuracy', 0) / 10) * 5  # Bonus for accuracy
    return base_xp + accuracy_bonus

# ============================================================================
# API ROUTES
# ============================================================================

@app.route('/api/pose/validate', methods=['POST'])
@require_auth
def validate_pose():
    """
    Enhanced pose validation with MediaPipe and advanced feedback
    """
    try:
        data = request.json
        landmarks = data.get('landmarks', [])
        pose_name = data.get('pose_name', '')
        target_angles = data.get('target_angles', {})
        tolerance = data.get('tolerance', app.config['ANGLE_TOLERANCE'])
        
        if not landmarks:
            return jsonify({'error': 'Missing landmarks'}), 400
        
        # Get pose data from database if pose_name provided
        if pose_name and not target_angles:
            pose_data = pose_model.get_pose_by_name(pose_name)
            if pose_data:
                target_angles = pose_data.get('measurements', {})
        
        if not target_angles:
            return jsonify({'error': 'Missing target angles'}), 400
        
        # Calculate current angles from landmarks
        current_angles = calculate_pose_angles(landmarks)
        
        # Enhanced validation with body symmetry check
        validation_result = validate_angles_enhanced(current_angles, target_angles, tolerance)
        
        # Add pose-specific feedback
        validation_result['pose_feedback'] = generate_pose_feedback(pose_name, current_angles, landmarks)
        
        return jsonify(validation_result)
        
    except Exception as e:
        app.logger.error(f"Pose validation error: {e}")
        return jsonify({'error': 'Validation failed'}), 500

@app.route('/api/poses/<module_type>')
@require_auth
def get_poses(module_type):
    """Get poses for specific module with user customization"""
    user_id = ObjectId(session['user_id'])
    user = db_manager.users.find_one({'_id': user_id})
    
    # Get base poses
    poses = pose_model.get_poses_by_module(module_type)
    
    # Filter by user experience level
    experience_level = user.get('preferences', {}).get('experienceLevel', 'Beginner')
    
    # Add user-specific modifications
    for pose in poses:
        pose['user_modifications'] = get_pose_modifications(pose, user)
        pose['previous_performance'] = get_user_pose_performance(user_id, pose.get('name', ''))
    
    return jsonify(poses)

@app.route('/api/poses/search', methods=['GET'])
@require_auth
def search_poses():
    """Search poses with filters"""
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    difficulty = request.args.get('difficulty', '')
    
    filters = {}
    if category:
        filters['category'] = category
    if difficulty:
        filters['difficulty'] = difficulty.lower()
    
    poses = pose_model.search_poses(query, filters)
    return jsonify(poses)

@app.route('/api/user/stats')
@require_auth
def get_user_stats():
    """Get comprehensive user statistics"""
    user_id = ObjectId(session['user_id'])
    stats = calculate_user_statistics(user_id)
    
    # Add weekly/monthly breakdowns
    stats['weekly_breakdown'] = get_weekly_breakdown(user_id)
    stats['monthly_breakdown'] = get_monthly_breakdown(user_id)
    
    return jsonify(stats)

@app.route('/api/user/progress')
@require_auth
def get_user_progress():
    """Get user progress data for charts"""
    user_id = ObjectId(session['user_id'])
    
    # Get sessions from last 30 days
    thirty_days_ago = datetime.now() - timedelta(days=30)
    sessions = list(db_manager.sessions.find({
        'userId': user_id,
        'startTime': {'$gte': thirty_days_ago}
    }).sort('startTime', 1))
    
    # Group by day
    daily_data = {}
    for session in sessions:
        date_key = session['startTime'].date().isoformat()
        if date_key not in daily_data:
            daily_data[date_key] = {
                'date': date_key,
                'sessions': 0,
                'minutes': 0,
                'accuracy': []
            }
        
        daily_data[date_key]['sessions'] += 1
        daily_data[date_key]['minutes'] += session.get('duration', 0) // 60
        if session.get('sessionStats', {}).get('totalAccuracy', 0) > 0:
            daily_data[date_key]['accuracy'].append(session['sessionStats']['totalAccuracy'])
    
    # Calculate average accuracy per day
    for day_data in daily_data.values():
        if day_data['accuracy']:
            day_data['avg_accuracy'] = sum(day_data['accuracy']) / len(day_data['accuracy'])
        else:
            day_data['avg_accuracy'] = 0
        del day_data['accuracy']  # Remove raw accuracy data
    
    return jsonify(list(daily_data.values()))

@app.route('/api/recommendations')
@require_auth
def get_recommendations():
    """Get AI-powered recommendations"""
    user_id = ObjectId(session['user_id'])
    user = db_manager.users.find_one({'_id': user_id})
    
    # Get recent sessions for analysis
    recent_sessions = list(db_manager.sessions.find(
        {'userId': user_id}
    ).sort('startTime', -1).limit(10))
    
    recommendations = get_user_recommendations(user_id, user, recent_sessions)
    
    # Add more detailed recommendations
    recommendations['pose_recommendations'] = get_pose_recommendations(user_id, recent_sessions)
    recommendations['schedule_recommendation'] = get_schedule_recommendation(recent_sessions)
    
    return jsonify(recommendations)

@app.route('/api/social/activity-feed')
@require_auth
def get_activity_feed():
    """Get social activity feed"""
    user_id = ObjectId(session['user_id'])
    limit = int(request.args.get('limit', 20))
    
    activities = social_model.get_activity_feed(user_id, limit)
    
    # Enrich activities with user data
    for activity in activities:
        if 'userId' in activity:
            user = db_manager.users.find_one({'_id': activity['userId']})
            if user:
                activity['user'] = {
                    'name': user.get('profile', {}).get('firstName', 'User'),
                    'avatar': user.get('profile', {}).get('avatar', '')
                }
    
    return jsonify(activities)

# Enhanced helper functions

def calculate_pose_angles(landmarks):
    """Enhanced pose angle calculation with more joints"""
    import math
    
    def calc_angle(a, b, c):
        """Calculate angle between three points"""
        if not all([a, b, c]):
            return None
            
        ba = {'x': a['x'] - b['x'], 'y': a['y'] - b['y'], 'z': a.get('z', 0) - b.get('z', 0)}
        bc = {'x': c['x'] - b['x'], 'y': c['y'] - b['y'], 'z': c.get('z', 0) - b.get('z', 0)}
        
        dot = ba['x'] * bc['x'] + ba['y'] * bc['y'] + ba['z'] * bc['z']
        mag_ba = math.sqrt(ba['x']**2 + ba['y']**2 + ba['z']**2)
        mag_bc = math.sqrt(bc['x']**2 + bc['y']**2 + bc['z']**2)
        
        if mag_ba == 0 or mag_bc == 0:
            return None
        
        cos_angle = max(-1, min(1, dot / (mag_ba * mag_bc)))
        angle = math.acos(cos_angle) * (180 / math.pi)
        return angle
    
    def calc_body_symmetry(left_landmarks, right_landmarks):
        """Calculate body symmetry ratio"""
        if not left_landmarks or not right_landmarks:
            return 1.0
        
        # Calculate distances from center line
        center_x = (left_landmarks[0]['x'] + right_landmarks[0]['x']) / 2
        left_dist = abs(left_landmarks[0]['x'] - center_x)
        right_dist = abs(right_landmarks[0]['x'] - center_x)
        
        if left_dist == 0 or right_dist == 0:
            return 1.0
        
        return min(left_dist, right_dist) / max(left_dist, right_dist)
    
    angles = {}
    
    try:
        # Basic joint angles
        angles['leftElbow'] = calc_angle(landmarks[11], landmarks[13], landmarks[15])
        angles['rightElbow'] = calc_angle(landmarks[12], landmarks[14], landmarks[16])
        angles['leftKnee'] = calc_angle(landmarks[23], landmarks[25], landmarks[27])
        angles['rightKnee'] = calc_angle(landmarks[24], landmarks[26], landmarks[28])
        angles['leftShoulder'] = calc_angle(landmarks[13], landmarks[11], landmarks[23])
        angles['rightShoulder'] = calc_angle(landmarks[14], landmarks[12], landmarks[24])
        angles['leftHip'] = calc_angle(landmarks[11], landmarks[23], landmarks[25])
        angles['rightHip'] = calc_angle(landmarks[12], landmarks[24], landmarks[26])
        
        # Additional angles for better pose detection
        angles['leftAnkle'] = calc_angle(landmarks[25], landmarks[27], landmarks[31])
        angles['rightAnkle'] = calc_angle(landmarks[26], landmarks[28], landmarks[32])
        angles['neck'] = calc_angle(landmarks[11], landmarks[0], landmarks[12])
        
        # Body symmetry
        left_shoulder = landmarks[11] if len(landmarks) > 11 else None
        right_shoulder = landmarks[12] if len(landmarks) > 12 else None
        angles['bodySymmetry'] = calc_body_symmetry([left_shoulder], [right_shoulder]) if left_shoulder and right_shoulder else 1.0
        
    except (IndexError, KeyError, TypeError) as e:
        app.logger.warning(f"Error calculating angles: {e}")
    
    return angles

def validate_angles_enhanced(current_angles, target_angles, tolerance):
    """Enhanced angle validation with weighted importance"""
    correct_count = 0
    total_count = 0
    feedback = []
    weighted_score = 0
    total_weight = 0
    
    # Joint importance weights
    joint_weights = {
        'leftShoulder': 1.5, 'rightShoulder': 1.5,
        'leftElbow': 1.2, 'rightElbow': 1.2,
        'leftHip': 1.3, 'rightHip': 1.3,
        'leftKnee': 1.1, 'rightKnee': 1.1,
        'bodySymmetry': 2.0,
        'neck': 1.0
    }
    
    for joint, target in target_angles.items():
        if joint not in current_angles or current_angles[joint] is None:
            continue
        
        total_count += 1
        current = current_angles[joint]
        weight = joint_weights.get(joint, 1.0)
        total_weight += weight
        
        # Special handling for symmetry
        if joint == 'bodySymmetry':
            diff = abs(1.0 - current)  # Symmetry should be close to 1.0
            is_correct = diff <= 0.1  # 10% tolerance for symmetry
        else:
            diff = abs(current - target)
            is_correct = diff <= tolerance
        
        if is_correct:
            correct_count += 1
            weighted_score += weight
        else:
            # Generate feedback
            if joint == 'bodySymmetry':
                feedback.append({
                    'joint': joint,
                    'message': 'Balance your body weight evenly',
                    'priority': 'high' if diff > 0.2 else 'medium'
                })
            else:
                adjustment = 'decrease' if current > target else 'increase'
                priority = 'high' if diff > tolerance * 2 else 'medium'
                
                feedback.append({
                    'joint': joint,
                    'current': round(current, 1),
                    'target': target,
                    'diff': round(diff, 1),
                    'adjustment': adjustment,
                    'priority': priority
                })
    
    # Calculate scores
    basic_accuracy = round((correct_count / total_count * 100) if total_count > 0 else 0, 1)
    weighted_accuracy = round((weighted_score / total_weight * 100) if total_weight > 0 else 0, 1)
    
    # Sort feedback by priority
    feedback.sort(key=lambda x: {'high': 0, 'medium': 1, 'low': 2}.get(x.get('priority', 'low'), 2))
    
    return {
        'valid': weighted_accuracy >= app.config['POSE_ACCURACY_THRESHOLD'],
        'accuracy': weighted_accuracy,
        'basic_accuracy': basic_accuracy,
        'correct_angles': correct_count,
        'total_angles': total_count,
        'feedback': feedback[:3],  # Top 3 most important adjustments
        'overall_assessment': get_overall_assessment(weighted_accuracy)
    }

def generate_pose_feedback(pose_name, current_angles, landmarks):
    """Generate pose-specific feedback and tips"""
    feedback = {
        'tips': [],
        'warnings': [],
        'encouragement': ''
    }
    
    # Get pose-specific data
    pose_data = pose_model.get_pose_by_name(pose_name)
    if not pose_data:
        return feedback
    
    # Add pose-specific tips
    if pose_data.get('technique', {}).get('alignment'):
        feedback['tips'] = pose_data['technique']['alignment'][:2]  # Top 2 tips
    
    # Add warnings for contraindications
    if pose_data.get('contraindications'):
        feedback['warnings'] = pose_data['contraindications'][:1]  # Most important warning
    
    # Generate encouragement based on performance
    accuracy = sum(1 for angle in current_angles.values() if angle is not None) / len(current_angles) * 100
    
    if accuracy >= 90:
        feedback['encouragement'] = "Excellent form! You're mastering this pose."
    elif accuracy >= 75:
        feedback['encouragement'] = "Great job! Small adjustments will perfect your form."
    elif accuracy >= 60:
        feedback['encouragement'] = "Good effort! Focus on the key alignment points."
    else:
        feedback['encouragement'] = "Keep practicing! Every session improves your form."
    
    return feedback

def get_overall_assessment(accuracy):
    """Get overall pose assessment"""
    if accuracy >= 95:
        return "Perfect"
    elif accuracy >= 85:
        return "Excellent"
    elif accuracy >= 75:
        return "Good"
    elif accuracy >= 60:
        return "Fair"
    else:
        return "Needs Improvement"

def get_pose_modifications(pose, user):
    """Get pose modifications based on user profile"""
    modifications = []
    
    experience_level = user.get('preferences', {}).get('experienceLevel', 'Beginner')
    health_conditions = user.get('physical', {}).get('healthConditions', [])
    injuries = user.get('physical', {}).get('injuries', [])
    
    # Experience-based modifications
    if experience_level == 'Beginner' and pose.get('difficulty') != 'beginner':
        modifications.append({
            'type': 'difficulty',
            'description': 'Use props or hold for shorter duration'
        })
    
    # Health condition modifications
    for condition in health_conditions:
        if 'back' in condition.lower() and 'spine' in pose.get('category', ''):
            modifications.append({
                'type': 'health',
                'description': 'Avoid deep backbends, use gentle variations'
            })
    
    return modifications

def get_user_pose_performance(user_id, pose_name):
    """Get user's historical performance for specific pose"""
    # This would analyze past sessions for this specific pose
    # Simplified implementation
    recent_sessions = list(db_manager.sessions.find({
        'userId': user_id,
        'poses.name': pose_name
    }).sort('startTime', -1).limit(5))
    
    if not recent_sessions:
        return None
    
    accuracies = []
    for session in recent_sessions:
        for pose in session.get('poses', []):
            if pose.get('name') == pose_name:
                accuracies.append(pose.get('accuracy', 0))
    
    if accuracies:
        return {
            'average_accuracy': sum(accuracies) / len(accuracies),
            'best_accuracy': max(accuracies),
            'attempts': len(accuracies),
            'improvement_trend': 'improving' if len(accuracies) > 1 and accuracies[-1] > accuracies[0] else 'stable'
        }
    
    return None

def get_weekly_breakdown(user_id):
    """Get weekly practice breakdown"""
    week_ago = datetime.now() - timedelta(days=7)
    sessions = list(db_manager.sessions.find({
        'userId': user_id,
        'startTime': {'$gte': week_ago}
    }))
    
    daily_breakdown = {}
    for i in range(7):
        date = (datetime.now() - timedelta(days=i)).date()
        daily_breakdown[date.isoformat()] = {
            'sessions': 0,
            'minutes': 0,
            'day_name': date.strftime('%A')
        }
    
    for session in sessions:
        date_key = session['startTime'].date().isoformat()
        if date_key in daily_breakdown:
            daily_breakdown[date_key]['sessions'] += 1
            daily_breakdown[date_key]['minutes'] += session.get('duration', 0) // 60
    
    return list(daily_breakdown.values())

def get_monthly_breakdown(user_id):
    """Get monthly practice breakdown"""
    month_ago = datetime.now() - timedelta(days=30)
    sessions = list(db_manager.sessions.find({
        'userId': user_id,
        'startTime': {'$gte': month_ago}
    }))
    
    weekly_breakdown = {}
    for session in sessions:
        week_start = session['startTime'] - timedelta(days=session['startTime'].weekday())
        week_key = week_start.date().isoformat()
        
        if week_key not in weekly_breakdown:
            weekly_breakdown[week_key] = {
                'week_start': week_key,
                'sessions': 0,
                'minutes': 0
            }
        
        weekly_breakdown[week_key]['sessions'] += 1
        weekly_breakdown[week_key]['minutes'] += session.get('duration', 0) // 60
    
    return list(weekly_breakdown.values())

def get_pose_recommendations(user_id, recent_sessions):
    """Get personalized pose recommendations"""
    # Analyze user's weak areas and suggest poses
    weak_areas = analyze_weak_areas(recent_sessions)
    
    recommendations = []
    for area in weak_areas:
        poses = pose_model.search_poses('', {'category': area})
        if poses:
            recommendations.append({
                'area': area,
                'reason': f'Improve your {area} flexibility and strength',
                'poses': poses[:3]  # Top 3 poses for this area
            })
    
    return recommendations[:2]  # Top 2 recommendations

def analyze_weak_areas(sessions):
    """Analyze user's weak areas from session data"""
    area_performance = {}
    
    for session in sessions:
        for pose in session.get('poses', []):
            category = pose.get('category', 'general')
            accuracy = pose.get('accuracy', 0)
            
            if category not in area_performance:
                area_performance[category] = []
            area_performance[category].append(accuracy)
    
    # Find areas with lowest average accuracy
    weak_areas = []
    for area, accuracies in area_performance.items():
        avg_accuracy = sum(accuracies) / len(accuracies)
        if avg_accuracy < 75:  # Below 75% accuracy
            weak_areas.append(area)
    
    return weak_areas[:3]  # Top 3 weak areas

def get_schedule_recommendation(recent_sessions):
    """Recommend optimal practice schedule"""
    if not recent_sessions:
        return {
            'frequency': 'daily',
            'duration': 15,
            'best_time': '07:00',
            'reason': 'Start with daily 15-minute sessions in the morning'
        }
    
    # Analyze practice patterns
    practice_times = [s['startTime'].hour for s in recent_sessions if 'startTime' in s]
    avg_duration = sum(s.get('duration', 0) for s in recent_sessions) / len(recent_sessions) // 60
    
    most_common_hour = max(set(practice_times), key=practice_times.count) if practice_times else 7
    
    return {
        'frequency': 'daily' if len(recent_sessions) >= 5 else '3-4 times per week',
        'duration': max(15, min(45, int(avg_duration + 5))),
        'best_time': f"{most_common_hour:02d}:00",
        'reason': 'Based on your practice history and performance'
    }

# ============================================================================
# ENHANCED FEATURES (Commented out for basic functionality)
# ============================================================================

# SOCIAL FEATURES - Uncomment when enhanced models are available
"""
@app.route('/social/friends')
@require_auth
def friends():
    # Friends management page
    user_id = ObjectId(session['user_id'])
    user = db_manager.users.find_one({'_id': user_id})
    
    # Get friends list with details
    friend_ids = user.get('social', {}).get('friends', [])
    friends = list(db_manager.users.find(
        {'_id': {'$in': friend_ids}},
        {'profile': 1, 'stats': 1}
    ))
    
    # Get pending friend requests
    pending_requests = list(db_manager.social_activities.find({
        'toUser': user_id,
        'type': 'friend_request',
        'status': 'pending'
    }))
    
    # Enrich pending requests with sender info
    for request in pending_requests:
        sender = db_manager.users.find_one({'_id': request['fromUser']})
        if sender:
            request['sender'] = sender.get('profile', {})
    
    return render_template('social/friends.html',
                         friends=friends,
                         pending_requests=pending_requests)

@app.route('/api/social/send-friend-request', methods=['POST'])
@require_auth
def send_friend_request():
    """Send friend request"""
    user_id = ObjectId(session['user_id'])
    target_email = request.json.get('email', '').lower().strip()
    
    # Find target user
    target_user = db_manager.users.find_one({'email': target_email})
    if not target_user:
        return jsonify({'error': 'User not found'}), 404
    
    if target_user['_id'] == user_id:
        return jsonify({'error': 'Cannot send request to yourself'}), 400
    
    # Send request
    success = social_model.send_friend_request(user_id, target_user['_id'])
    
    if success:
        return jsonify({'success': True, 'message': 'Friend request sent'})
    else:
        return jsonify({'error': 'Request already exists or users are already friends'}), 400

@app.route('/api/social/accept-friend-request/<request_id>', methods=['POST'])
@require_auth
def accept_friend_request(request_id):
    """Accept friend request"""
    success = social_model.accept_friend_request(ObjectId(request_id))
    
    if success:
        return jsonify({'success': True, 'message': 'Friend request accepted'})
    else:
        return jsonify({'error': 'Invalid request'}), 400

@app.route('/api/social/leaderboard')
@require_auth
def get_leaderboard():
    """Get leaderboard data"""
    leaderboard_type = request.args.get('type', 'global')
    user_id = ObjectId(session['user_id'])
    
    if leaderboard_type == 'friends':
        # Get friends leaderboard
        user = db_manager.users.find_one({'_id': user_id})
        friend_ids = user.get('social', {}).get('friends', [])
        friend_ids.append(user_id)  # Include self
        
        leaderboard = list(db_manager.users.find(
            {'_id': {'$in': friend_ids}},
            {'profile.firstName': 1, 'stats': 1}
        ).sort('stats.xp', -1).limit(50))
    else:
        # Global leaderboard
        leaderboard = list(db_manager.users.find(
            {},
            {'profile.firstName': 1, 'stats': 1}
        ).sort('stats.xp', -1).limit(50))
    
    # Add rank
    for i, user in enumerate(leaderboard):
        user['rank'] = i + 1
    
    return jsonify(leaderboard)

# ============================================================================
# WEBSOCKET EVENTS (Real-time features)
# ============================================================================

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    if 'user_id' in session:
        join_room(f"user_{session['user_id']}")
        emit('connected', {'status': 'Connected to Yogic Guide'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    if 'user_id' in session:
        leave_room(f"user_{session['user_id']}")

@socketio.on('pose_update')
def handle_pose_update(data):
    """Handle real-time pose updates during session"""
    if 'user_id' not in session:
        return
    
    session_id = data.get('session_id')
    pose_data = data.get('pose_data', {})
    
    # Update session in real-time
    if session_id:
        db_manager.sessions.update_one(
            {'_id': ObjectId(session_id)},
            {'$set': {
                'currentPose': pose_data,
                'lastUpdate': datetime.now()
            }}
        )
    
    # Emit back to client for confirmation
    emit('pose_updated', {'status': 'success', 'timestamp': datetime.now().isoformat()})

@socketio.on('join_challenge')
def handle_join_challenge(data):
    """Handle joining a challenge"""
    if 'user_id' not in session:
        return
    
    user_id = ObjectId(session['user_id'])
    challenge_id = data.get('challenge_id')
    
    # Add user to challenge
    db_manager.challenges.update_one(
        {'_id': ObjectId(challenge_id)},
        {'$addToSet': {'participants': user_id}}
    )
    
    # Join challenge room for real-time updates
    join_room(f"challenge_{challenge_id}")
    
    emit('challenge_joined', {'challenge_id': challenge_id})

# ============================================================================
# ADMIN ROUTES (Basic admin functionality)
# ============================================================================

@app.route('/admin')
@require_auth
def admin_dashboard():
    """Basic admin dashboard"""
    # Simple admin check (in production, use proper role-based access)
    user_id = ObjectId(session['user_id'])
    user = db_manager.users.find_one({'_id': user_id})
    
    if not user or user.get('email') != 'admin@yogicguide.com':
        return redirect(url_for('dashboard'))
    
    # Get platform statistics
    stats = {
        'total_users': db_manager.users.count_documents({}),
        'total_sessions': db_manager.sessions.count_documents({}),
        'active_users_today': db_manager.sessions.count_documents({
            'startTime': {'$gte': datetime.now().replace(hour=0, minute=0, second=0)}
        }),
        'total_poses': db_manager.poses.count_documents({})
    }
    
    return render_template('admin/dashboard.html', stats=stats)

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403

# ============================================================================
# HEALTH CHECK & MONITORING
# ============================================================================

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check database connection
        db_manager.users.find_one()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/system/stats')
def system_stats():
    """System statistics for monitoring"""
    try:
        stats = {
            'database': {
                'users': db_manager.users.count_documents({}),
                'sessions': db_manager.sessions.count_documents({}),
                'poses': db_manager.poses.count_documents({})
            },
            'activity': {
                'sessions_today': db_manager.sessions.count_documents({
                    'startTime': {'$gte': datetime.now().replace(hour=0, minute=0, second=0)}
                }),
                'active_users_week': len(db_manager.sessions.distinct('userId', {
                    'startTime': {'$gte': datetime.now() - timedelta(days=7)}
                }))
            }
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# APPLICATION STARTUP
# ============================================================================

if __name__ == '__main__':
    # Simple startup
    try:
        print("🚀 Starting Yogic Guide...")
        print(f"📊 Database: {app.config.get('MONGO_URI', 'Not configured')}")
        print(f"🌐 Server: http://localhost:5000")
        
        if socketio:
            socketio.run(app, debug=True, host='0.0.0.0', port=5000)
        else:
            app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        print("💡 Make sure MongoDB is running and dependencies are installed")

"""

def init_default_data():
    """Initialize default poses and achievements"""
    # Check if poses exist
    if db_manager.poses.count_documents({}) == 0:
        create_default_poses()
    
    # Ensure achievements are created
    achievement_model.create_default_achievements()

def create_default_poses():
    """Create default pose library"""
    default_poses = [
        {
            'name': 'Mountain Pose',
            'sanskrit': 'Tadasana',
            'module': 'stretching',
            'sequence': 1,
            'difficulty': 'beginner',
            'category': 'standing',
            'duration': {'hold': 30, 'default': 30, 'minimum': 15, 'maximum': 60},
            'technique': {
                'startingPosition': 'Stand tall with feet hip-width apart',
                'steps': [
                    'Ground through your feet',
                    'Engage your leg muscles',
                    'Lengthen your spine',
                    'Relax your shoulders',
                    'Breathe deeply'
                ],
                'alignment': [
                    'Keep your weight evenly distributed',
                    'Maintain natural curves of spine'
                ],
                'warnings': ['Avoid locking knees']
            },
            'benefits': {
                'primary': ['Improves posture', 'Builds foundation'],
                'secondary': ['Increases awareness', 'Calms mind']
            },
            'measurements': {
                'shoulderAngle': {'min': 170, 'max': 190, 'ideal': 180},
                'hipAngle': {'min': 170, 'max': 190, 'ideal': 180},
                'bodySymmetry': 0.9
            },
            'contraindications': ['Severe balance issues'],
            'tags': ['beginner', 'foundation', 'posture'],
            'createdAt': datetime.now()
        },
        {
            'name': 'Downward Dog',
            'sanskrit': 'Adho Mukha Svanasana',
            'module': 'stretching',
            'sequence': 2,
            'difficulty': 'beginner',
            'category': 'inversion',
            'duration': {'hold': 45, 'default': 45, 'minimum': 20, 'maximum': 90},
            'technique': {
                'startingPosition': 'Start on hands and knees',
                'steps': [
                    'Tuck toes under',
                    'Lift hips up and back',
                    'Straighten legs as much as possible',
                    'Press hands firmly into ground',
                    'Create inverted V shape'
                ],
                'alignment': [
                    'Keep hands shoulder-width apart',
                    'External rotation of arms',
                    'Long spine'
                ],
                'warnings': ['Avoid if you have wrist injuries']
            },
            'benefits': {
                'primary': ['Stretches hamstrings', 'Strengthens arms'],
                'secondary': ['Calms nervous system', 'Improves circulation']
            },
            'measurements': {
                'shoulderAngle': {'min': 40, 'max': 60, 'ideal': 50},
                'hipAngle': {'min': 70, 'max': 90, 'ideal': 80},
                'elbowAngle': {'min': 170, 'max': 180, 'ideal': 175}
            },
            'contraindications': ['Wrist injuries', 'High blood pressure'],
            'tags': ['inversion', 'strength', 'flexibility'],
            'createdAt': datetime.now()
        }
        # Add more poses as needed
    ]
    
    for pose in default_poses:
        db_manager.poses.update_one(
            {'name': pose['name']},
            {'$setOnInsert': pose},
            upsert=True
        )