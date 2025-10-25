#!/usr/bin/env python3
"""
Simple startup script for Yogic Guide
This script provides a basic working version with fallback functionality
"""

import os
import sys
from datetime import datetime

def check_dependencies():
    """Check if required dependencies are available"""
    required_packages = [
        ('flask', 'Flask'),
        ('pymongo', 'PyMongo'),
        ('bcrypt', 'bcrypt'),
        ('bson', 'PyMongo BSON')
    ]
    
    missing = []
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"✓ {name}")
        except ImportError:
            missing.append(name)
            print(f"❌ {name} - Missing")
    
    return missing

def check_mongodb():
    """Check if MongoDB is accessible"""
    try:
        from pymongo import MongoClient
        
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/yogic_guide')
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
        client.server_info()
        
        print("✓ MongoDB connection successful")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

def setup_basic_data():
    """Set up basic data in MongoDB"""
    try:
        from pymongo import MongoClient
        import bcrypt
        
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/yogic_guide')
        client = MongoClient(mongo_uri)
        db = client.yogic_guide
        
        # Create a demo user if none exists
        if db.users.count_documents({}) == 0:
            demo_user = {
                'name': 'Demo User',
                'email': 'demo@yogicguide.com',
                'password': bcrypt.hashpw('demo123'.encode('utf-8'), bcrypt.gensalt()),
                'age': 25,
                'gender': 'Other',
                'experience_level': 'Beginner',
                'created_at': datetime.now(),
                'emailVerified': True
            }
            
            db.users.insert_one(demo_user)
            print("✓ Demo user created (demo@yogicguide.com / demo123)")
        
        # Create basic poses if none exist
        if db.poses.count_documents({}) == 0:
            basic_poses = [
                {
                    'name': 'Mountain Pose',
                    'sanskrit': 'Tadasana',
                    'module': 'stretching',
                    'difficulty': 'beginner',
                    'duration': 30,
                    'description': 'Stand tall with feet hip-width apart',
                    'created_at': datetime.now()
                },
                {
                    'name': 'Deep Breathing',
                    'sanskrit': 'Pranayama',
                    'module': 'breathing',
                    'difficulty': 'beginner',
                    'duration': 300,
                    'description': 'Slow, deep breathing exercise',
                    'created_at': datetime.now()
                }
            ]
            
            db.poses.insert_many(basic_poses)
            print("✓ Basic poses created")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to setup basic data: {e}")
        return False

def start_app():
    """Start the Flask application"""
    try:
        print("\n🚀 Starting Yogic Guide...")
        
        # Set development environment
        os.environ['FLASK_ENV'] = 'development'
        os.environ['FLASK_DEBUG'] = 'True'
        
        # Import and run the app
        from app import app, socketio
        
        print("🌐 Server starting at http://localhost:5000")
        print("📱 Demo login: demo@yogicguide.com / demo123")
        print("⏹️  Press Ctrl+C to stop the server")
        
        if socketio:
            socketio.run(app, debug=True, host='0.0.0.0', port=5000)
        else:
            app.run(debug=True, host='0.0.0.0', port=5000)
            
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Failed to start server: {e}")
        return False
    
    return True

def main():
    """Main startup function"""
    print("🧘 Yogic Guide - Basic Startup")
    print("=" * 40)
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        print("💡 Install them with: pip install -r requirements.txt")
        return False
    
    # Check MongoDB
    print("\n🗄️  Checking MongoDB...")
    if not check_mongodb():
        print("💡 Start MongoDB with: mongod")
        print("💡 Or install MongoDB from: https://www.mongodb.com/try/download/community")
        return False
    
    # Setup basic data
    print("\n📊 Setting up basic data...")
    if not setup_basic_data():
        print("⚠️ Failed to setup data, but continuing anyway...")
    
    # Start the app
    return start_app()

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)