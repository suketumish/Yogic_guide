#!/usr/bin/env python3
"""
Test script to verify Chart.js visualizations implementation
Tests all four required chart types:
1. Line chart for user activity timeline
2. Bar chart for module distribution
3. Pie chart for accuracy distribution
4. Gauge chart for platform health
"""

import sys
import re

def test_chartjs_cdn_included():
    """Test if Chart.js CDN is included in admin base template"""
    try:
        with open('templates/admin/base.html', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'chart.js' in content.lower():
            print("✅ Chart.js CDN is included in admin base template")
            return True
        else:
            print("❌ Chart.js CDN not found in admin base template")
            return False
    except Exception as e:
        print(f"❌ Error checking Chart.js CDN: {e}")
        return False

def test_chart_canvases_exist():
    """Test if all required chart canvas elements exist in analytics template"""
    try:
        with open('templates/admin/analytics.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_canvases = [
            'userGrowthChart',  # Line chart for user activity
            'modulePerformanceChart',  # Bar chart for module distribution
            'accuracyDistributionChart',  # Pie chart for accuracy
            'platformHealthGauge'  # Gauge chart for platform health
        ]
        
        all_found = True
        for canvas_id in required_canvases:
            if f'id="{canvas_id}"' in content:
                print(f"✅ Canvas element '{canvas_id}' found")
            else:
                print(f"❌ Canvas element '{canvas_id}' not found")
                all_found = False
        
        return all_found
    except Exception as e:
        print(f"❌ Error checking canvas elements: {e}")
        return False

def test_chart_data_structure():
    """Test if analytics data structure includes all required data for charts"""
    try:
        with open('templates/admin/analytics.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_data_keys = [
            'userGrowth',  # For line chart
            'modulePerformance',  # For bar chart
            'accuracyDistribution',  # For pie chart
            'platformHealth'  # For gauge chart
        ]
        
        all_found = True
        for data_key in required_data_keys:
            if data_key in content:
                print(f"✅ Data structure '{data_key}' found")
            else:
                print(f"❌ Data structure '{data_key}' not found")
                all_found = False
        
        return all_found
    except Exception as e:
        print(f"❌ Error checking data structure: {e}")
        return False

def test_chart_initialization():
    """Test if all four chart types are properly initialized"""
    try:
        with open('templates/admin/analytics.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for Chart.js initialization patterns
        chart_patterns = [
            (r'new Chart\(userGrowthCtx.*?type:\s*[\'"]line[\'"]', 'Line chart (User Activity)'),
            (r'new Chart\(modulePerformanceCtx.*?type:\s*[\'"]bar[\'"]', 'Bar chart (Module Distribution)'),
            (r'new Chart\(accuracyDistributionCtx.*?type:\s*[\'"]pie[\'"]', 'Pie chart (Accuracy Distribution)'),
            (r'new Chart\(platformHealthCtx.*?type:\s*[\'"]doughnut[\'"]', 'Gauge chart (Platform Health)')
        ]
        
        all_found = True
        for pattern, chart_name in chart_patterns:
            if re.search(pattern, content, re.DOTALL):
                print(f"✅ {chart_name} initialization found")
            else:
                print(f"❌ {chart_name} initialization not found")
                all_found = False
        
        return all_found
    except Exception as e:
        print(f"❌ Error checking chart initialization: {e}")
        return False

def test_backend_data_provision():
    """Test if backend provides accuracy distribution and platform health data"""
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_backend_data = [
            ('accuracy_distribution', 'Accuracy distribution data'),
            ('platform_health', 'Platform health data')
        ]
        
        all_found = True
        for data_key, description in required_backend_data:
            if f"'{data_key}'" in content or f'"{data_key}"' in content:
                print(f"✅ Backend provides {description}")
            else:
                print(f"❌ Backend missing {description}")
                all_found = False
        
        return all_found
    except Exception as e:
        print(f"❌ Error checking backend data: {e}")
        return False

def test_analytics_page_loads():
    """Test if analytics page loads successfully with new charts"""
    try:
        from app import app
        
        with app.test_client() as client:
            # Simulate admin session
            with client.session_transaction() as sess:
                sess['user_id'] = 'test_admin_id'
                sess['is_admin'] = True
            
            # Test analytics route
            response = client.get('/admin/analytics')
            
            if response.status_code == 200:
                content = response.data.decode('utf-8')
                
                # Check for chart-related content
                checks = [
                    ('accuracyDistributionChart' in content, 'Accuracy chart canvas'),
                    ('platformHealthGauge' in content, 'Platform health gauge canvas'),
                    ('Chart.js' in content or 'chart.js' in content, 'Chart.js library'),
                    ('analyticsData' in content, 'Analytics data object')
                ]
                
                all_passed = True
                for check, description in checks:
                    if check:
                        print(f"✅ {description} present in response")
                    else:
                        print(f"❌ {description} missing from response")
                        all_passed = False
                
                return all_passed
            else:
                print(f"❌ Analytics page returned status code: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Analytics page load test failed: {e}")
        return False

def test_chart_configuration():
    """Test if charts have proper configuration options"""
    try:
        with open('templates/admin/analytics.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for important chart configuration
        config_checks = [
            ('responsive: true', 'Responsive configuration'),
            ('maintainAspectRatio', 'Aspect ratio configuration'),
            ('plugins:', 'Plugin configuration'),
            ('backgroundColor', 'Color configuration'),
            ('tooltip', 'Tooltip configuration')
        ]
        
        all_found = True
        for config, description in config_checks:
            if config in content:
                print(f"✅ {description} found")
            else:
                print(f"⚠️  {description} not found (optional)")
        
        return True  # Configuration is optional but recommended
    except Exception as e:
        print(f"❌ Error checking chart configuration: {e}")
        return False

def main():
    """Run all Chart.js visualization tests"""
    print("📊 Testing Chart.js Visualizations Implementation")
    print("=" * 50)
    print("\nTask 10.4: Implement Chart.js visualizations")
    print("- Line chart for user activity timeline")
    print("- Bar chart for module distribution")
    print("- Pie chart for accuracy distribution")
    print("- Gauge chart for platform health")
    print("=" * 50)
    
    tests = [
        ("Chart.js CDN Inclusion", test_chartjs_cdn_included),
        ("Chart Canvas Elements", test_chart_canvases_exist),
        ("Chart Data Structure", test_chart_data_structure),
        ("Chart Initialization", test_chart_initialization),
        ("Backend Data Provision", test_backend_data_provision),
        ("Analytics Page Loading", test_analytics_page_loads),
        ("Chart Configuration", test_chart_configuration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing: {test_name}")
        print("-" * 50)
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    print("=" * 50)
    
    if passed == total:
        print("\n🎉 All Chart.js visualization tests passed!")
        print("\n✅ Implementation Complete:")
        print("   1. ✅ Line chart for user activity timeline")
        print("   2. ✅ Bar chart for module distribution")
        print("   3. ✅ Pie chart for accuracy distribution")
        print("   4. ✅ Gauge chart for platform health")
        print("\n💡 Next Steps:")
        print("   - Start the application: python app.py")
        print("   - Navigate to: http://localhost:5000/admin/analytics")
        print("   - Verify all charts render correctly")
        return True
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        print("   Please review the failed tests above")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
