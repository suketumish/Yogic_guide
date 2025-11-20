"""
Color Contrast Verification Script for Surya Namaskar Module
Verifies WCAG 2.1 AA compliance for color contrast ratios
"""

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def relative_luminance(rgb):
    """Calculate relative luminance of an RGB color"""
    r, g, b = [x / 255.0 for x in rgb]
    
    # Apply gamma correction
    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
    
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast_ratio(color1, color2):
    """Calculate contrast ratio between two colors"""
    lum1 = relative_luminance(hex_to_rgb(color1))
    lum2 = relative_luminance(hex_to_rgb(color2))
    
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    
    return (lighter + 0.05) / (darker + 0.05)

def check_wcag_compliance(ratio, level='AA', size='normal'):
    """Check if contrast ratio meets WCAG standards"""
    if level == 'AA':
        if size == 'large':
            return ratio >= 3.0
        else:
            return ratio >= 4.5
    elif level == 'AAA':
        if size == 'large':
            return ratio >= 4.5
        else:
            return ratio >= 7.0
    return False

# Define color combinations used in Surya Namaskar module
color_tests = [
    # Header section
    {
        'name': 'Header title gradient (approximated as purple)',
        'foreground': '#667eea',  # Approximation of gradient
        'background': '#ffffff',
        'size': 'large',
        'element': 'h1.text-gradient'
    },
    {
        'name': 'Header subtitle',
        'foreground': '#475569',  # slate-600
        'background': '#ffffff',
        'size': 'normal',
        'element': 'p.text-slate-600'
    },
    
    # Statistics cards
    {
        'name': 'Orange stat value',
        'foreground': '#ea580c',  # orange-600
        'background': '#fff7ed',  # orange-50
        'size': 'large',
        'element': '.text-orange-600 on .bg-orange-50'
    },
    {
        'name': 'Red stat value',
        'foreground': '#dc2626',  # red-600
        'background': '#fef2f2',  # red-50
        'size': 'large',
        'element': '.text-red-600 on .bg-red-50'
    },
    {
        'name': 'Yellow stat value',
        'foreground': '#ca8a04',  # yellow-600
        'background': '#fefce8',  # yellow-50
        'size': 'large',
        'element': '.text-yellow-600 on .bg-yellow-50'
    },
    {
        'name': 'Amber stat value',
        'foreground': '#d97706',  # amber-600
        'background': '#fffbeb',  # amber-50
        'size': 'large',
        'element': '.text-amber-600 on .bg-amber-50'
    },
    {
        'name': 'Stat label',
        'foreground': '#4b5563',  # gray-600
        'background': '#fff7ed',  # orange-50 (worst case)
        'size': 'normal',
        'element': '.text-gray-600 on stat cards'
    },
    
    # About section (gradient background)
    {
        'name': 'About section text on gradient',
        'foreground': '#ffffff',
        'background': '#ea580c',  # orange-600 (lighter end of gradient)
        'size': 'normal',
        'element': 'White text on orange-red gradient'
    },
    
    # Benefits section
    {
        'name': 'Benefit title',
        'foreground': '#1f2937',  # gray-800
        'background': '#ffffff',
        'size': 'normal',
        'element': 'h3.text-gray-800'
    },
    {
        'name': 'Benefit description',
        'foreground': '#4b5563',  # gray-600
        'background': '#ffffff',
        'size': 'normal',
        'element': 'p.text-gray-600'
    },
    
    # Pose cards
    {
        'name': 'Pose title',
        'foreground': '#1f2937',  # gray-800
        'background': '#fffbeb',  # yellow-50 (lighter background)
        'size': 'large',
        'element': 'h3.text-gray-800 on pose card'
    },
    {
        'name': 'Pose description',
        'foreground': '#4b5563',  # gray-600
        'background': '#fffbeb',  # yellow-50
        'size': 'normal',
        'element': 'p.text-gray-600 on pose card'
    },
    {
        'name': 'Pose number badge',
        'foreground': '#ffffff',
        'background': '#f97316',  # orange-500
        'size': 'large',
        'element': '.pose-number'
    },
    {
        'name': 'Mantra text',
        'foreground': '#374151',  # gray-700
        'background': '#fed7aa',  # orange-100
        'size': 'normal',
        'element': 'Mantra box text'
    },
    {
        'name': 'Metadata tags',
        'foreground': '#64748b',  # gray-500
        'background': '#fffbeb',  # yellow-50
        'size': 'normal',
        'element': 'Breathing/chakra tags'
    },
    
    # Practice guidelines
    {
        'name': 'Guidelines text on gradient',
        'foreground': '#ffffff',
        'background': '#ea580c',  # orange-600
        'size': 'normal',
        'element': 'White text on orange-red gradient'
    },
    {
        'name': 'Note box text',
        'foreground': '#374151',  # gray-700
        'background': '#fefce8',  # yellow-50
        'size': 'normal',
        'element': 'Important note box'
    },
    
    # Buttons
    {
        'name': 'Button text',
        'foreground': '#ffffff',
        'background': '#667eea',  # Approximation of gradient
        'size': 'large',
        'element': '.btn-gradient'
    },
]

def main():
    print("=" * 80)
    print("WCAG 2.1 Color Contrast Verification for Surya Namaskar Module")
    print("=" * 80)
    print()
    
    passed_aa = 0
    failed_aa = 0
    passed_aaa = 0
    
    for test in color_tests:
        ratio = contrast_ratio(test['foreground'], test['background'])
        aa_pass = check_wcag_compliance(ratio, 'AA', test['size'])
        aaa_pass = check_wcag_compliance(ratio, 'AAA', test['size'])
        
        status_aa = "✓ PASS" if aa_pass else "✗ FAIL"
        status_aaa = "✓ PASS" if aaa_pass else "✗ FAIL"
        
        if aa_pass:
            passed_aa += 1
        else:
            failed_aa += 1
        
        if aaa_pass:
            passed_aaa += 1
        
        print(f"Test: {test['name']}")
        print(f"  Element: {test['element']}")
        print(f"  Foreground: {test['foreground']}")
        print(f"  Background: {test['background']}")
        print(f"  Text size: {test['size']}")
        print(f"  Contrast ratio: {ratio:.2f}:1")
        print(f"  WCAG AA ({test['size']}): {status_aa}")
        print(f"  WCAG AAA ({test['size']}): {status_aaa}")
        print()
    
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total tests: {len(color_tests)}")
    print(f"WCAG AA passed: {passed_aa}/{len(color_tests)}")
    print(f"WCAG AA failed: {failed_aa}/{len(color_tests)}")
    print(f"WCAG AAA passed: {passed_aaa}/{len(color_tests)}")
    print()
    
    if failed_aa == 0:
        print("✓ All color combinations meet WCAG 2.1 AA standards!")
    else:
        print(f"✗ {failed_aa} color combination(s) do not meet WCAG 2.1 AA standards.")
        print("  Please review and adjust the failing combinations.")
    
    print()
    print("Minimum contrast ratios required:")
    print("  - Normal text (AA): 4.5:1")
    print("  - Large text (AA): 3.0:1")
    print("  - Normal text (AAA): 7.0:1")
    print("  - Large text (AAA): 4.5:1")
    print()
    print("Note: Large text is defined as 18pt+ or 14pt+ bold")
    print("=" * 80)

if __name__ == "__main__":
    main()
