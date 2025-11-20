"""
Verify performance optimizations for Surya Namaskar module.
Checks CSS and JavaScript optimization without requiring Selenium.
"""

import re
import os


def analyze_file_size(filepath):
    """Get file size in bytes."""
    if os.path.exists(filepath):
        return os.path.getsize(filepath)
    return 0


def count_lines(filepath):
    """Count lines in a file."""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    return 0


def analyze_css_optimization(filepath):
    """Analyze CSS optimization in the template."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find CSS block
    css_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    if not css_match:
        return None
    
    css_content = css_match.group(1)
    
    # Count CSS size
    css_size = len(css_content.encode('utf-8'))
    
    # Check for minification indicators
    has_minification = (
        '\n' not in css_content.strip()[:100] or  # First 100 chars should be on one line
        css_content.count('\n') < 50  # Should have fewer line breaks
    )
    
    # Count media queries
    media_queries = len(re.findall(r'@media', css_content))
    
    # Check for important optimizations
    has_responsive = '@media' in css_content
    has_hover_optimization = '@media(min-width:1025px)' in css_content or '@media (min-width: 1025px)' in css_content
    
    return {
        'size_bytes': css_size,
        'size_kb': css_size / 1024,
        'is_minified': has_minification,
        'media_queries': media_queries,
        'has_responsive': has_responsive,
        'has_hover_optimization': has_hover_optimization
    }


def analyze_js_optimization(filepath):
    """Analyze JavaScript optimization in the template."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find JS block
    js_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    if not js_match:
        return None
    
    js_content = js_match.group(1)
    
    # Count JS size
    js_size = len(js_content.encode('utf-8'))
    
    # Check for minification/optimization
    has_iife = '(function()' in js_content or '(function (' in js_content
    has_short_vars = bool(re.search(r'\bconst [A-Z]\b', js_content))  # Single letter constants
    
    # Check for performance monitoring
    has_performance_api = 'performance' in js_content.lower()
    has_image_tracking = 'img' in js_content.lower() or 'image' in js_content.lower()
    
    # Count function definitions (should be minimal)
    function_count = len(re.findall(r'function\s+\w+', js_content))
    
    return {
        'size_bytes': js_size,
        'size_kb': js_size / 1024,
        'uses_iife': has_iife,
        'uses_short_vars': has_short_vars,
        'has_performance_monitoring': has_performance_api,
        'has_image_tracking': has_image_tracking,
        'function_count': function_count
    }


