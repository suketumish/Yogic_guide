"""
Lighthouse Audit Runner for Surya Namaskar Module Page

This script runs Lighthouse audits for performance, accessibility, and best practices
on the Surya Namaskar module page.

Requirements:
- Flask app must be running (python app.py)
- Node.js and Lighthouse CLI must be installed (npm install -g lighthouse)
"""

import subprocess
import json
import os
import sys
from datetime import datetime

def check_lighthouse_installed():
    """Check if Lighthouse CLI is installed"""
    try:
        result = subprocess.run(
            ['lighthouse', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✓ Lighthouse CLI found: {result.stdout.strip()}")
            return True
        return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def check_server_running(url):
    """Check if the Flask server is running"""
    try:
        import requests
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✓ Server is running at {url}")
            return True
        return False
    except Exception as e:
        print(f"✗ Server not accessible at {url}: {e}")
        return False

def run_lighthouse_audit(url, output_dir='lighthouse_reports'):
    """Run Lighthouse audit and save results"""
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(output_dir, f'lighthouse_report_{timestamp}.json')
    html_file = os.path.join(output_dir, f'lighthouse_report_{timestamp}.html')
    
    print(f"\n🔍 Running Lighthouse audit on {url}...")
    print("This may take 30-60 seconds...\n")
    
    # Run Lighthouse with all categories
    cmd = [
        'lighthouse',
        url,
        '--output=json',
        '--output=html',
        '--output-path=' + output_file.replace('.json', ''),
        '--chrome-flags="--headless"',
        '--only-categories=performance,accessibility,best-practices'
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode != 0:
            print(f"✗ Lighthouse failed: {result.stderr}")
            return None
        
        print(f"✓ Lighthouse audit completed!")
        print(f"  JSON report: {output_file}")
        print(f"  HTML report: {html_file}")
        
        return output_file
        
    except subprocess.TimeoutExpired:
        print("✗ Lighthouse audit timed out")
        return None
    except Exception as e:
        print(f"✗ Error running Lighthouse: {e}")
        return None

def parse_lighthouse_results(json_file):
    """Parse and display Lighthouse results"""
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        categories = data.get('categories', {})
        
        print("\n" + "="*60)
        print("LIGHTHOUSE AUDIT RESULTS")
        print("="*60)
        
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
                'first-contentful-paint': ('First Contentful Paint', 'ms'),
                'largest-contentful-paint': ('Largest Contentful Paint', 'ms'),
                'total-blocking-time': ('Total Blocking Time', 'ms'),
                'cumulative-layout-shift': ('Cumulative Layout Shift', ''),
                'speed-index': ('Speed Index', 'ms'),
            }
            
            for key, (name, unit) in metrics.items():
                if key in audits:
                    value = audits[key].get('numericValue', 0)
                    display_value = audits[key].get('displayValue', '')
                    print(f"  {name}: {display_value}")
        
        print("\n" + "="*60)
        
        # Check if performance target is met
        if results.get('performance', 0) >= 90:
            print("\n✓ SUCCESS: Performance score meets the 90+ target!")
        else:
            print(f"\n✗ ATTENTION: Performance score ({results.get('performance', 0):.0f}) is below 90")
            print("  Consider optimizing images, CSS, and JavaScript")
        
        print("="*60 + "\n")
        
        return results
        
    except Exception as e:
        print(f"✗ Error parsing results: {e}")
        return None

def main():
    """Main execution function"""
    
    # Configuration
    url = 'http://127.0.0.1:5000/module/surya-namaskar'
    
    print("="*60)
    print("LIGHTHOUSE AUDIT FOR SURYA NAMASKAR MODULE")
    print("="*60)
    
    # Check prerequisites
    print("\n1. Checking prerequisites...")
    
    if not check_lighthouse_installed():
        print("\n✗ Lighthouse CLI is not installed")
        print("\nTo install Lighthouse:")
        print("  npm install -g lighthouse")
        print("\nOr use npx (no installation needed):")
        print(f"  npx lighthouse {url} --view")
        return 1
    
    # Check if requests is available
    try:
        import requests
    except ImportError:
        print("\n✗ 'requests' library not found")
        print("  Install with: pip install requests")
        return 1
    
    if not check_server_running(url):
        print("\n✗ Flask server is not running")
        print("\nPlease start the server first:")
        print("  python app.py")
        print("\nThen run this script again.")
        return 1
    
    # Run audit
    print("\n2. Running Lighthouse audit...")
    output_file = run_lighthouse_audit(url)
    
    if not output_file:
        print("\n✗ Audit failed")
        return 1
    
    # Parse results
    print("\n3. Parsing results...")
    results = parse_lighthouse_results(output_file)
    
    if results:
        return 0 if results.get('performance', 0) >= 90 else 1
    
    return 1

if __name__ == '__main__':
    sys.exit(main())
