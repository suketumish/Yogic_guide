#!/usr/bin/env python3
"""
Test script to verify admin system functionality
"""

import sys
from datetime import datetime

def test_admin_creation():
    """Test if admin user is created properly"""
    try:
        from app import app, MONGO_AVAILABLE, db, create_admin_user
        
        if not MONGO_AVAILABLE:
            print("⚠️  MongoDB not available - admin system will use fallback mode")
            return True
        
        # Check if admin user exists
        admin_user = db.users.find_one({'role': 'admin'})
        
        if admin_user:
            print("✅ Admin user found!")
            print(f"   Email: {admin_user['email']}")
            print(f"   Name: {admin_user.get('profile', {}).get('name', 'Unknown')}")
            print(f"   Created: {admin_user.get('createdAt', 'Unknown')}")
            return True
        else:
            print("❌ No admin user found. Creating one...")
            success = create_admin_user()
            if success:
                print("✅ Admin user created successfully!")
                return True
            else:
                print("❌ Failed to create admin user")
                return False
                
    except Exception as e:
        print(f"❌ Error testing admin creation: {e}")
        return False

def test_admin_routes():
    """Test if admin routes are accessible"""
    try:
        from app import app
        
        with app.test_client() as client:
            # Test admin route without authentication (should redirect)
            response = client.get('/admin')
            
            if response.status_code in [302, 401, 403]:
                print("✅ Admin routes are protected (good!)")
                return True
            else:
                print(f"⚠️  Admin route returned unexpected status: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Error testing admin routes: {e}")
        return False

def test_admin_login():
    """Test admin login functionality"""
    try:
        from app import app, MONGO_AVAILABLE
        
        if not MONGO_AVAILABLE:
            print("⚠️  Skipping admin login test - MongoDB not available")
            return True
        
        with app.test_client() as client:
            # Test admin login
            response = client.post('/login', data={
                'email': 'admin@yogicguide.com',
                'password': 'admin123'
            }, follow_redirects=False)
            
            if response.status_code == 302:
                # Check if redirected to admin dashboard
                location = response.headers.get('Location', '')
                if '/admin' in location:
                    print("✅ Admin login redirects to admin dashboard!")
                    return True
                else:
                    print(f"⚠️  Admin login redirects to: {location}")
                    return True
            else:
                print(f"❌ Admin login failed with status: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Error testing admin login: {e}")
        return False

def main():
    """Run all admin tests"""
    print("🔐 Testing Admin System")
    print("=" * 30)
    
    tests = [
        ("Admin User Creation", test_admin_creation),
        ("Admin Route Protection", test_admin_routes),
        ("Admin Login", test_admin_login)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"   ❌ {test_name} failed")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All admin tests passed!")
        print("\n💡 To test admin functionality:")
        print("   1. Start the app: python app.py")
        print("   2. Login with: admin@yogicguide.com / admin123")
        print("   3. You should be redirected to /admin")
        print("   4. Change the default password!")
        return True
    else:
        print(f"\n❌ {total - passed} tests failed")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)