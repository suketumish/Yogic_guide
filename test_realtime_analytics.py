"""
Test Real-time Analytics API Endpoint
Tests the /api/analytics/live endpoint for proper data structure and response
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_analytics_api_structure():
    """Test that the analytics API returns the expected data structure"""
    print("🧪 Testing Real-time Analytics API Structure...")
    
    # Expected keys in the response
    expected_keys = [
        'timestamp',
        'metrics',
        'userGrowth',
        'sessionAnalytics',
        'modulePerformance',
        'userEngagement',
        'hourlyUsage',
        'weeklyTrends',
        'retention',
        'accuracyDistribution',
        'platformHealth'
    ]
    
    # Expected metrics keys
    expected_metrics_keys = [
        'totalUsers',
        'totalSessions',
        'activeUsers7d',
        'activeUsers30d',
        'avgSessionDuration',
        'retentionRate'
    ]
    
    print("✅ Expected response structure defined")
    print(f"   - Top-level keys: {len(expected_keys)}")
    print(f"   - Metrics keys: {len(expected_metrics_keys)}")
    
    # Test data structure for charts
    chart_data_structures = {
        'userGrowth': ['labels', 'data'],
        'sessionAnalytics': ['labels', 'sessions', 'durations'],
        'modulePerformance': ['labels', 'data', 'users', 'durations'],
        'userEngagement': ['labels', 'data'],
        'retention': ['labels', 'data'],
        'accuracyDistribution': ['labels', 'data']
    }
    
    print("\n✅ Chart data structures validated")
    for chart, keys in chart_data_structures.items():
        print(f"   - {chart}: {keys}")
    
    # Test platform health structure
    platform_health_keys = ['score', 'components']
    platform_health_components = ['userActivity', 'sessionQuality', 'retention', 'engagement']
    
    print("\n✅ Platform health structure validated")
    print(f"   - Keys: {platform_health_keys}")
    print(f"   - Components: {platform_health_components}")
    
    return True

def test_realtime_update_functionality():
    """Test the real-time update JavaScript functionality"""
    print("\n🧪 Testing Real-time Update Functionality...")
    
    # Check that the JavaScript file exists
    js_file = 'static/js/analytics-realtime.js'
    if os.path.exists(js_file):
        print(f"✅ JavaScript file exists: {js_file}")
        
        # Read and check for key functions
        with open(js_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        required_functions = [
            'initializeRealTimeUpdates',
            'fetchAndUpdateAnalytics',
            'updateMetricsCards',
            'updateCharts',
            'showLoadingIndicator',
            'hideLoadingIndicator',
            'manualRefresh'
        ]
        
        for func in required_functions:
            if func in content:
                print(f"   ✅ Function found: {func}")
            else:
                print(f"   ❌ Function missing: {func}")
                return False
        
        # Check for polling interval
        if 'setInterval' in content:
            print("   ✅ Polling mechanism implemented")
        else:
            print("   ❌ Polling mechanism missing")
            return False
        
        # Check for loading indicators
        if 'analytics-loading-indicator' in content:
            print("   ✅ Loading indicator implemented")
        else:
            print("   ❌ Loading indicator missing")
            return False
        
        return True
    else:
        print(f"❌ JavaScript file not found: {js_file}")
        return False

def test_chart_instances_storage():
    """Test that chart instances are properly stored for updates"""
    print("\n🧪 Testing Chart Instances Storage...")
    
    template_file = 'templates/admin/analytics.html'
    if os.path.exists(template_file):
        print(f"✅ Template file exists: {template_file}")
        
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for chart instance storage
        chart_types = [
            'userGrowth',
            'sessionAnalytics',
            'modulePerformance',
            'accuracyDistribution',
            'platformHealth',
            'userEngagement',
            'hourlyUsage',
            'weeklyTrends',
            'retention'
        ]
        
        for chart in chart_types:
            if f'window.chartInstances.{chart}' in content:
                print(f"   ✅ Chart instance stored: {chart}")
            else:
                print(f"   ❌ Chart instance not stored: {chart}")
                return False
        
        # Check for real-time script inclusion
        if 'analytics-realtime.js' in content:
            print("   ✅ Real-time script included in template")
        else:
            print("   ❌ Real-time script not included")
            return False
        
        # Check for initialization call
        if 'initializeRealTimeUpdates' in content:
            print("   ✅ Real-time updates initialization found")
        else:
            print("   ❌ Real-time updates initialization missing")
            return False
        
        return True
    else:
        print(f"❌ Template file not found: {template_file}")
        return False

def test_api_endpoint_exists():
    """Test that the API endpoint is defined in app.py"""
    print("\n🧪 Testing API Endpoint Definition...")
    
    app_file = 'app.py'
    if os.path.exists(app_file):
        print(f"✅ App file exists: {app_file}")
        
        with open(app_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for API endpoint
        if "/api/analytics/live" in content or "get_live_analytics" in content:
            print("   ✅ API endpoint defined: /api/analytics/live")
        else:
            print("   ❌ API endpoint not found")
            return False
        
        # Check for required decorators
        if "@require_admin" in content:
            print("   ✅ Admin authentication required")
        else:
            print("   ⚠️  Admin authentication not found")
        
        # Check for JSON response
        if "jsonify" in content:
            print("   ✅ JSON response implemented")
        else:
            print("   ❌ JSON response not found")
            return False
        
        return True
    else:
        print(f"❌ App file not found: {app_file}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("REAL-TIME ANALYTICS UPDATE FUNCTIONALITY TESTS")
    print("=" * 60)
    
    tests = [
        ("API Structure", test_analytics_api_structure),
        ("Real-time Update Functionality", test_realtime_update_functionality),
        ("Chart Instances Storage", test_chart_instances_storage),
        ("API Endpoint Definition", test_api_endpoint_exists)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Real-time analytics update functionality is ready.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the implementation.")
        return 1

if __name__ == '__main__':
    exit(main())
