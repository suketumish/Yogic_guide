"""
Parse Lighthouse JSON results and display key metrics
"""

import json
import sys

def parse_lighthouse_results(json_file):
    """Parse and display Lighthouse results"""
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        categories = data.get('categories', {})
        
        print("\n" + "="*60)
        print("LIGHTHOUSE AUDIT RESULTS - SURYA NAMASKAR MODULE")
        print("="*60)
        
        # Check for warnings
        warnings = data.get('runWarnings', [])
        if warnings:
            print("\n⚠️  WARNINGS:")
            for warning in warnings:
                print(f"  {warning}")
        
        results = {}
        
        # Performance
        if 'performance' in categories:
            score = categories['performance']['score'] * 100
            results['performance'] = score
            status = "✓ PASS" if score >= 90 else "✗ FAIL"
            print(f"\n📊 Performance: {score:.0f}/100 {status}")
        
        # Accessibility
        if 'accessibility' in categories:
            score = categories['accessibility']['score'] * 100
            results['accessibility'] = score
            status = "✓ PASS" if score >= 90 else "✗ FAIL"
            print(f"♿ Accessibility: {score:.0f}/100 {status}")
        
        # Best Practices
        if 'best-practices' in categories:
            score = categories['best-practices']['score'] * 100
            results['best-practices'] = score
            status = "✓ PASS" if score >= 90 else "✗ FAIL"
            print(f"✨ Best Practices: {score:.0f}/100 {status}")
        
        # Performance metrics
        if 'performance' in categories:
            audits = data.get('audits', {})
            print("\n" + "-"*60)
            print("KEY PERFORMANCE METRICS")
            print("-"*60)
            
            metrics = {
                'first-contentful-paint': 'First Contentful Paint',
                'largest-contentful-paint': 'Largest Contentful Paint',
                'total-blocking-time': 'Total Blocking Time',
                'cumulative-layout-shift': 'Cumulative Layout Shift',
                'speed-index': 'Speed Index',
            }
            
            for key, name in metrics.items():
                if key in audits:
                    display_value = audits[key].get('displayValue', 'N/A')
                    print(f"  {name}: {display_value}")
        
        print("\n" + "="*60)
        
        # Check if performance target is met
        if results.get('performance', 0) >= 90:
            print("\n✓ SUCCESS: Performance score meets the 90+ target!")
        else:
            print(f"\n✗ ATTENTION: Performance score ({results.get('performance', 0):.0f}) is below 90")
            print("\n  Recommendations:")
            print("  - The page redirected to login (authentication required)")
            print("  - Test with authenticated session for accurate results")
            print("  - Consider optimizing images, CSS, and JavaScript")
        
        print("="*60 + "\n")
        
        return results
        
    except Exception as e:
        print(f"✗ Error parsing results: {e}")
        return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python parse_lighthouse_results.py <json_file>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    results = parse_lighthouse_results(json_file)
    
    if results and results.get('performance', 0) >= 90:
        sys.exit(0)
    else:
        sys.exit(1)
