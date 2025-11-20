#!/usr/bin/env python3
"""
Verification script for task 8.3: Extract inline CSS to external stylesheet
Checks that all CSS and JS have been properly extracted to external files
"""

import os
import re

def check_file_exists(filepath):
    """Check if a file exists and return its size"""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        return True, size
    return False, 0

def check_template_for_inline_styles(template_path):
    """Check if template has any inline styles or scripts"""
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for inline <style> tags
    inline_style_tags = re.findall(r'<style[^>]*>.*?</style>', content, re.DOTALL)
    
    # Check for inline style attributes (excluding those in comments)
    inline_style_attrs = re.findall(r'style\s*=\s*["\'][^"\']+["\']', content)
    
    # Check for inline <script> tags (excluding external script references)
    inline_script_tags = re.findall(r'<script(?![^>]*src=)[^>]*>.*?</script>', content, re.DOTALL)
    
    return {
        'inline_style_tags': len(inline_style_tags),
        'inline_style_attrs': len(inline_style_attrs),
        'inline_script_tags': len(inline_script_tags)
    }

def main():
    print("=" * 70)
    print("Task 8.3 Verification: Extract inline CSS to external stylesheet")
    print("=" * 70)
    print()
    
    # Check external CSS file
    css_path = 'static/css/module-surya-namaskar.css'
    css_exists, css_size = check_file_exists(css_path)
    print(f"✓ CSS File: {css_path}")
    print(f"  - Exists: {'YES' if css_exists else 'NO'}")
    if css_exists:
        print(f"  - Size: {css_size:,} bytes ({css_size/1024:.2f} KB)")
    print()
    
    # Check external JS file
    js_path = 'static/js/module-surya-namaskar.js'
    js_exists, js_size = check_file_exists(js_path)
    print(f"✓ JS File: {js_path}")
    print(f"  - Exists: {'YES' if js_exists else 'NO'}")
    if js_exists:
        print(f"  - Size: {js_size:,} bytes ({js_size/1024:.2f} KB)")
    print()
    
    # Check template for inline styles
    template_path = 'templates/module_surya_namaskar.html'
    template_exists, template_size = check_file_exists(template_path)
    print(f"✓ Template: {template_path}")
    print(f"  - Exists: {'YES' if template_exists else 'NO'}")
    if template_exists:
        print(f"  - Size: {template_size:,} bytes ({template_size/1024:.2f} KB)")
        
        inline_check = check_template_for_inline_styles(template_path)
        print(f"  - Inline <style> tags: {inline_check['inline_style_tags']}")
        print(f"  - Inline style attributes: {inline_check['inline_style_attrs']}")
        print(f"  - Inline <script> tags: {inline_check['inline_script_tags']}")
    print()
    
    # Check if template links to external files
    if template_exists:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        css_linked = 'module-surya-namaskar.css' in template_content
        js_linked = 'module-surya-namaskar.js' in template_content
        
        print("✓ External File Links:")
        print(f"  - CSS linked: {'YES' if css_linked else 'NO'}")
        print(f"  - JS linked: {'YES' if js_linked else 'NO'}")
        print()
    
    # Summary
    print("=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    all_checks_passed = (
        css_exists and 
        js_exists and 
        template_exists and
        inline_check['inline_style_tags'] == 0 and
        inline_check['inline_style_attrs'] == 0 and
        inline_check['inline_script_tags'] == 0 and
        css_linked and
        js_linked
    )
    
    if all_checks_passed:
        print("✅ ALL CHECKS PASSED!")
        print()
        print("Task 8.3 Requirements Met:")
        print("  ✓ Dedicated CSS file created")
        print("  ✓ All inline styles moved to external file")
        print("  ✓ Stylesheet linked in template")
        print("  ✓ Browser caching enabled (external files are cacheable)")
        print()
        print(f"Total external assets size: {(css_size + js_size)/1024:.2f} KB")
        print("This enables efficient browser caching and improved performance.")
    else:
        print("❌ SOME CHECKS FAILED")
        if not css_exists:
            print("  ✗ CSS file not found")
        if not js_exists:
            print("  ✗ JS file not found")
        if inline_check['inline_style_tags'] > 0:
            print(f"  ✗ Found {inline_check['inline_style_tags']} inline <style> tags")
        if inline_check['inline_style_attrs'] > 0:
            print(f"  ✗ Found {inline_check['inline_style_attrs']} inline style attributes")
        if inline_check['inline_script_tags'] > 0:
            print(f"  ✗ Found {inline_check['inline_script_tags']} inline <script> tags")
        if not css_linked:
            print("  ✗ CSS file not linked in template")
        if not js_linked:
            print("  ✗ JS file not linked in template")
    
    print("=" * 70)
    
    return 0 if all_checks_passed else 1

if __name__ == '__main__':
    exit(main())
