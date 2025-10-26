#!/usr/bin/env python3
"""
Yogic Guide - Clean Working Version
Basic functionality without complex features
"""

import os
import logging
from datetime import datetime, timedelta
from bson import ObjectId
import bcrypt

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash

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
            
            # Create user document
            user_data = {
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
                'createdAt': datetime.now(),
                'stats': {
                    'totalSessions': 0,
                    'totalMinutes': 0,
                    'totalPoses': 0
                },
                'achievements': [],
                'preferences': {
                    'notifications': True,
                    'theme': 'light'
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

@app.route('/dashboard')
@require_auth
def dashboard():
    """Basic dashboard"""
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
        
        progress = {
            'total_sessions': total_sessions,
            'total_minutes': total_minutes,
            'streak_days': streak_days
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
            'streak_days': 0
        }
        session['user_name'] = 'User'
        return render_template('dashboard.html', user={'profile': {'name': 'User'}}, recent_sessions=[], progress=progress)

@app.route('/profile')
@require_auth
def profile():
    """Basic profile page"""
    if MONGO_AVAILABLE:
        user_id = ObjectId(session['user_id'])
        user_doc = db.users.find_one({'_id': user_id})
        
        if user_doc:
            # Transform user data to match template expectations
            user = {
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
            
            # Get recent sessions for profile
            recent_sessions = []
            sessions = db.sessions.find({'userId': user_id}).sort('startTime', -1).limit(10)
            
            for session_doc in sessions:
                recent_sessions.append({
                    'module_type': session_doc.get('moduleType', 'Unknown'),
                    'start_time': session_doc.get('startTime', datetime.now()),
                    'duration': session_doc.get('duration', 0)
                })
            
            return render_template('profile_new.html', user=user, sessions=recent_sessions)
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
            return render_template('profile_new.html', user=user, sessions=[])
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

@app.route('/session-complete')
@require_auth
def session_complete():
    """Basic session completion page"""
    return render_template('session-complete.html')

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
        
        # 3. Module Performance
        module_performance_pipeline = [
            {'$group': {
                '_id': '$moduleType',
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
        
        analytics_data = {
            'user_growth': user_growth,
            'session_analytics': session_analytics,
            'module_performance': module_performance,
            'user_engagement': user_engagement,
            'hourly_usage': hourly_usage,
            'weekly_trends': weekly_trends,
            'retention_analysis': retention_analysis,
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
    """Basic pose validation"""
    try:
        data = request.get_json()
        pose_name = data.get('pose_name', '')
        
        # Basic validation (in real app, this would use ML models)
        result = {
            'valid': True,
            'confidence': 0.85,
            'feedback': 'Good pose alignment!',
            'pose_name': pose_name
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
    print("🧘 Yogic Guide - Starting Clean Version")
    print("=" * 40)
    print(f"🌐 Server: http://localhost:5000")
    print(f"📊 Database: {'Connected' if MONGO_AVAILABLE else 'Disconnected'}")
    
    # Create admin user if needed
    if MONGO_AVAILABLE:
        create_admin_user()
    
    print("⏹️  Press Ctrl+C to stop")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Failed to start server: {e}")