def analyze_image_loading(filepath):
    """Analyze image loading strategy."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count images
    img_tags = re.findall(r'<img[^>]+>', content)
    total_images = len(img_tags)
    
    # Check loading attributes
    eager_loading = len(re.findall(r'loading=["\']eager["\']', content))
    lazy_loading = len(re.findall(r'loading=["\']lazy["\']', content))
    
    # Check for error handling
    has_error_handler = 'error' in content and 'data-retry' in content
    has_fallback = 'fallback' in content.lower() or 'removebg-preview' in content
    
    return {
        'total_images': total_images,
        'eager_loading': eager_loading,
        'lazy_loading': lazy_loading,
        'has_error_handler': has_error_handler,
        'has_fallback': has_fallback
    }


def main():
    """Run performance optimization verification."""
    template_path = 'templates/module_surya_namaskar.html'
    
    print("="*70)
    print("PERFORMANCE OPTIMIZATION VERIFICATION")
    print("Surya Namaskar Module - Task 13.1 & 13.2")
    print("="*70)
    print()
    
    # File size analysis
    file_size = analyze_file_size(template_path)
    line_count = count_lines(template_path)
    
    print("📄 FILE METRICS")
    print(f"   File size: {file_size:,} bytes ({file_size/1024:.2f} KB)")
    print(f"   Line count: {line_count}")
    print()
    
    # CSS analysis
    print("🎨 CSS OPTIMIZATION")
    css_stats = analyze_css_optimization(template_path)
    if css_stats:
        print(f"   CSS size: {css_stats['size_bytes']:,} bytes ({css_stats['size_kb']:.2f} KB)")
        print(f"   Minified: {'✓ YES' if css_stats['is_minified'] else '✗ NO'}")
        print(f"   Media queries: {css_stats['media_queries']}")
        print(f"   Responsive design: {'✓ YES' if css_stats['has_responsive'] else '✗ NO'}")
        print(f"   Hover optimization: {'✓ YES' if css_stats['has_hover_optimization'] else '✗ NO'}")
        
        # Evaluation
        if css_stats['is_minified'] and css_stats['size_kb'] < 5:
            print("   Status: ✓ OPTIMIZED - CSS is minified and compact")
        elif css_stats['size_kb'] < 10:
            print("   Status: ⚠ ACCEPTABLE - CSS could be further optimized")
        else:
            print("   Status: ✗ NEEDS WORK - CSS is too large")
    print()
    
    # JavaScript analysis
    print("⚡ JAVASCRIPT OPTIMIZATION")
    js_stats = analyze_js_optimization(template_path)
    if js_stats:
        print(f"   JS size: {js_stats['size_bytes']:,} bytes ({js_stats['size_kb']:.2f} KB)")
        print(f"   Uses IIFE: {'✓ YES' if js_stats['uses_iife'] else '✗ NO'}")
        print(f"   Short variables: {'✓ YES' if js_stats['uses_short_vars'] else '✗ NO'}")
        print(f"   Performance monitoring: {'✓ YES' if js_stats['has_performance_monitoring'] else '✗ NO'}")
        print(f"   Image tracking: {'✓ YES' if js_stats['has_image_tracking'] else '✗ NO'}")
        print(f"   Function count: {js_stats['function_count']}")
        
        # Evaluation
        if js_stats['uses_iife'] and js_stats['size_kb'] < 5:
            print("   Status: ✓ OPTIMIZED - JavaScript is compact and efficient")
        elif js_stats['size_kb'] < 10:
            print("   Status: ⚠ ACCEPTABLE - JavaScript could be further optimized")
        else:
            print("   Status: ✗ NEEDS WORK - JavaScript is too large")
    print()
    
    # Image loading analysis
    print("🖼️  IMAGE LOADING STRATEGY")
    img_stats = analyze_image_loading(template_path)
    print(f"   Total images: {img_stats['total_images']}")
    print(f"   Eager loading: {img_stats['eager_loading']}")
    print(f"   Lazy loading: {img_stats['lazy_loading']}")
    print(f"   Error handling: {'✓ YES' if img_stats['has_error_handler'] else '✗ NO'}")
    print(f"   Fallback mechanism: {'✓ YES' if img_stats['has_fallback'] else '✗ NO'}")
    
    if img_stats['has_error_handler'] and img_stats['has_fallback']:
        print("   Status: ✓ OPTIMIZED - Proper error handling and fallbacks")
    else:
        print("   Status: ⚠ NEEDS IMPROVEMENT - Missing error handling or fallbacks")
    print()
    
    # Overall assessment
    print("="*70)
    print("OVERALL ASSESSMENT")
    print("="*70)
    
    optimizations = []
    issues = []
    
    # Check CSS
    if css_stats and css_stats['is_minified'] and css_stats['size_kb'] < 5:
        optimizations.append("✓ CSS is minified and optimized")
    elif css_stats:
        issues.append("⚠ CSS could be further minified")
    
    # Check JS
    if js_stats and js_stats['uses_iife'] and js_stats['size_kb'] < 5:
        optimizations.append("✓ JavaScript is optimized with IIFE")
    elif js_stats:
        issues.append("⚠ JavaScript could be further optimized")
    
    # Check images
    if img_stats['has_error_handler'] and img_stats['has_fallback']:
        optimizations.append("✓ Image loading is optimized with error handling")
    else:
        issues.append("⚠ Image loading needs better error handling")
    
    # Check performance monitoring
    if js_stats and js_stats['has_performance_monitoring']:
        optimizations.append("✓ Performance monitoring is implemented")
    
    print()
    print("OPTIMIZATIONS COMPLETED:")
    for opt in optimizations:
        print(f"  {opt}")
    
    if issues:
        print()
        print("AREAS FOR IMPROVEMENT:")
        for issue in issues:
            print(f"  {issue}")
    
    print()
    print("="*70)
    print("REQUIREMENTS VERIFICATION")
    print("="*70)
    print()
    print("Requirement 8.1 - Page loads within 2 seconds:")
    print("  ⚠ Requires live testing with browser (see test_surya_namaskar_performance.py)")
    print()
    print("Requirement 8.2 - Minimize CSS file size:")
    if css_stats and css_stats['is_minified']:
        print(f"  ✓ PASS - CSS is minified ({css_stats['size_kb']:.2f} KB)")
    else:
        print("  ✗ FAIL - CSS is not minified")
    print()
    print("Requirement 8.3 - Reduce JavaScript execution time:")
    if js_stats and js_stats['uses_iife'] and js_stats['function_count'] < 5:
        print(f"  ✓ PASS - JavaScript is optimized (IIFE, {js_stats['function_count']} functions)")
    else:
        print("  ⚠ PARTIAL - JavaScript could be further optimized")
    print()
    print("Requirement 8.4 - Optimize image loading strategy:")
    if img_stats['has_error_handler'] and img_stats['has_fallback']:
        print("  ✓ PASS - Image loading has error handling and fallbacks")
    else:
        print("  ✗ FAIL - Image loading needs improvement")
    print()
    print("Requirement 8.5 - Performance metrics:")
    if js_stats and js_stats['has_performance_monitoring']:
        print("  ✓ PASS - Performance monitoring is implemented")
    else:
        print("  ✗ FAIL - Performance monitoring is missing")
    print()
    print("="*70)
    print()
    
    # Summary
    total_checks = 5
    passed_checks = sum([
        css_stats and css_stats['is_minified'],
        js_stats and js_stats['uses_iife'] and js_stats['function_count'] < 5,
        img_stats['has_error_handler'] and img_stats['has_fallback'],
        js_stats and js_stats['has_performance_monitoring'],
    ])
    
    print(f"SUMMARY: {passed_checks}/{total_checks-1} optimization checks passed")
    print("(Live performance testing requires browser - use test_surya_namaskar_performance.py)")
    print()
    
    return passed_checks >= 3


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
