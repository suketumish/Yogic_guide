#!/usr/bin/env python3
"""
Test script to verify admin dashboard functionality
"""

import sys
from datetime import datetime

def test_admin_dashboard():
    """Test if admin dashboard loads without errors"""
    try:
        from app import app, MONGO_AVAILABLE
        
        with app.test_client() as client:
            # Simulate admin session
            with client.session_transaction() as sess:
                sess['user_id'] = 'test_admin_id'
                sess['is_admin'] = True
            
            # Test admin dashboard route
            response = client.get('/admin')
            
            if response.status_code == 200:
                print("✅ Admin dashboard loads successfully!")
                print(f"✅ Response length: {len(response.data)} bytes")
                
                # Check if the response contains expected content
                content = response.data.decode('utf-8')
                if 'Admin Dashboard' in content:
                    print("✅ Dashboard title found in response")
                if 'Total Users' in content:
                    print("✅ Stats section found in response")
                if 'Recent Users' in content:
                    print("✅ Recent users section found in response")
                
                return True
            else:
                print(f"❌ Admin dashboard returned status code: {response.status_code}")
                if response.status_code == 500:
                    print("❌ Server error - check template syntax")
                return False
                
    except Exception as e:
        print(f"❌ Admin dashboard test failed: {e}")
        return False

def test_admin_routes():
    """Test if all admin routes are accessible"""
    try:
        from app import app
        
        admin_routes = [
            '/admin',
            '/admin/users', 
            '/admin/sessions',
            '/admin/analytics',
            '/admin/settings'
        ]
        
        with app.test_client() as client:
            # Simulate admin session
            with client.session_transaction() as sess:
                sess['user_id'] = 'test_admin_id'
                sess['is_admin'] = True
            
            results = {}
            for route in admin_routes:
                try:
                    response = client.get(route)
                    results[route] = response.status_code
                    if response.status_code == 200:
                        print(f"✅ {route} - OK")
                    else:
                        print(f"❌ {route} - Status {response.status_code}")
                except Exception as e:
                    results[route] = f"Error: {e}"
                    print(f"❌ {route} - Error: {e}")
            
            success_count = sum(1 for status in results.values() if status == 200)
            total_count = len(admin_routes)
            
            print(f"\n📊 Results: {success_count}/{total_count} routes working")
            return success_count == total_count
                
    except Exception as e:
        print(f"❌ Admin routes test failed: {e}")
        return False

def main():
    """Run all admin dashboard tests"""
    print("🔐 Testing Admin Dashboard")
    print("=" * 30)
    
    tests = [
        ("Admin Dashboard Loading", test_admin_dashboard),
        ("Admin Routes Accessibility", test_admin_routes)
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
        print("\n🎉 All admin dashboard tests passed!")
        print("\n💡 Admin dashboard should work correctly now!")
        return True
    else:
        print(f"\n❌ {total - passed} tests failed")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)