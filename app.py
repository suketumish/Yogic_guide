#!/usr/bin/env python3
"""
Zen_Align - Clean Working Version
Basic functionality without complex features
"""

import os
import logging
from datetime import datetime, timedelta
from bson import ObjectId
import bcrypt

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash

# Import yoga pose detection API
try:
    from yoga_api_routes import register_yoga_api_routes
    YOGA_API_AVAILABLE = True
    print("✅ Yoga API module loaded")
except Exception as e:
    print(f"⚠️  Yoga API not available: {e}")
    YOGA_API_AVAILABLE = False

# Basic configuration
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database setup with fallback
try:
    from pymongo import MongoClient
    from pymongo.server_api import ServerApi
    
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    
    # Check if it's Atlas URI
    if 'mongodb+srv://' in mongo_uri or 'mongodb.net' in mongo_uri:
        # MongoDB Atlas connection
        client = MongoClient(mongo_uri, server_api=ServerApi('1'))
        # Test the connection
        client.admin.command('ping')
        print("✅ MongoDB Atlas connected successfully!")
    else:
        # Local MongoDB connection
        client = MongoClient(mongo_uri)
        print("✅ MongoDB local connected")
    
    db = client.yogic_guide
    MONGO_AVAILABLE = True
    
except Exception as e:
    print(f"⚠️  MongoDB connection failed: {e}")
    print(f"⚠️  URI being used: {os.getenv('MONGO_URI', 'Not set')[:50]}...")
    MONGO_AVAILABLE = False
    db = None

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def require_auth(f):
    """Decorator to require authentication"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def require_admin(f):
    """Decorator to require admin authentication"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        
        if MONGO_AVAILABLE:
            user_id = ObjectId(session['user_id'])
            user = db.users.find_one({'_id': user_id})
            if not user or user.get('role') != 'admin':
                flash('Access denied. Admin privileges required.', 'error')
                return redirect(url_for('dashboard'))
        else:
            # Fallback: check if user is marked as admin in session
            if not session.get('is_admin', False):
                flash('Access denied. Admin privileges required.', 'error')
                return redirect(url_for('dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function

def is_admin():
    """Check if current user is admin"""
    if 'user_id' not in session:
        return False
    
    if MONGO_AVAILABLE:
        user_id = ObjectId(session['user_id'])
        user = db.users.find_one({'_id': user_id})
        return user and user.get('role') == 'admin'
    else:
        return session.get('is_admin', False)

def generate_unique_user_id():
    """
    Generate a unique 8-character alphanumeric user ID
    Validates uniqueness against database to prevent collisions
    Returns: String - 8-character uppercase alphanumeric ID
    """
    import uuid
    
    if not MONGO_AVAILABLE:
        # Fallback when database is not available
        return str(uuid.uuid4())[:8].upper()
    
    max_attempts = 10
    for attempt in range(max_attempts):
        # Generate 8-character ID from UUID
        unique_id = str(uuid.uuid4())[:8].upper()
        
        # Check if ID already exists in database
        existing_user = db.users.find_one({'uniqueId': unique_id})
        
        if not existing_user:
            # ID is unique, return it
            return unique_id
    
    # If we couldn't generate a unique ID after max_attempts,
    # use a longer UUID segment to ensure uniqueness
    return str(uuid.uuid4()).replace('-', '')[:12].upper()

def create_admin_user():
    """Create default admin user if none exists"""
    if not MONGO_AVAILABLE:
        return False
    
    # Check if admin exists
    admin_exists = db.users.find_one({'role': 'admin'})
    if admin_exists:
        return True
    
    # Create default admin
    admin_data = {
        'uniqueId': generate_unique_user_id(),  # Add unique ID for admin
        'email': 'admin@yogicguide.com',
        'password': hash_password('admin123'),  # Change this in production!
        'profile': {
            'name': 'Super Admin',
            'experience_level': 'Expert'
        },
        'role': 'admin',
        'createdAt': datetime.now(),
        'stats': {'totalSessions': 0, 'totalMinutes': 0}
    }
    
    try:
        result = db.users.insert_one(admin_data)
        print(f"✅ Admin user created with ID: {result.inserted_id}")
        print("📧 Admin email: admin@yogicguide.com")
        print("🔑 Admin password: admin123 (CHANGE THIS!)")
        return True
    except Exception as e:
        print(f"❌ Failed to create admin user: {e}")
        return False

# ============================================================================
# BASIC ROUTES
# ============================================================================

@app.route('/')
def index():
    """Landing page or redirect to dashboard if authenticated"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('landing.html')

@app.route('/about')
def about():
    """About Us page"""
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact Us page"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        if all([name, email, subject, message]):
            # Here you can add email sending logic or save to database
            # For now, just show success message
            flash(f'Thank you {name}! We have received your message and will respond soon.', 'success')
            return redirect(url_for('contact'))
        else:
            flash('Please fill in all fields.', 'error')
    
    return render_template('contact.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Basic user registration"""
    if request.method == 'POST':
        try:
            email = request.form.get('email', '').lower().strip()
            password = request.form.get('password', '')
            name = request.form.get('name', '').strip()
            age = request.form.get('age', '')
            mobile = request.form.get('mobile', '').strip()
            gender = request.form.get('gender', '')
            experience = request.form.get('experience', 'Beginner')
            
            # Validation
            if not all([email, password, name, age, mobile]):
                flash('Name, age, email, mobile and password are required.', 'error')
                return render_template('register.html')
            
            if len(password) < 6:
                flash('Password must be at least 6 characters long.', 'error')
                return render_template('register.html')
            
            if len(mobile) != 10 or not mobile.isdigit():
                flash('Please enter a valid 10-digit mobile number.', 'error')
                return render_template('register.html')
            
            if not MONGO_AVAILABLE:
                flash('Database connection error. Please try again later.', 'error')
                print("❌ Registration failed: MongoDB not available")
                return render_template('register.html')
            
            # Check if user exists
            existing_user = db.users.find_one({'email': email})
            if existing_user:
                flash('Email already registered. Please login instead.', 'error')
                return render_template('register.html')
            
            # Check if mobile exists
            existing_mobile = db.users.find_one({'mobile': mobile})
            if existing_mobile:
                flash('Mobile number already registered. Please use a different number.', 'error')
                return render_template('register.html')
            
            # Generate unique user ID with database validation
            unique_user_id = generate_unique_user_id()
            
            # Create user document
            user_data = {
                'uniqueId': unique_user_id,  # Unique 8-character ID for display
                'email': email,
                'mobile': mobile,
                'password': hash_password(password),
                'profile': {
                    'name': name,
                    'age': int(age) if age else None,
                    'gender': gender if gender else None,
                    'experience': experience
                },
                'role': 'user',
                'tags': [],  # For agent tags
                'skills': [],  # For skill badges
                'createdAt': datetime.now(),
                'stats': {
                    'totalSessions': 0,
                    'totalMinutes': 0,
                    'totalPoses': 0
                },
                'achievements': [],
                'preferences': {
                    'notifications': True,
                    'theme': 'light',
                    'voiceOver': True  # Voice-over preference
                }
            }
            
            # Insert user
            result = db.users.insert_one(user_data)
            
            if result.inserted_id:
                # Set session
                session['user_id'] = str(result.inserted_id)
                session['is_admin'] = False
                session['user_name'] = name
                
                print(f"✅ User registered successfully: {email}")
                flash(f'Welcome {name}! Your account has been created successfully.', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Registration failed. Please try again.', 'error')
                print("❌ Registration failed: Insert returned no ID")
                
        except Exception as e:
            error_msg = str(e)
            flash(f'Registration error: {error_msg}', 'error')
            print(f"❌ Registration exception: {error_msg}")
            import traceback
            traceback.print_exc()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Basic login functionality"""
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password', '')
        
        if not all([email, password]):
            flash('Email and password are required.', 'error')
            return render_template('login.html')
        
        if MONGO_AVAILABLE:
            user = db.users.find_one({'email': email})
            if user and verify_password(password, user['password']):
                session['user_id'] = str(user['_id'])
                session['is_admin'] = user.get('role') == 'admin'
                
                if session['is_admin']:
                    flash('Welcome back, Admin!', 'success')
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('Login successful!', 'success')
                    return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password.', 'error')
        else:
            flash('Database not available. Please try again later.', 'error')
    
    return render_template('login.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Dedicated admin login page"""
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password', '')
        
        if not all([email, password]):
            flash('Email and password are required.', 'error')
            return render_template('admin_login.html')
        
        if MONGO_AVAILABLE:
            user = db.users.find_one({'email': email})
            if user and verify_password(password, user['password']):
                if user.get('role') == 'admin':
                    session['user_id'] = str(user['_id'])
                    session['is_admin'] = True
                    flash('Welcome to Admin Panel!', 'success')
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('Access denied. Admin privileges required.', 'error')
            else:
                flash('Invalid admin credentials.', 'error')
        else:
            # Fallback for demo purposes
            if email == 'admin@yogicguide.com' and password == 'admin123':
                session['user_id'] = 'demo_admin'
                session['is_admin'] = True
                flash('Welcome to Admin Panel! (Demo Mode)', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid admin credentials.', 'error')
    
    return render_template('admin_login.html')

@app.route('/logout')
def logout():
    """Basic logout"""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password - send reset link"""
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        
        if not email:
            flash('Please enter your email address.', 'error')
            return render_template('forgot_password.html')
        
        if MONGO_AVAILABLE:
            user = db.users.find_one({'email': email})
            
            if user:
                # Generate simple reset token (in production, use secure token generation)
                import secrets
                reset_token = secrets.token_urlsafe(32)
                
                # Store token with expiry (1 hour)
                db.users.update_one(
                    {'email': email},
                    {
                        '$set': {
                            'reset_token': reset_token,
                            'reset_token_expiry': datetime.utcnow() + timedelta(hours=1)
                        }
                    }
                )
                
                # In production, send email with reset link
                # For now, just show success message
                flash(f'Password reset link has been sent to {email}. Please check your email.', 'success')
                logging.info(f'Password reset requested for: {email}')
                logging.info(f'Reset link: {url_for("reset_password", token=reset_token, _external=True)}')
            else:
                # Don't reveal if email exists or not (security best practice)
                flash(f'If an account exists with {email}, you will receive a password reset link.', 'info')
        else:
            flash('Database not available. Please try again later.', 'error')
        
        return redirect(url_for('login'))
    
    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password with token"""
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not all([email, password, confirm_password]):
            flash('All fields are required.', 'error')
            return render_template('reset_password.html', token=token)
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('reset_password.html', token=token)
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return render_template('reset_password.html', token=token)
        
        if MONGO_AVAILABLE:
            # Find user with valid token
            user = db.users.find_one({
                'email': email,
                'reset_token': token,
                'reset_token_expiry': {'$gt': datetime.utcnow()}
            })
            
            if user:
                # Hash new password
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                
                # Update password and remove reset token
                db.users.update_one(
                    {'email': email},
                    {
                        '$set': {'password': hashed_password},
                        '$unset': {'reset_token': '', 'reset_token_expiry': ''}
                    }
                )
                
                flash('Password reset successful! You can now login with your new password.', 'success')
                logging.info(f'Password reset successful for: {email}')
                return redirect(url_for('login'))
            else:
                flash('Invalid or expired reset link. Please request a new one.', 'error')
        else:
            flash('Database not available. Please try again later.', 'error')
    
    return render_template('reset_password.html', token=token)

@app.route('/dashboard')
@require_auth
def dashboard():
    """Basic dashboard with module-wise breakdown"""
    if MONGO_AVAILABLE:
        user_id = ObjectId(session['user_id'])
        user = db.users.find_one({'_id': user_id})
        
        # Get recent sessions
        recent_sessions = list(db.sessions.find(
            {'userId': user_id}
        ).sort('startTime', -1).limit(5))
        
        # Calculate progress stats
        total_sessions = db.sessions.count_documents({'userId': user_id})
        total_minutes = 0
        
        # Calculate total minutes from sessions
        for session_doc in db.sessions.find({'userId': user_id}):
            if 'duration' in session_doc:
                total_minutes += session_doc.get('duration', 0)
        
        # Calculate streak (simplified - consecutive days with sessions)
        streak_days = 0
        today = datetime.now().date()
        current_date = today
        
        for i in range(30):  # Check last 30 days
            sessions_on_date = db.sessions.count_documents({
                'userId': user_id,
                'startTime': {
                    '$gte': datetime.combine(current_date, datetime.min.time()),
                    '$lt': datetime.combine(current_date + timedelta(days=1), datetime.min.time())
                }
            })
            
            if sessions_on_date > 0:
                streak_days += 1
                current_date -= timedelta(days=1)
            else:
                break
        
        # Get module-wise breakdown
        module_pipeline = [
            {'$match': {'userId': user_id}},
            {'$group': {
                '_id': {'$ifNull': ['$module', '$moduleType']},
                'count': {'$sum': 1},
                'total_duration': {'$sum': '$duration'}
            }},
            {'$sort': {'count': -1}}
        ]
        module_breakdown = list(db.sessions.aggregate(module_pipeline))
        
        # Format module names
        module_name_map = {
            'surya_namaskar': 'Surya Namaskar',
            'breathing': 'Breathing Exercises',
            'stretching': 'Stretching Routine',
            'meditation': 'Meditation',
            'yoga': 'Yoga Practice',
            'mindfulness': 'Mindfulness',
            'custom': 'Custom Routine'
        }
        
        for module in module_breakdown:
            module_key = module['_id']
            module['name'] = module_name_map.get(module_key, module_key.replace('_', ' ').title() if module_key else 'Unknown')
            module['duration_minutes'] = round(module['total_duration'] / 60, 1)
        
        progress = {
            'total_sessions': total_sessions,
            'total_minutes': total_minutes,
            'streak_days': streak_days,
            'module_breakdown': module_breakdown
        }
        
        # Set user name in session for template
        if user and 'profile' in user and 'name' in user['profile']:
            session['user_name'] = user['profile']['name']
        
        return render_template('dashboard.html', user=user, recent_sessions=recent_sessions, progress=progress)
    else:
        # Fallback data when database is not available
        progress = {
            'total_sessions': 0,
            'total_minutes': 0,
            'streak_days': 0,
            'module_breakdown': []
        }
        session['user_name'] = 'User'
        return render_template('dashboard.html', user={'profile': {'name': 'User'}}, recent_sessions=[], progress=progress)

@app.route('/profile')
@require_auth
def profile():
    """Basic profile page with module filtering support"""
    if MONGO_AVAILABLE:
        user_id = ObjectId(session['user_id'])
        user_doc = db.users.find_one({'_id': user_id})
        
        # Get module filter from query params
        module_filter = request.args.get('module', None)
        
        if user_doc:
            # Transform user data to match template expectations
            user = {
                'uniqueId': user_doc.get('uniqueId', str(user_doc.get('_id'))[:8].upper()),
                'name': user_doc.get('profile', {}).get('name', 'User'),
                'email': user_doc.get('email', ''),
                'mobile': user_doc.get('mobile', 'Not provided'),
                'age': user_doc.get('profile', {}).get('age', 'Not specified'),
                'gender': user_doc.get('profile', {}).get('gender', 'Not specified'),
                'experience_level': user_doc.get('profile', {}).get('experience', 'Beginner'),
                'created_at': user_doc.get('createdAt', datetime.now()),
                'total_sessions': user_doc.get('stats', {}).get('totalSessions', 0),
                'total_minutes': user_doc.get('stats', {}).get('totalMinutes', 0)
            }
            
            # Build session query with optional module filter
            session_query = {'userId': user_id}
            if module_filter:
                session_query['$or'] = [
                    {'module': module_filter},
                    {'moduleType': module_filter}
                ]
            
            # Get recent sessions for profile
            recent_sessions = []
            sessions = db.sessions.find(session_query).sort('startTime', -1).limit(10)
            
            for session_doc in sessions:
                module = session_doc.get('module') or session_doc.get('moduleType', 'Unknown')
                recent_sessions.append({
                    'module': module,
                    'module_type': session_doc.get('moduleType', module),
                    'module_name': session_doc.get('moduleName', module.replace('_', ' ').title()),
                    'start_time': session_doc.get('startTime', datetime.now()),
                    'duration': session_doc.get('duration', 0),
                    'accuracy': session_doc.get('accuracy', 0)
                })
            
            # Get available modules for filter dropdown
            available_modules = db.sessions.distinct('module', {'userId': user_id})
            if not available_modules:
                available_modules = db.sessions.distinct('moduleType', {'userId': user_id})
            
            module_name_map = {
                'surya_namaskar': 'Surya Namaskar',
                'breathing': 'Breathing Exercises',
                'stretching': 'Stretching Routine',
                'meditation': 'Meditation',
                'yoga': 'Yoga Practice',
                'mindfulness': 'Mindfulness',
                'custom': 'Custom Routine'
            }
            
            modules_list = [
                {
                    'value': mod,
                    'name': module_name_map.get(mod, mod.replace('_', ' ').title() if mod else 'Unknown')
                }
                for mod in available_modules if mod
            ]
            
            return render_template('profile_new.html', 
                                 user=user, 
                                 sessions=recent_sessions,
                                 available_modules=modules_list,
                                 selected_module=module_filter)
        else:
            # User not found, create default
            user = {
                'name': 'User',
                'email': 'user@example.com',
                'age': 'Not specified',
                'gender': 'Not specified',
                'experience_level': 'Beginner',
                'created_at': datetime.now()
            }
            return render_template('profile_new.html', user=user, sessions=[], available_modules=[], selected_module=None)
    else:
        # Fallback when database is not available
        user = {
            'name': 'User',
            'email': 'user@example.com',
            'age': 'Not specified',
            'gender': 'Not specified',
            'experience_level': 'Beginner',
            'created_at': datetime.now()
        }
        return render_template('profile.html', user=user, recent_sessions=[])

# Badge showcase route removed - badges system disabled
# @app.route('/badge-showcase')
# @require_auth
# def badge_showcase():
#     """Badge system showcase page for testing and demonstration"""
#     return render_template('badge_showcase.html')

@app.route('/module/stretching/info')
@require_auth
def module_stretching_info():
    """Full Body Stretching module information page"""
    return render_template('module_stretching.html')

@app.route('/module/breathing/info')
@require_auth
def module_breathing_info():
    """Breathing Exercises module information page"""
    return render_template('module_breathing.html')

@app.route('/module/surya-namaskar/info')
@require_auth
def module_surya_namaskar_info():
    """Surya Namaskar module information page"""
    return render_template('module_surya_namaskar.html')

@app.route('/module/<module_type>')
@require_auth
def module_session(module_type):
    """Basic module session"""
    valid_modules = {
        'breathing': 'Breathing Exercises',
        'meditation': 'Meditation',
        'yoga': 'Yoga Practice',
        'mindfulness': 'Mindfulness',
        'stretching': 'Stretching',
        'surya-namaskar': 'Surya Namaskar'
    }
    
    if module_type not in valid_modules:
        flash('Invalid module type.', 'error')
        return redirect(url_for('dashboard'))
    
    module_name = valid_modules[module_type]
    return render_template('session.html', module_type=module_type, module_name=module_name)

@app.route('/api/session/start/surya-namaskar', methods=['POST'])
@require_auth
def start_surya_namaskar_session():
    """Start a Surya Namaskar session"""
    return start_module_session('surya_namaskar', 'Surya Namaskar')

@app.route('/api/session/start/breathing', methods=['POST'])
@require_auth
def start_breathing_session():
    """Start a Breathing Exercises session"""
    return start_module_session('breathing', 'Breathing Exercises')

@app.route('/api/session/start/stretching', methods=['POST'])
@require_auth
def start_stretching_session():
    """Start a Stretching Routine session"""
    return start_module_session('stretching', 'Stretching Routine')

@app.route('/api/session/start/meditation', methods=['POST'])
@require_auth
def start_meditation_session():
    """Start a Meditation session"""
    return start_module_session('meditation', 'Meditation')

@app.route('/api/session/start/yoga', methods=['POST'])
@require_auth
def start_yoga_session():
    """Start a Yoga Practice session"""
    return start_module_session('yoga', 'Yoga Practice')

def start_module_session(module_type, module_name):
    """Helper function to start a module-specific session"""
    try:
        if not MONGO_AVAILABLE:
            return jsonify({'error': 'Database not available'}), 500
        
        user_id = ObjectId(session['user_id'])
        
        # Create session document with module field
        session_doc = {
            'userId': user_id,
            'module': module_type,  # REQUIRED: Module type for tracking and filtering
            'moduleType': module_type.replace('_', '-'),  # Keep for backward compatibility
            'moduleName': module_name,
            'startTime': datetime.now(),
            'endTime': None,
            'duration': 0,
            'poses': [],
            'poseCorrections': [],
            'accuracy': 0,
            'status': 'active',
            'createdAt': datetime.now()
        }
        
        result = db.sessions.insert_one(session_doc)
        
        return jsonify({
            'success': True,
            'session_id': str(result.inserted_id),
            'module': module_type,
            'module_name': module_name,
            'message': f'{module_name} session started successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/pose/<pose_id>')
@require_auth
def pose_details(pose_id):
    """
    View detailed information about a specific pose
    Supports both ObjectId and pose name lookups
    Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6
    """
    if not MONGO_AVAILABLE:
        flash('Database not available. Please try again later.', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        # Try to find pose by ObjectId first
        try:
            pose = db.poses.find_one({'_id': ObjectId(pose_id)})
        except:
            # If not a valid ObjectId, try finding by name
            pose = db.poses.find_one({'name': pose_id})
            
            # Also try URL-friendly name format (e.g., "mountain-pose")
            if not pose:
                # Convert URL format to title case (mountain-pose -> Mountain Pose)
                pose_name = pose_id.replace('-', ' ').title()
                pose = db.poses.find_one({'name': pose_name})
        
        if not pose:
            flash('Pose not found.', 'error')
            return redirect(url_for('dashboard'))
        
        # Add default icon if not present
        if 'icon' not in pose:
            pose['icon'] = '🧘'
        
        # Ensure all required fields have defaults
        pose.setdefault('difficulty', 'Beginner')
        pose.setdefault('category', 'Yoga')
        pose.setdefault('duration', 30)
        pose.setdefault('module', 'yoga')
        
        return render_template('pose_details.html', pose=pose)
        
    except Exception as e:
        print(f"Error loading pose details: {e}")
        import traceback
        traceback.print_exc()
        flash('Error loading pose details.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/session-complete')
@require_auth
def session_complete():
    """Basic session completion page"""
    return render_template('session-complete.html')

@app.route('/yoga-test')
def yoga_test():
    """Yoga pose detection test page (no auth required for testing)"""
    return render_template('yoga_test.html')

@app.route('/mediapipe-test')
def mediapipe_test():
    """MediaPipe pose detection diagnostic page"""
    return render_template('mediapipe_test.html')

@app.route('/test-simple-pose')
def test_simple_pose():
    """Test page for simple pose detector"""
    return render_template('test_simple_pose.html')

@app.route('/simple-yoga-test')
def simple_yoga_test():
    """Simple yoga pose detection test (works without MediaPipe)"""
    return render_template('simple_yoga_test.html')

# ============================================================================
# ADMIN ROUTES
# ============================================================================

@app.route('/admin')
@require_admin
def admin_dashboard():
    """Admin dashboard with system overview"""
    if MONGO_AVAILABLE:
        # Get system statistics
        total_users = db.users.count_documents({})
        total_sessions = db.sessions.count_documents({})
        total_admins = db.users.count_documents({'role': 'admin'})
        
        # Get recent users
        recent_users = list(db.users.find({}).sort('createdAt', -1).limit(10))
        
        # Get recent sessions
        recent_sessions = list(db.sessions.find({}).sort('startTime', -1).limit(10))
        
        # Get user activity stats
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        users_today = db.users.count_documents({'createdAt': {'$gte': today}})
        sessions_today = db.sessions.count_documents({'startTime': {'$gte': today}})
        
        stats = {
            'total_users': total_users,
            'total_sessions': total_sessions,
            'total_admins': total_admins,
            'users_today': users_today,
            'sessions_today': sessions_today
        }
        
        return render_template('admin/dashboard.html', 
                             stats=stats, 
                             recent_users=recent_users, 
                             recent_sessions=recent_sessions,
                             current_time=datetime.now())
    else:
        # Fallback stats
        stats = {
            'total_users': 0,
            'total_sessions': 0,
            'total_admins': 1,
            'users_today': 0,
            'sessions_today': 0
        }
        return render_template('admin/dashboard.html', 
                             stats=stats, 
                             recent_users=[], 
                             recent_sessions=[],
                             current_time=datetime.now())

@app.route('/admin/users')
@require_admin
def admin_users():
    """Admin user management"""
    if MONGO_AVAILABLE:
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        # Get users with pagination
        total_users = db.users.count_documents({})
        users = list(db.users.find({}).sort('createdAt', -1).skip((page-1)*per_page).limit(per_page))
        
        # Calculate pagination
        total_pages = (total_users + per_page - 1) // per_page
        
        return render_template('admin/users.html', 
                             users=users, 
                             page=page, 
                             total_pages=total_pages,
                             total_users=total_users)
    else:
        return render_template('admin/users.html', 
                             users=[], 
                             page=1, 
                             total_pages=1,
                             total_users=0)

@app.route('/admin/users/<user_id>')
@require_admin
def admin_user_detail(user_id):
    """Admin user detail view"""
    if MONGO_AVAILABLE:
        try:
            user = db.users.find_one({'_id': ObjectId(user_id)})
            if not user:
                flash('User not found.', 'error')
                return redirect(url_for('admin_users'))
            
            # Get user sessions
            user_sessions = list(db.sessions.find({'userId': ObjectId(user_id)}).sort('startTime', -1))
            
            return render_template('admin/user_detail.html', user=user, sessions=user_sessions)
        except Exception as e:
            flash(f'Error loading user: {str(e)}', 'error')
            return redirect(url_for('admin_users'))
    else:
        flash('Database not available.', 'error')
        return redirect(url_for('admin_users'))

@app.route('/admin/users/<user_id>/toggle-admin', methods=['POST'])
@require_admin
def admin_toggle_user_admin(user_id):
    """Toggle user admin status"""
    if MONGO_AVAILABLE:
        try:
            user = db.users.find_one({'_id': ObjectId(user_id)})
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Toggle admin role
            new_role = 'admin' if user.get('role') != 'admin' else 'user'
            db.users.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': {'role': new_role}}
            )
            
            action = 'granted' if new_role == 'admin' else 'revoked'
            return jsonify({'success': True, 'message': f'Admin privileges {action}', 'new_role': new_role})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Database not available'}), 500

@app.route('/admin/users/<user_id>/delete', methods=['POST'])
@require_admin
def admin_delete_user(user_id):
    """Delete user (admin only)"""
    if MONGO_AVAILABLE:
        try:
            # Don't allow deleting the last admin
            user = db.users.find_one({'_id': ObjectId(user_id)})
            if user and user.get('role') == 'admin':
                admin_count = db.users.count_documents({'role': 'admin'})
                if admin_count <= 1:
                    return jsonify({'error': 'Cannot delete the last admin user'}), 400
            
            # Delete user and their sessions
            db.users.delete_one({'_id': ObjectId(user_id)})
            db.sessions.delete_many({'userId': ObjectId(user_id)})
            
            return jsonify({'success': True, 'message': 'User deleted successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Database not available'}), 500

@app.route('/admin/sessions')
@require_admin
def admin_sessions():
    """Admin session management"""
    if MONGO_AVAILABLE:
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        # Get sessions with user info
        pipeline = [
            {'$lookup': {
                'from': 'users',
                'localField': 'userId',
                'foreignField': '_id',
                'as': 'user'
            }},
            {'$sort': {'startTime': -1}},
            {'$skip': (page-1) * per_page},
            {'$limit': per_page}
        ]
        
        sessions = list(db.sessions.aggregate(pipeline))
        total_sessions = db.sessions.count_documents({})
        total_pages = (total_sessions + per_page - 1) // per_page
        
        return render_template('admin/sessions.html', 
                             sessions=sessions, 
                             page=page, 
                             total_pages=total_pages,
                             total_sessions=total_sessions)
    else:
        return render_template('admin/sessions.html', 
                             sessions=[], 
                             page=1, 
                             total_pages=1,
                             total_sessions=0)

@app.route('/admin/analytics')
@require_admin
def admin_analytics():
    """Enhanced admin analytics dashboard with comprehensive insights"""
    if MONGO_AVAILABLE:
        # Time ranges for analysis
        now = datetime.now()
        thirty_days_ago = now - timedelta(days=30)
        seven_days_ago = now - timedelta(days=7)
        yesterday = now - timedelta(days=1)
        
        # 1. User Growth Analytics
        user_growth_pipeline = [
            {'$match': {'createdAt': {'$gte': thirty_days_ago}}},
            {'$group': {
                '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$createdAt'}},
                'new_users': {'$sum': 1}
            }},
            {'$sort': {'_id': 1}}
        ]
        user_growth = list(db.users.aggregate(user_growth_pipeline))
        
        # 2. Session Analytics
        session_analytics_pipeline = [
            {'$match': {'startTime': {'$gte': thirty_days_ago}}},
            {'$group': {
                '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$startTime'}},
                'sessions': {'$sum': 1},
                'total_duration': {'$sum': '$duration'},
                'avg_duration': {'$avg': '$duration'}
            }},
            {'$sort': {'_id': 1}}
        ]
        session_analytics = list(db.sessions.aggregate(session_analytics_pipeline))
        
        # 3. Module Performance - Updated to use 'module' field
        module_performance_pipeline = [
            {'$group': {
                '_id': {'$ifNull': ['$module', '$moduleType']},  # Use module field, fallback to moduleType
                'sessions': {'$sum': 1},
                'total_duration': {'$sum': '$duration'},
                'avg_duration': {'$avg': '$duration'},
                'unique_users': {'$addToSet': '$userId'}
            }},
            {'$addFields': {
                'unique_user_count': {'$size': '$unique_users'}
            }},
            {'$sort': {'sessions': -1}}
        ]
        module_performance = list(db.sessions.aggregate(module_performance_pipeline))
        
        # 4. User Engagement Levels
        user_engagement_pipeline = [
            {'$group': {
                '_id': '$userId',
                'session_count': {'$sum': 1},
                'total_time': {'$sum': '$duration'}
            }},
            {'$bucket': {
                'groupBy': '$session_count',
                'boundaries': [0, 1, 5, 10, 20, 50, 100],
                'default': '100+',
                'output': {
                    'users': {'$sum': 1},
                    'avg_total_time': {'$avg': '$total_time'}
                }
            }}
        ]
        user_engagement = list(db.sessions.aggregate(user_engagement_pipeline))
        
        # 5. Hourly Usage Patterns
        hourly_usage_pipeline = [
            {'$match': {'startTime': {'$gte': seven_days_ago}}},
            {'$group': {
                '_id': {'$hour': '$startTime'},
                'sessions': {'$sum': 1}
            }},
            {'$sort': {'_id': 1}}
        ]
        hourly_usage = list(db.sessions.aggregate(hourly_usage_pipeline))
        
        # 6. Weekly Trends
        weekly_trends_pipeline = [
            {'$match': {'startTime': {'$gte': thirty_days_ago}}},
            {'$group': {
                '_id': {'$dayOfWeek': '$startTime'},
                'sessions': {'$sum': 1},
                'avg_duration': {'$avg': '$duration'}
            }},
            {'$sort': {'_id': 1}}
        ]
        weekly_trends = list(db.sessions.aggregate(weekly_trends_pipeline))
        
        # 7. User Retention Analysis
        retention_pipeline = [
            {'$group': {
                '_id': '$userId',
                'first_session': {'$min': '$startTime'},
                'last_session': {'$max': '$startTime'},
                'session_count': {'$sum': 1}
            }},
            {'$addFields': {
                'days_active': {
                    '$divide': [
                        {'$subtract': ['$last_session', '$first_session']},
                        86400000  # milliseconds in a day
                    ]
                }
            }},
            {'$bucket': {
                'groupBy': '$days_active',
                'boundaries': [0, 1, 7, 14, 30],
                'default': '30+',
                'output': {
                    'users': {'$sum': 1}
                }
            }}
        ]
        retention_analysis = list(db.sessions.aggregate(retention_pipeline))
        
        # 8. Performance Metrics
        total_users = db.users.count_documents({})
        total_sessions = db.sessions.count_documents({})
        active_users_7d = len(db.sessions.distinct('userId', {'startTime': {'$gte': seven_days_ago}}))
        active_users_30d = len(db.sessions.distinct('userId', {'startTime': {'$gte': thirty_days_ago}}))
        
        # Calculate averages
        avg_session_duration = 0
        if total_sessions > 0:
            duration_result = list(db.sessions.aggregate([
                {'$group': {'_id': None, 'avg_duration': {'$avg': '$duration'}}}
            ]))
            if duration_result:
                avg_session_duration = duration_result[0]['avg_duration'] or 0
        
        # 9. Accuracy Distribution (for pie chart)
        accuracy_distribution_pipeline = [
            {'$match': {'overallAccuracy': {'$exists': True, '$ne': None}}},
            {'$bucket': {
                'groupBy': '$overallAccuracy',
                'boundaries': [0, 60, 75, 90, 100],
                'default': 'other',
                'output': {
                    'count': {'$sum': 1}
                }
            }}
        ]
        accuracy_buckets = list(db.sessions.aggregate(accuracy_distribution_pipeline))
        
        # Map buckets to distribution
        accuracy_distribution = {
            'poor': 0,
            'fair': 0,
            'good': 0,
            'excellent': 0
        }
        
        for bucket in accuracy_buckets:
            if bucket['_id'] == 0:
                accuracy_distribution['poor'] = bucket['count']
            elif bucket['_id'] == 60:
                accuracy_distribution['fair'] = bucket['count']
            elif bucket['_id'] == 75:
                accuracy_distribution['good'] = bucket['count']
            elif bucket['_id'] == 90:
                accuracy_distribution['excellent'] = bucket['count']
        
        # 10. Platform Health Score (for gauge chart)
        # Calculate health score based on multiple factors
        user_activity_score = min(100, (active_users_7d / max(1, total_users)) * 200)  # 50% active = 100 score
        session_quality_score = min(100, (avg_session_duration / 600) * 100) if avg_session_duration else 0  # 10 min = 100 score
        retention_score = min(100, (active_users_7d / max(1, total_users)) * 200)
        
        # Calculate average accuracy for engagement score
        avg_accuracy = 0
        if total_sessions > 0:
            accuracy_result = list(db.sessions.aggregate([
                {'$match': {'overallAccuracy': {'$exists': True, '$ne': None}}},
                {'$group': {'_id': None, 'avg_accuracy': {'$avg': '$overallAccuracy'}}}
            ]))
            if accuracy_result:
                avg_accuracy = accuracy_result[0]['avg_accuracy'] or 0
        
        engagement_score = min(100, avg_accuracy)
        
        # Overall health score (weighted average)
        platform_health_score = round(
            (user_activity_score * 0.3 + 
             session_quality_score * 0.25 + 
             retention_score * 0.25 + 
             engagement_score * 0.2)
        )
        
        platform_health = {
            'score': platform_health_score,
            'user_activity': round(user_activity_score),
            'session_quality': round(session_quality_score),
            'retention': round(retention_score),
            'engagement': round(engagement_score)
        }
        
        analytics_data = {
            'user_growth': user_growth,
            'session_analytics': session_analytics,
            'module_performance': module_performance,
            'user_engagement': user_engagement,
            'hourly_usage': hourly_usage,
            'weekly_trends': weekly_trends,
            'retention_analysis': retention_analysis,
            'accuracy_distribution': accuracy_distribution,
            'platform_health': platform_health,
            'metrics': {
                'total_users': total_users,
                'total_sessions': total_sessions,
                'active_users_7d': active_users_7d,
                'active_users_30d': active_users_30d,
                'avg_session_duration': round(avg_session_duration / 60, 1) if avg_session_duration else 0,
                'user_retention_rate': round((active_users_7d / total_users * 100), 1) if total_users > 0 else 0
            }
        }
        
        return render_template('admin/analytics.html', analytics=analytics_data)
    else:
        # Generate sample data for demo when database is not available
        import random
        
        # Generate sample data for the last 30 days
        sample_dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]
        
        analytics_data = {
            'user_growth': [
                {'_id': date, 'new_users': random.randint(2, 15)} 
                for date in sample_dates
            ],
            'session_analytics': [
                {
                    '_id': date, 
                    'sessions': random.randint(5, 50),
                    'total_duration': random.randint(300, 3000),
                    'avg_duration': random.randint(600, 1800)
                } 
                for date in sample_dates
            ],
            'module_performance': [
                {'_id': 'breathing', 'sessions': 145, 'total_duration': 8700, 'avg_duration': 900, 'unique_user_count': 32},
                {'_id': 'meditation', 'sessions': 98, 'total_duration': 11760, 'avg_duration': 1200, 'unique_user_count': 28},
                {'_id': 'yoga', 'sessions': 76, 'total_duration': 6840, 'avg_duration': 900, 'unique_user_count': 24},
                {'_id': 'stretching', 'sessions': 54, 'total_duration': 2700, 'avg_duration': 500, 'unique_user_count': 18},
                {'_id': 'surya-namaskar', 'sessions': 43, 'total_duration': 3440, 'avg_duration': 800, 'unique_user_count': 15}
            ],
            'user_engagement': [
                {'_id': 1, 'users': 25},
                {'_id': 5, 'users': 18},
                {'_id': 10, 'users': 12},
                {'_id': 20, 'users': 8},
                {'_id': 50, 'users': 3}
            ],
            'hourly_usage': [
                {'_id': hour, 'sessions': random.randint(1, 20)} 
                for hour in range(24)
            ],
            'weekly_trends': [
                {'_id': day, 'sessions': random.randint(10, 40)} 
                for day in range(1, 8)
            ],
            'retention_analysis': [
                {'_id': 0, 'users': 45},
                {'_id': 1, 'users': 32},
                {'_id': 7, 'users': 18},
                {'_id': 14, 'users': 12},
                {'_id': 30, 'users': 8}
            ],
            'accuracy_distribution': {
                'excellent': 120,
                'good': 180,
                'fair': 80,
                'poor': 36
            },
            'platform_health': {
                'score': 78,
                'user_activity': 82,
                'session_quality': 75,
                'retention': 70,
                'engagement': 85
            },
            'metrics': {
                'total_users': 156,
                'total_sessions': 416,
                'active_users_7d': 89,
                'active_users_30d': 134,
                'avg_session_duration': 12.5,
                'user_retention_rate': 57.1
            }
        }
        return render_template('admin/analytics.html', analytics=analytics_data)

