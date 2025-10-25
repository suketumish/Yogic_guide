#!/usr/bin/env python3
"""
Basic test script to verify the application starts correctly
"""

import os
import sys

def test_imports():
    """Test that basic imports work"""
    try:
        print("Testing imports...")
        
        # Test Flask
        from flask import Flask
        print("✓ Flask imported successfully")
        
        # Test MongoDB
        from pymongo import MongoClient
        print("✓ PyMongo imported successfully")
        
        # Test bcrypt
        import bcrypt
        print("✓ bcrypt imported successfully")
        
        # Test basic app creation
        app = Flask(__name__)
        print("✓ Flask app created successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_mongodb_connection():
    """Test MongoDB connection"""
    try:
        from pymongo import MongoClient
        
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/yogic_guide')
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.server_info()
        print("✓ MongoDB connection successful")
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("💡 Make sure MongoDB is running on localhost:27017")
        return False

def test_app_startup():
    """Test that the app can start"""
    try:
        print("Testing app startup...")
        
        # Set environment for testing
        os.environ['FLASK_ENV'] = 'development'
        
        # Import the app
        from app import app
        print("✓ App imported successfully")
        
        # Test that app is configured
        if app.config.get('SECRET_KEY'):
            print("✓ App configuration loaded")
        else:
            print("⚠️ App configuration may be incomplete")
        
        return True
        
    except Exception as e:
        print(f"❌ App startup failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running basic tests for Yogic Guide...")
    print("=" * 50)
    
    tests = [
        ("Basic Imports", test_imports),
        ("MongoDB Connection", test_mongodb_connection),
        ("App Startup", test_app_startup)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! You can start the application with:")
        print("   python app.py")
    else:
        print("\n⚠️ Some tests failed. Please fix the issues before starting the app.")
        print("\n💡 Common solutions:")
        print("   - Install dependencies: pip install -r requirements.txt")
        print("   - Start MongoDB: mongod")
        print("   - Check .env configuration")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)