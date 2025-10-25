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
    client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/'))
    db = client.yogic_guide
    MONGO_AVAILABLE = True
    print("✅ MongoDB connected")
except Exception as e:
    print(f"⚠️  MongoDB not available: {e}")
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

# ============================================================================
# BASIC ROUTES
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
            email = request.form.get('email', '').lower().strip()
            password = request.form.get('password', '')
            name = request.form.get('name', '').strip()
            
            if not all([email, password, name]):
                flash('All fields are required.', 'error')
                return render_template('register.html')
            
            if MONGO_AVAILABLE:
                # Check if user exists
                if db.users.find_one({'email': email}):
                    flash('Email already registered.', 'error')
                    return render_template('register.html')
                
                # Create user
                user_data = {
                    'email': email,
                    'password': hash_password(password),
                    'profile': {'name': name},
                    'createdAt': datetime.now(),
                    'stats': {'totalSessions': 0, 'totalMinutes': 0}
                }
                
                result = db.users.insert_one(user_data)
                session['user_id'] = str(result.inserted_id)
                flash('Registration successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Database not available. Please try again later.', 'error')
                
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'error')
    
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
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password.', 'error')
        else:
            flash('Database not available. Please try again later.', 'error')
    
    return render_template('login.html')

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
        
        return render_template('dashboard.html', user=user, recent_sessions=recent_sessions)
    else:
        return render_template('dashboard.html', user={'profile': {'name': 'User'}}, recent_sessions=[])

@app.route('/profile')
@require_auth
def profile():
    """Basic profile page"""
    if MONGO_AVAILABLE:
        user_id = ObjectId(session['user_id'])
        user = db.users.find_one({'_id': user_id})
        return render_template('profile.html', user=user)
    else:
        return render_template('profile.html', user={'profile': {'name': 'User'}})

@app.route('/module/<module_type>')
@require_auth
def module_session(module_type):
    """Basic module session"""
    valid_modules = ['breathing', 'meditation', 'yoga', 'mindfulness']
    if module_type not in valid_modules:
        flash('Invalid module type.', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('session.html', module_type=module_type)

@app.route('/session-complete')
@require_auth
def session_complete():
    """Basic session completion page"""
    return render_template('session-complete.html')

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

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# ============================================================================
# APPLICATION STARTUP
# ============================================================================

if __name__ == '__main__':
    print("🧘 Yogic Guide - Starting Clean Version")
    print("=" * 40)
    print(f"🌐 Server: http://localhost:5000")
    print(f"📊 Database: {'Connected' if MONGO_AVAILABLE else 'Disconnected'}")
    print("⏹️  Press Ctrl+C to stop")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Failed to start server: {e}")