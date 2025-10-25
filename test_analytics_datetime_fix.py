#!/usr/bin/env python3
"""
Test script to verify analytics datetime fix
"""

import sys

def test_analytics_route():
    """Test if analytics route works without datetime errors"""
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
                print("✅ Analytics route works without datetime errors!")
                print(f"✅ Response length: {len(response.data)} bytes")
                
                # Check if the response contains expected content
                content = response.data.decode('utf-8')
                if 'Analytics Dashboard' in content:
                    print("✅ Analytics dashboard content loaded")
                if 'Chart.js' in content:
                    print("✅ Chart.js library included")
                if 'userGrowthChart' in content:
                    print("✅ Chart elements found")
                
                return True
            else:
                print(f"❌ Analytics route returned status code: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Analytics route test failed: {e}")
        return False

def test_datetime_import():
    """Test if datetime imports work correctly"""
    try:
        from app import datetime, timedelta
        print("✅ Datetime imports work correctly")
        
        # Test datetime usage
        now = datetime.now()
        past = now - timedelta(days=30)
        print(f"✅ Datetime operations work: {now.strftime('%Y-%m-%d')}")
        
        return True
    except Exception as e:
        print(f"❌ Datetime import test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🕐 Testing Analytics Datetime Fix")
    print("=" * 35)
    
    tests = [
        ("Datetime Import", test_datetime_import),
        ("Analytics Route", test_analytics_route)
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
        print("\n🎉 All datetime tests passed!")
        print("\n💡 Analytics should work correctly now!")
        print("\n🔗 Test it: http://localhost:5000/admin/analytics")
        return True
    else:
        print(f"\n❌ {total - passed} tests failed")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)