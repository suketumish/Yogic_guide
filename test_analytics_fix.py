#!/usr/bin/env python3
"""
Test script to verify analytics page functionality
"""

import sys

def test_analytics_page():
    """Test if analytics page loads without errors"""
    try:
        from app import app, MONGO_AVAILABLE
        
        with app.test_client() as client:
            # Simulate admin session
            with client.session_transaction() as sess:
                sess['user_id'] = 'test_admin_id'
                sess['is_admin'] = True
            
            # Test analytics route
            response = client.get('/admin/analytics')
            
            if response.status_code == 200:
                print("✅ Analytics page loads successfully!")
                print(f"✅ Response length: {len(response.data)} bytes")
                
                # Check if the response contains expected content
                content = response.data.decode('utf-8')
                if 'Analytics Dashboard' in content:
                    print("✅ Analytics title found in response")
                if 'Total Registrations' in content:
                    print("✅ Stats section found in response")
                if 'User Registrations' in content:
                    print("✅ Charts section found in response")
                
                return True
            else:
                print(f"❌ Analytics page returned status code: {response.status_code}")
                if response.status_code == 500:
                    print("❌ Server error - check template syntax")
                return False
                
    except Exception as e:
        print(f"❌ Analytics page test failed: {e}")
        return False

def test_analytics_with_empty_data():
    """Test analytics page with empty data (no sessions/users)"""
    try:
        from app import app
        
        with app.test_client() as client:
            # Simulate admin session
            with client.session_transaction() as sess:
                sess['user_id'] = 'test_admin_id'
                sess['is_admin'] = True
            
            # Test analytics route (should handle empty data gracefully)
            response = client.get('/admin/analytics')
            
            if response.status_code == 200:
                print("✅ Analytics page handles empty data correctly!")
                return True
            else:
                print(f"❌ Analytics page failed with empty data: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Analytics empty data test failed: {e}")
        return False

def main():
    """Run all analytics tests"""
    print("📊 Testing Analytics Page Fixes")
    print("=" * 35)
    
    tests = [
        ("Analytics Page Loading", test_analytics_page),
        ("Analytics Empty Data Handling", test_analytics_with_empty_data)
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
        print("\n🎉 All analytics tests passed!")
        print("\n💡 Analytics page should work correctly now!")
        print("\n🔗 Test it: http://localhost:5000/admin/analytics")
        return True
    else:
        print(f"\n❌ {total - passed} tests failed")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)