@app.route('/api/analytics/live', methods=['GET'])
@require_admin
def get_live_analytics():
    """API endpoint for real-time analytics updates"""
    if not MONGO_AVAILABLE:
        return jsonify({'error': 'Database not available'}), 500
    
    try:
        # Time ranges for analysis
        now = datetime.now()
        thirty_days_ago = now - timedelta(days=30)
        seven_days_ago = now - timedelta(days=7)
        
        # 1. Key Metrics
        total_users = db.users.count_documents({})
        total_sessions = db.sessions.count_documents({})
        active_users_7d = len(db.sessions.distinct('userId', {'startTime': {'$gte': seven_days_ago}}))
        active_users_30d = len(db.sessions.distinct('userId', {'startTime': {'$gte': thirty_days_ago}}))
        
        # Calculate average session duration
        avg_session_duration = 0
        if total_sessions > 0:
            duration_result = list(db.sessions.aggregate([
                {'$group': {'_id': None, 'avg_duration': {'$avg': '$duration'}}}
            ]))
            if duration_result:
                avg_session_duration = duration_result[0]['avg_duration'] or 0
        
        # 2. User Growth (last 30 days)
        user_growth_pipeline = [
            {'$match': {'createdAt': {'$gte': thirty_days_ago}}},
            {'$group': {
                '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$createdAt'}},
                'new_users': {'$sum': 1}
            }},
            {'$sort': {'_id': 1}}
        ]
        user_growth = list(db.users.aggregate(user_growth_pipeline))
        
        # 3. Session Analytics (last 30 days)
        session_analytics_pipeline = [
            {'$match': {'startTime': {'$gte': thirty_days_ago}}},
            {'$group': {
                '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$startTime'}},
                'sessions': {'$sum': 1},
                'total_duration': {'$sum': '$duration'},
                'avg_duration': {'$avg': '$duration'}
            }},
            {'$sort': {'_id': 1}}
        ]
        session_analytics = list(db.sessions.aggregate(session_analytics_pipeline))
        
        # 4. Module Performance
        module_performance_pipeline = [
            {'$group': {
                '_id': {'$ifNull': ['$module', '$moduleType']},
                'sessions': {'$sum': 1},
                'total_duration': {'$sum': '$duration'},
                'avg_duration': {'$avg': '$duration'},
                'unique_users': {'$addToSet': '$userId'}
            }},
            {'$addFields': {
                'unique_user_count': {'$size': '$unique_users'}
            }},
            {'$sort': {'sessions': -1}}
        ]
        module_performance = list(db.sessions.aggregate(module_performance_pipeline))
        
        # 5. User Engagement Levels
        user_engagement_pipeline = [
            {'$group': {
                '_id': '$userId',
                'session_count': {'$sum': 1},
                'total_time': {'$sum': '$duration'}
            }},
            {'$bucket': {
                'groupBy': '$session_count',
                'boundaries': [0, 1, 5, 10, 20, 50, 100],
                'default': '100+',
                'output': {
                    'users': {'$sum': 1},
                    'avg_total_time': {'$avg': '$total_time'}
                }
            }}
        ]
        user_engagement = list(db.sessions.aggregate(user_engagement_pipeline))
        
        # 6. Hourly Usage Patterns (last 7 days)
        hourly_usage_pipeline = [
            {'$match': {'startTime': {'$gte': seven_days_ago}}},
            {'$group': {
                '_id': {'$hour': '$startTime'},
                'sessions': {'$sum': 1}
            }},
            {'$sort': {'_id': 1}}
        ]
        hourly_usage = list(db.sessions.aggregate(hourly_usage_pipeline))
        
        # 7. Weekly Trends
        weekly_trends_pipeline = [
            {'$match': {'startTime': {'$gte': thirty_days_ago}}},
            {'$group': {
                '_id': {'$dayOfWeek': '$startTime'},
                'sessions': {'$sum': 1},
                'avg_duration': {'$avg': '$duration'}
            }},
            {'$sort': {'_id': 1}}
        ]
        weekly_trends = list(db.sessions.aggregate(weekly_trends_pipeline))
        
        # 8. User Retention Analysis
        retention_pipeline = [
            {'$group': {
                '_id': '$userId',
                'first_session': {'$min': '$startTime'},
                'last_session': {'$max': '$startTime'},
                'session_count': {'$sum': 1}
            }},
            {'$addFields': {
                'days_active': {
                    '$divide': [
                        {'$subtract': ['$last_session', '$first_session']},
                        86400000
                    ]
                }
            }},
            {'$bucket': {
                'groupBy': '$days_active',
                'boundaries': [0, 1, 7, 14, 30],
                'default': '30+',
                'output': {
                    'users': {'$sum': 1}
                }
            }}
        ]
        retention_analysis = list(db.sessions.aggregate(retention_pipeline))
        
        # 9. Accuracy Distribution
        accuracy_distribution_pipeline = [
            {'$match': {'overallAccuracy': {'$exists': True, '$ne': None}}},
            {'$bucket': {
                'groupBy': '$overallAccuracy',
                'boundaries': [0, 60, 75, 90, 100],
                'default': 'other',
                'output': {
                    'count': {'$sum': 1}
                }
            }}
        ]
        accuracy_buckets = list(db.sessions.aggregate(accuracy_distribution_pipeline))
        
        accuracy_distribution = {
            'poor': 0,
            'fair': 0,
            'good': 0,
            'excellent': 0
        }
        
        for bucket in accuracy_buckets:
            if bucket['_id'] == 0:
                accuracy_distribution['poor'] = bucket['count']
            elif bucket['_id'] == 60:
                accuracy_distribution['fair'] = bucket['count']
            elif bucket['_id'] == 75:
                accuracy_distribution['good'] = bucket['count']
            elif bucket['_id'] == 90:
                accuracy_distribution['excellent'] = bucket['count']
        
        # 10. Platform Health Score
        user_activity_score = min(100, (active_users_7d / max(1, total_users)) * 200)
        session_quality_score = min(100, (avg_session_duration / 600) * 100) if avg_session_duration else 0
        retention_score = min(100, (active_users_7d / max(1, total_users)) * 200)
        
        avg_accuracy = 0
        if total_sessions > 0:
            accuracy_result = list(db.sessions.aggregate([
                {'$match': {'overallAccuracy': {'$exists': True, '$ne': None}}},
                {'$group': {'_id': None, 'avg_accuracy': {'$avg': '$overallAccuracy'}}}
            ]))
            if accuracy_result:
                avg_accuracy = accuracy_result[0]['avg_accuracy'] or 0
        
        engagement_score = min(100, avg_accuracy)
        
        platform_health_score = round(
            (user_activity_score * 0.3 + 
             session_quality_score * 0.25 + 
             retention_score * 0.25 + 
             engagement_score * 0.2)
        )
        
        # Build response
        response_data = {
            'timestamp': now.isoformat(),
            'metrics': {
                'totalUsers': total_users,
                'totalSessions': total_sessions,
                'activeUsers7d': active_users_7d,
                'activeUsers30d': active_users_30d,
                'avgSessionDuration': round(avg_session_duration / 60, 1) if avg_session_duration else 0,
                'retentionRate': round((active_users_7d / total_users * 100), 1) if total_users > 0 else 0
            },
            'userGrowth': {
                'labels': [item['_id'] for item in user_growth],
                'data': [item['new_users'] for item in user_growth]
            },
            'sessionAnalytics': {
                'labels': [item['_id'] for item in session_analytics],
                'sessions': [item['sessions'] for item in session_analytics],
                'durations': [round(item['avg_duration'] / 60, 1) for item in session_analytics]
            },
            'modulePerformance': {
                'labels': [item['_id'].replace('-', ' ').replace('_', ' ').title() if item['_id'] else 'Unknown' for item in module_performance],
                'data': [item['sessions'] for item in module_performance],
                'users': [item['unique_user_count'] for item in module_performance],
                'durations': [item['avg_duration'] for item in module_performance]
            },
            'userEngagement': {
                'labels': [f"{item['_id']} sessions" if item['_id'] != '100+' else 'New Users' for item in user_engagement],
                'data': [item['users'] for item in user_engagement]
            },
            'hourlyUsage': {str(item['_id']): item['sessions'] for item in hourly_usage},
            'weeklyTrends': {str(item['_id']): item['sessions'] for item in weekly_trends},
            'retention': {
                'labels': [f"{item['_id']} days" if item['_id'] != '30+' else 'Same Day' for item in retention_analysis],
                'data': [item['users'] for item in retention_analysis]
            },
            'accuracyDistribution': {
                'labels': ['Excellent (90-100%)', 'Good (75-89%)', 'Fair (60-74%)', 'Needs Improvement (<60%)'],
                'data': [
                    accuracy_distribution['excellent'],
                    accuracy_distribution['good'],
                    accuracy_distribution['fair'],
                    accuracy_distribution['poor']
                ]
            },
            'platformHealth': {
                'score': platform_health_score,
                'components': {
                    'userActivity': round(user_activity_score),
                    'sessionQuality': round(session_quality_score),
                    'retention': round(retention_score),
                    'engagement': round(engagement_score)
                }
            }
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error fetching live analytics: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/admin/settings')
@require_admin
def admin_settings():
    """Admin system settings"""
    return render_template('admin/settings.html')

# ============================================================================
# API ROUTES
# ============================================================================

@app.route('/api/pose/validate', methods=['POST'])
@require_auth
def validate_pose():
    """Enhanced pose validation with strict correction logic"""
    try:
        data = request.get_json()
        pose_name = data.get('pose_name', '')
        keypoints = data.get('keypoints', {})
        session_id = data.get('session_id')
        
        # Calculate pose accuracy (simplified - in production use ML model)
        accuracy = calculate_pose_accuracy(keypoints)
        
        # Strict validation: must meet 75% threshold
        is_valid = accuracy >= 75
        
        result = {
            'valid': is_valid,
            'accuracy': accuracy,
            'pose_name': pose_name,
            'canContinue': is_valid,
            'feedback': generate_pose_feedback(pose_name, accuracy, is_valid)
        }
        
        # If pose is incorrect, mark session for review
        if not is_valid and session_id and MONGO_AVAILABLE:
            db.sessions.update_one(
                {'_id': ObjectId(session_id)},
                {
                    '$push': {
                        'poseCorrections': {
                            'pose': pose_name,
                            'accuracy': accuracy,
                            'timestamp': datetime.now(),
                            'valid': False
                        }
                    }
                }
            )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def calculate_pose_accuracy(keypoints):
    """Calculate pose accuracy from keypoints"""
    if not keypoints:
        return 0
    
    # Simplified calculation - count confident keypoints
    confident_points = sum(1 for kp in keypoints.values() if kp.get('confidence', 0) > 0.5)
    total_points = len(keypoints)
    
    if total_points == 0:
        return 0
    
    accuracy = (confident_points / total_points) * 100
    return round(accuracy)

def generate_pose_feedback(pose_name, accuracy, is_valid):
    """Generate feedback based on pose accuracy"""
    if is_valid:
        if accuracy >= 95:
            return f"Excellent! Your {pose_name} is perfect!"
        elif accuracy >= 85:
            return f"Great job! Your {pose_name} looks good!"
        else:
            return f"Good! Keep maintaining your {pose_name}!"
    else:
        if accuracy < 50:
            return f"Please adjust your entire {pose_name} position. Check the reference image."
        elif accuracy < 65:
            return f"Your {pose_name} needs significant adjustment. Focus on alignment."
        else:
            return f"You're close! Minor adjustments needed for {pose_name}."

@app.route('/api/session/start', methods=['POST'])
@require_auth
def start_session():
    """Start a new practice session with module tracking"""
    try:
        data = request.get_json()
        module_type = data.get('module_type')
        module_name = data.get('module_name')
        
        if not MONGO_AVAILABLE:
            return jsonify({'error': 'Database not available'}), 500
        
        if not module_type:
            return jsonify({'error': 'Module type is required'}), 400
        
        user_id = ObjectId(session['user_id'])
        
        # Normalize module type (convert hyphens to underscores for consistency)
        normalized_module = module_type.replace('-', '_')
        
        # Generate module name if not provided
        if not module_name:
            module_name_map = {
                'surya_namaskar': 'Surya Namaskar',
                'breathing': 'Breathing Exercises',
                'stretching': 'Stretching Routine',
                'meditation': 'Meditation',
                'yoga': 'Yoga Practice',
                'mindfulness': 'Mindfulness',
                'custom': 'Custom Routine'
            }
            module_name = module_name_map.get(normalized_module, normalized_module.replace('_', ' ').title())
        
        # Create session document with module field
        session_doc = {
            'userId': user_id,
            'module': normalized_module,  # REQUIRED: Module type for tracking and filtering
            'moduleType': module_type,  # Keep for backward compatibility
            'moduleName': module_name,
            'startTime': datetime.now(),
            'endTime': None,
            'duration': 0,
            'poses': [],
            'poseCorrections': [],
            'accuracy': 0,
            'status': 'active',
            'createdAt': datetime.now()
        }
        
        result = db.sessions.insert_one(session_doc)
        
        return jsonify({
            'success': True,
            'session_id': str(result.inserted_id),
            'module': normalized_module,
            'message': 'Session started successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/session/complete', methods=['POST'])
@require_auth
def complete_session():
    """Complete a practice session"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        duration = data.get('duration', 0)
        accuracy = data.get('accuracy', 0)
        poses_completed = data.get('poses_completed', [])
        
        if not MONGO_AVAILABLE:
            return jsonify({'error': 'Database not available'}), 500
        
        user_id = ObjectId(session['user_id'])
        
        # Update session
        db.sessions.update_one(
            {'_id': ObjectId(session_id)},
            {
                '$set': {
                    'endTime': datetime.now(),
                    'duration': duration,
                    'accuracy': accuracy,
                    'poses': poses_completed,
                    'status': 'completed'
                }
            }
        )
        
        # Update user stats
        db.users.update_one(
            {'_id': user_id},
            {
                '$inc': {
                    'stats.totalSessions': 1,
                    'stats.totalMinutes': duration // 60,
                    'stats.totalPoses': len(poses_completed)
                }
            }
        )
        
        return jsonify({
            'success': True,
            'message': 'Session completed successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/preferences', methods=['POST'])
@require_auth
def save_user_preferences():
    """Save user preferences including voice-over settings"""
    try:
        data = request.get_json()
        
        if not MONGO_AVAILABLE:
            return jsonify({'error': 'Database not available'}), 500
        
        user_id = ObjectId(session['user_id'])
        
        # Extract voice-over preferences
        preferences = {}
        if 'voiceOverEnabled' in data:
            preferences['voiceOverEnabled'] = data['voiceOverEnabled']
        if 'voiceOverSpeed' in data:
            preferences['voiceOverSpeed'] = data['voiceOverSpeed']
        if 'voiceOverVolume' in data:
            preferences['voiceOverVolume'] = data['voiceOverVolume']
        
        # Update user preferences
        db.users.update_one(
            {'_id': user_id},
            {
                '$set': {
                    'preferences': preferences,
                    'updatedAt': datetime.now()
                }
            }
        )
        
        return jsonify({
            'success': True,
            'message': 'Preferences saved successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/preferences', methods=['GET'])
@require_auth
def get_user_preferences():
    """Get user preferences"""
    try:
        if not MONGO_AVAILABLE:
            return jsonify({'error': 'Database not available'}), 500
        
        user_id = ObjectId(session['user_id'])
        user = db.users.find_one({'_id': user_id})
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        preferences = user.get('preferences', {})
        
        return jsonify({
            'success': True,
            'preferences': preferences
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/modules', methods=['GET'])
@require_auth
def get_module_analytics():
    """Get analytics aggregated by module"""
    try:
        if not MONGO_AVAILABLE:
            return jsonify({'error': 'Database not available'}), 500
        
        user_id = request.args.get('user_id')
        
        # Build match filter
        match_filter = {}
        if user_id:
            match_filter['userId'] = ObjectId(user_id)
        
        # Aggregate sessions by module
        pipeline = [
            {'$match': match_filter} if match_filter else {'$match': {}},
            {'$group': {
                '_id': {'$ifNull': ['$module', '$moduleType']},
                'total_sessions': {'$sum': 1},
                'total_duration': {'$sum': '$duration'},
                'avg_duration': {'$avg': '$duration'},
                'avg_accuracy': {'$avg': '$accuracy'},
                'total_poses': {'$sum': {'$size': {'$ifNull': ['$poses', []]}}},
                'unique_users': {'$addToSet': '$userId'}
            }},
            {'$addFields': {
                'unique_user_count': {'$size': '$unique_users'},
                'avg_duration_minutes': {'$divide': [{'$ifNull': ['$avg_duration', 0]}, 60]}
            }},
            {'$project': {
                'unique_users': 0  # Remove the array from output
            }},
            {'$sort': {'total_sessions': -1}}
        ]
        
        module_stats = list(db.sessions.aggregate(pipeline))
        
        # Format module names for display
        module_name_map = {
            'surya_namaskar': 'Surya Namaskar',
            'breathing': 'Breathing Exercises',
            'stretching': 'Stretching Routine',
            'meditation': 'Meditation',
            'yoga': 'Yoga Practice',
            'mindfulness': 'Mindfulness',
            'custom': 'Custom Routine'
        }
        
        for stat in module_stats:
            module_key = stat['_id']
            stat['module_name'] = module_name_map.get(module_key, module_key.replace('_', ' ').title() if module_key else 'Unknown')
        
        return jsonify({
            'success': True,
            'modules': module_stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/module/<module_type>', methods=['GET'])
@require_auth
def get_specific_module_analytics(module_type):
    """Get detailed analytics for a specific module"""
    try:
        if not MONGO_AVAILABLE:
            return jsonify({'error': 'Database not available'}), 500
        
        user_id = request.args.get('user_id')
        
        # Build match filter
        match_filter = {'$or': [{'module': module_type}, {'moduleType': module_type}]}
        if user_id:
            match_filter['userId'] = ObjectId(user_id)
        
        # Get sessions for this module
        sessions = list(db.sessions.find(match_filter).sort('startTime', -1).limit(50))
        
        # Calculate statistics
        total_sessions = len(sessions)
        total_duration = sum(s.get('duration', 0) for s in sessions)
        avg_accuracy = sum(s.get('accuracy', 0) for s in sessions) / total_sessions if total_sessions > 0 else 0
        
        # Get unique users
        unique_users = len(set(str(s.get('userId')) for s in sessions))
        
        # Get recent sessions with user info
        recent_sessions = []
        for s in sessions[:10]:
            user = db.users.find_one({'_id': s.get('userId')})
            recent_sessions.append({
                'session_id': str(s.get('_id')),
                'user_name': user.get('profile', {}).get('name', 'Unknown') if user else 'Unknown',
                'start_time': s.get('startTime').isoformat() if s.get('startTime') else None,
                'duration': s.get('duration', 0),
                'accuracy': s.get('accuracy', 0),
                'status': s.get('status', 'unknown')
            })
        
        return jsonify({
            'success': True,
            'module': module_type,
            'statistics': {
                'total_sessions': total_sessions,
                'total_duration': total_duration,
                'total_duration_minutes': round(total_duration / 60, 1),
                'avg_duration': round(total_duration / total_sessions, 1) if total_sessions > 0 else 0,
                'avg_accuracy': round(avg_accuracy, 1),
                'unique_users': unique_users
            },
            'recent_sessions': recent_sessions
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions/history', methods=['GET'])
@require_auth
def get_session_history():
    """Get session history with optional module filtering"""
    try:
        if not MONGO_AVAILABLE:
            return jsonify({'error': 'Database not available'}), 500
        
        user_id = ObjectId(session['user_id'])
        module_filter = request.args.get('module', None)
        limit = request.args.get('limit', 20, type=int)
        skip = request.args.get('skip', 0, type=int)
        
        # Build query with optional module filter
        query = {'userId': user_id}
        if module_filter:
            query['$or'] = [
                {'module': module_filter},
                {'moduleType': module_filter}
            ]
        
        # Get total count
        total_count = db.sessions.count_documents(query)
        
        # Get sessions
        sessions = list(db.sessions.find(query)
                       .sort('startTime', -1)
                       .skip(skip)
                       .limit(limit))
        
        # Format sessions for response
        formatted_sessions = []
        for s in sessions:
            module = s.get('module') or s.get('moduleType', 'Unknown')
            formatted_sessions.append({
                'session_id': str(s.get('_id')),
                'module': module,
                'module_name': s.get('moduleName', module.replace('_', ' ').title()),
                'start_time': s.get('startTime').isoformat() if s.get('startTime') else None,
                'end_time': s.get('endTime').isoformat() if s.get('endTime') else None,
                'duration': s.get('duration', 0),
                'duration_minutes': round(s.get('duration', 0) / 60, 1),
                'accuracy': s.get('accuracy', 0),
                'status': s.get('status', 'unknown'),
                'poses_count': len(s.get('poses', []))
            })
        
        return jsonify({
            'success': True,
            'sessions': formatted_sessions,
            'total_count': total_count,
            'has_more': (skip + limit) < total_count
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ANALYTICS API ENDPOINTS
# ============================================================================

@app.route('/api/analytics/overview', methods=['GET'])
@require_admin
def api_analytics_overview():
    """Get overview analytics - summary statistics for the dashboard"""
    try:
        if not MONGO_AVAILABLE:
            return jsonify({'error': 'Database not available'}), 500
        
        # Time ranges
        now = datetime.now()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        seven_days_ago = now - timedelta(days=7)
        thirty_days_ago = now - timedelta(days=30)
        
        # Total counts
        total_users = db.users.count_documents({})
        total_sessions = db.sessions.count_documents({})
        
        # Active users
        active_users_today = len(db.sessions.distinct('userId', {'startTime': {'$gte': today}}))
        active_users_7d = len(db.sessions.distinct('userId', {'startTime': {'$gte': seven_days_ago}}))
        active_users_30d = len(db.sessions.distinct('userId', {'startTime': {'$gte': thirty_days_ago}}))
        
        # Sessions today
        sessions_today = db.sessions.count_documents({'startTime': {'$gte': today}})
        sessions_7d = db.sessions.count_documents({'startTime': {'$gte': seven_days_ago}})
        sessions_30d = db.sessions.count_documents({'startTime': {'$gte': thirty_days_ago}})
        
        # Average session duration
        avg_duration_result = list(db.sessions.aggregate([
            {'$group': {'_id': None, 'avg_duration': {'$avg': '$duration'}}}
        ]))
        avg_session_duration = avg_duration_result[0]['avg_duration'] if avg_duration_result else 0
        
        # Average accuracy
        avg_accuracy_result = list(db.sessions.aggregate([
            {'$group': {'_id': None, 'avg_accuracy': {'$avg': '$accuracy'}}}
        ]))
        avg_accuracy = avg_accuracy_result[0]['avg_accuracy'] if avg_accuracy_result else 0
        
        # User retention rate (7-day active / total users)
        retention_rate = round((active_users_7d / total_users * 100), 1) if total_users > 0 else 0
        
        # Platform health score (composite metric)
        health_score = min(100, round(
            (active_users_7d / max(1, total_users) * 40) +  # 40% weight on active users
            (sessions_7d / max(1, total_users) * 30) +       # 30% weight on session frequency
            (avg_accuracy / 100 * 30)                         # 30% weight on accuracy
        ))
        
        overview = {
            'total_users': total_users,
            'total_sessions': total_sessions,
            'active_users_today': active_users_today,
            'active_users_7d': active_users_7d,
            'active_users_30d': active_users_30d,
            'sessions_today': sessions_today,
            'sessions_7d': sessions_7d,
            'sessions_30d': sessions_30d,
            'avg_session_duration_seconds': round(avg_session_duration),
            'avg_session_duration_minutes': round(avg_session_duration / 60, 1),
            'avg_accuracy': round(avg_accuracy, 1),
            'retention_rate': retention_rate,
            'health_score': health_score,
            'timestamp': now.isoformat()
        }
        
        return jsonify({
            'success': True,
            'data': overview
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/users', methods=['GET'])
@require_admin
def api_analytics_users():
    """Get user analytics - user growth and engagement metrics"""
    try:
        if not MONGO_AVAILABLE:
            return jsonify({'error': 'Database not available'}), 500
        
        days = request.args.get('days', 30, type=int)
        start_date = datetime.now() - timedelta(days=days)
        
        # User growth over time
        user_growth_pipeline = [
            {'$match': {'createdAt': {'$gte': start_date}}},
            {'$group': {
                '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$createdAt'}},
                'new_users': {'$sum': 1}
            }},
            {'$sort': {'_id': 1}}
        ]
        user_growth = list(db.users.aggregate(user_growth_pipeline))
        
        # User engagement levels (by session count)
        user_engagement_pipeline = [
            {'$group': {
                '_id': '$userId',
                'session_count': {'$sum': 1},
                'total_time': {'$sum': '$duration'}
            }},
            {'$bucket': {
                'groupBy': '$session_count',
                'boundaries': [0, 1, 5, 10, 20, 50, 100],
                'default': '100+',
                'output': {
                    'users': {'$sum': 1},
                    'avg_total_time': {'$avg': '$total_time'}
                }
            }}
        ]
        user_engagement = list(db.sessions.aggregate(user_engagement_pipeline))
        
        # Top active users
        top_users_pipeline = [
            {'$group': {
                '_id': '$userId',
                'session_count': {'$sum': 1},
                'total_duration': {'$sum': '$duration'},
                'avg_accuracy': {'$avg': '$accuracy'}
            }},
            {'$sort': {'session_count': -1}},
            {'$limit': 10},
            {'$lookup': {
                'from': 'users',
                'localField': '_id',
                'foreignField': '_id',
                'as': 'user_info'
            }}
        ]
        top_users_raw = list(db.sessions.aggregate(top_users_pipeline))
        
        # Format top users
        top_users = []
        for user_data in top_users_raw:
            user_info = user_data.get('user_info', [{}])[0]
            top_users.append({
                'user_id': str(user_data['_id']),
                'user_name': user_info.get('profile', {}).get('name', 'Unknown'),
                'session_count': user_data['session_count'],
                'total_duration_minutes': round(user_data['total_duration'] / 60, 1),
                'avg_accuracy': round(user_data['avg_accuracy'], 1)
            })
        
        return jsonify({
            'success': True,
            'data': {
                'user_growth': user_growth,
                'user_engagement': user_engagement,
                'top_users': top_users
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/sessions', methods=['GET'])
@require_admin
def api_analytics_sessions():
    """Get session analytics - session activity and patterns"""
    try:
        if not MONGO_AVAILABLE:
            return jsonify({'error': 'Database not available'}), 500
        
        days = request.args.get('days', 30, type=int)
        start_date = datetime.now() - timedelta(days=days)
        
        # Session activity over time
        session_activity_pipeline = [
            {'$match': {'startTime': {'$gte': start_date}}},
            {'$group': {
                '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$startTime'}},
                'sessions': {'$sum': 1},
                'total_duration': {'$sum': '$duration'},
                'avg_duration': {'$avg': '$duration'},
                'avg_accuracy': {'$avg': '$accuracy'}
            }},
            {'$sort': {'_id': 1}}
        ]
        session_activity = list(db.sessions.aggregate(session_activity_pipeline))
        
        # Format for response
        for item in session_activity:
            item['avg_duration_minutes'] = round(item['avg_duration'] / 60, 1) if item.get('avg_duration') else 0
            item['avg_accuracy'] = round(item['avg_accuracy'], 1) if item.get('avg_accuracy') else 0
        
        # Hourly usage patterns (last 7 days)
        seven_days_ago = datetime.now() - timedelta(days=7)
        hourly_usage_pipeline = [
            {'$match': {'startTime': {'$gte': seven_days_ago}}},
            {'$group': {
                '_id': {'$hour': '$startTime'},
                'sessions': {'$sum': 1}
            }},
            {'$sort': {'_id': 1}}
        ]
        hourly_usage = list(db.sessions.aggregate(hourly_usage_pipeline))
        
        # Weekly trends (day of week)
        weekly_trends_pipeline = [
            {'$match': {'startTime': {'$gte': start_date}}},
            {'$group': {
                '_id': {'$dayOfWeek': '$startTime'},
                'sessions': {'$sum': 1},
                'avg_duration': {'$avg': '$duration'}
            }},
            {'$sort': {'_id': 1}}
        ]
        weekly_trends = list(db.sessions.aggregate(weekly_trends_pipeline))
        
        # Format weekly trends with day names
        day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        for item in weekly_trends:
            item['day_name'] = day_names[item['_id'] - 1] if 1 <= item['_id'] <= 7 else 'Unknown'
            item['avg_duration_minutes'] = round(item['avg_duration'] / 60, 1) if item.get('avg_duration') else 0
        
        # Session duration distribution
        duration_distribution_pipeline = [
            {'$bucket': {
                'groupBy': '$duration',
                'boundaries': [0, 300, 600, 900, 1800, 3600],  # 0, 5min, 10min, 15min, 30min, 60min
                'default': '60+',
                'output': {
                    'count': {'$sum': 1}
                }
            }}
        ]
        duration_distribution = list(db.sessions.aggregate(duration_distribution_pipeline))
        
        return jsonify({
            'success': True,
            'data': {
                'session_activity': session_activity,
                'hourly_usage': hourly_usage,
                'weekly_trends': weekly_trends,
                'duration_distribution': duration_distribution
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/modules/<module>', methods=['GET'])
@require_admin
def api_analytics_module_specific(module):
    """Get analytics for a specific module"""
    try:
        if not MONGO_AVAILABLE:
            return jsonify({'error': 'Database not available'}), 500
        
        days = request.args.get('days', 30, type=int)
        start_date = datetime.now() - timedelta(days=days)
        
        # Match filter for the specific module
        match_filter = {
            '$or': [{'module': module}, {'moduleType': module}],
            'startTime': {'$gte': start_date}
        }
        
        # Module statistics
        module_stats_pipeline = [
            {'$match': match_filter},
            {'$group': {
                '_id': None,
                'total_sessions': {'$sum': 1},
                'total_duration': {'$sum': '$duration'},
                'avg_duration': {'$avg': '$duration'},
                'avg_accuracy': {'$avg': '$accuracy'},
                'unique_users': {'$addToSet': '$userId'}
            }},
            {'$addFields': {
                'unique_user_count': {'$size': '$unique_users'}
            }}
        ]
        module_stats_result = list(db.sessions.aggregate(module_stats_pipeline))
        
        if not module_stats_result:
            return jsonify({
                'success': True,
                'data': {
                    'module': module,
                    'statistics': {
                        'total_sessions': 0,
                        'total_duration_minutes': 0,
                        'avg_duration_minutes': 0,
                        'avg_accuracy': 0,
                        'unique_users': 0
                    },
                    'activity_over_time': [],
                    'accuracy_distribution': []
                }
            })
        
        module_stats = module_stats_result[0]
        
        # Activity over time for this module
        activity_pipeline = [
            {'$match': match_filter},
            {'$group': {
                '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$startTime'}},
                'sessions': {'$sum': 1},
                'avg_accuracy': {'$avg': '$accuracy'}
            }},
            {'$sort': {'_id': 1}}
        ]
        activity_over_time = list(db.sessions.aggregate(activity_pipeline))
        
        # Accuracy distribution
        accuracy_distribution_pipeline = [
            {'$match': match_filter},
            {'$bucket': {
                'groupBy': '$accuracy',
                'boundaries': [0, 50, 70, 85, 95, 100],
                'default': 'unknown',
                'output': {
                    'count': {'$sum': 1}
                }
            }}
        ]
        accuracy_distribution = list(db.sessions.aggregate(accuracy_distribution_pipeline))
        
        # Format statistics
        statistics = {
            'total_sessions': module_stats['total_sessions'],
            'total_duration_minutes': round(module_stats['total_duration'] / 60, 1),
            'avg_duration_minutes': round(module_stats['avg_duration'] / 60, 1),
            'avg_accuracy': round(module_stats['avg_accuracy'], 1),
            'unique_users': module_stats['unique_user_count']
        }
        
        return jsonify({
            'success': True,
            'data': {
                'module': module,
                'statistics': statistics,
                'activity_over_time': activity_over_time,
                'accuracy_distribution': accuracy_distribution
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/live', methods=['GET'])
@require_admin
def api_analytics_live():
    """Get real-time analytics data for live updates"""
    try:
        if not MONGO_AVAILABLE:
            return jsonify({'error': 'Database not available'}), 500
        
        now = datetime.now()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        last_hour = now - timedelta(hours=1)
        last_5_minutes = now - timedelta(minutes=5)
        
        # Active sessions (started in last hour, not completed)
        active_sessions = db.sessions.count_documents({
            'startTime': {'$gte': last_hour},
            'status': {'$in': ['active', 'paused']}
        })
        
        # Recent activity (last 5 minutes)
        recent_sessions = db.sessions.count_documents({
            'startTime': {'$gte': last_5_minutes}
        })
        
        # Sessions today
        sessions_today = db.sessions.count_documents({
            'startTime': {'$gte': today}
        })
        
        # Active users today
        active_users_today = len(db.sessions.distinct('userId', {
            'startTime': {'$gte': today}
        }))
        
        # Latest completed sessions
        latest_sessions_pipeline = [
            {'$match': {'status': 'completed'}},
            {'$sort': {'endTime': -1}},
            {'$limit': 5},
            {'$lookup': {
                'from': 'users',
                'localField': 'userId',
                'foreignField': '_id',
                'as': 'user_info'
            }}
        ]
        latest_sessions_raw = list(db.sessions.aggregate(latest_sessions_pipeline))
        
        # Format latest sessions
        latest_sessions = []
        for session_data in latest_sessions_raw:
            user_info = session_data.get('user_info', [{}])[0]
            module = session_data.get('module') or session_data.get('moduleType', 'Unknown')
            latest_sessions.append({
                'session_id': str(session_data['_id']),
                'user_name': user_info.get('profile', {}).get('name', 'Unknown'),
                'module': module,
                'duration_minutes': round(session_data.get('duration', 0) / 60, 1),
                'accuracy': round(session_data.get('accuracy', 0), 1),
                'completed_at': session_data.get('endTime').isoformat() if session_data.get('endTime') else None
            })
        
        # Module distribution today
        module_distribution_pipeline = [
            {'$match': {'startTime': {'$gte': today}}},
            {'$group': {
                '_id': {'$ifNull': ['$module', '$moduleType']},
                'count': {'$sum': 1}
            }},
            {'$sort': {'count': -1}}
        ]
        module_distribution = list(db.sessions.aggregate(module_distribution_pipeline))
        
        live_data = {
            'active_sessions': active_sessions,
            'recent_sessions_5min': recent_sessions,
            'sessions_today': sessions_today,
            'active_users_today': active_users_today,
            'latest_sessions': latest_sessions,
            'module_distribution_today': module_distribution,
            'timestamp': now.isoformat()
        }
        
        return jsonify({
            'success': True,
            'data': live_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'database': 'connected' if MONGO_AVAILABLE else 'disconnected'
        }
        return jsonify(status)
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/favicon.ico')
def favicon():
    """Favicon route to prevent 404 errors"""
    # Return a simple response to prevent 404 errors
    # In production, you would serve an actual favicon file
    return app.response_class(
        response='',
        status=204,
        headers={'Content-Type': 'image/x-icon'}
    )

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')), 500

# ============================================================================
# APPLICATION STARTUP
# ============================================================================

if __name__ == '__main__':
    print("🧘 Zen_Align - Starting Clean Version")
    print("=" * 40)
    
    # Register Yoga API routes
    if YOGA_API_AVAILABLE:
        try:
            register_yoga_api_routes(app)
            print("✅ Yoga Pose Detection API enabled")
        except Exception as e:
            print(f"⚠️  Failed to register Yoga API: {e}")
    else:
        print("⚠️  Yoga Pose Detection API disabled (models not trained)")
    
    # Get port from environment variable (required for Render)
    port = int(os.getenv('PORT', 5000))
    
    print(f"🌐 Server: http://0.0.0.0:{port}")
    print(f"📊 Database: {'Connected' if MONGO_AVAILABLE else 'Disconnected'}")
    
    # Create admin user if needed
    if MONGO_AVAILABLE:
        create_admin_user()
    
    print("⏹️  Press Ctrl+C to stop")
    
    try:
        # Use environment variable for debug mode
        debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
        app.run(debug=debug_mode, host='0.0.0.0', port=port)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Failed to start server: {e}")