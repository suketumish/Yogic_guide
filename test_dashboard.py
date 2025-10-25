#!/usr/bin/env python3
"""
Test script to verify dashboard functionality
"""

import sys
import os
from datetime import datetime

def test_dashboard_data():
    """Test if dashboard route provides correct data"""
    try:
        # Import the app
        from app import app, MONGO_AVAILABLE
        
        with app.test_client() as client:
            with client.session_transaction() as sess:
                # Simulate logged in user
                sess['user_id'] = '507f1f77bcf86cd799439011'  # Mock ObjectId
                sess['user_name'] = 'Test User'
            
            # Test dashboard route
            response = client.get('/dashboard')
            
            if response.status_code == 200:
                print("✅ Dashboard route works!")
                print(f"✅ Database status: {'Connected' if MONGO_AVAILABLE else 'Disconnected (using fallback)'}")
                return True
            else:
                print(f"❌ Dashboard returned status code: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Dashboard test failed: {e}")
        return False

def test_profile_data():
    """Test if profile route provides correct data"""
    try:
        from app import app
        
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = '507f1f77bcf86cd799439011'
            
            response = client.get('/profile')
            
            if response.status_code == 200:
                print("✅ Profile route works!")
                return True
            else:
                print(f"❌ Profile returned status code: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Profile test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧘 Testing Dashboard Fixes")
    print("=" * 30)
    
    success = True
    
    # Test dashboard
    if not test_dashboard_data():
        success = False
    
    # Test profile
    if not test_profile_data():
        success = False
    
    if success:
        print("\n🎉 All tests passed! The dashboard should work now.")
        print("\n💡 The app should now start without template errors.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
    
    return success

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)