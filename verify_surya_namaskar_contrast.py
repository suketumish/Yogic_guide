"""
Color Contrast Verification Script for Surya Namaskar Module Page
Tests all text/background combinations against WCAG 2.1 AA standards
- Body text: minimum 4.5:1 ratio
- Large text (18pt+ or 14pt+ bold): minimum 3:1 ratio
- UI components: minimum 3:1 ratio
"""

import colorsys
from typing import Tuple, List, Dict


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_relative_luminance(rgb: Tuple[int, int, int]) -> float:
    """
    Calculate relative luminance according to WCAG 2.1
    https://www.w3.org/TR/WCAG21/#dfn-relative-luminance
    """
    r, g, b = [x / 255.0 for x in rgb]
    
    # Apply gamma correction
    def adjust(channel):
        if channel <= 0.03928:
            return channel / 12.92
        return ((channel + 0.055) / 1.055) ** 2.4
    
    r_adj = adjust(r)
    g_adj = adjust(g)
    b_adj = adjust(b)
    
    # Calculate luminance
    return 0.2126 * r_adj + 0.7152 * g_adj + 0.0722 * b_adj


def calculate_contrast_ratio(color1: str, color2: str) -> float:
    """
    Calculate contrast ratio between two colors
    Returns ratio as float (e.g., 4.5 for 4.5:1)
    """
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)
    
    lum1 = rgb_to_relative_luminance(rgb1)
    lum2 = rgb_to_relative_luminance(rgb2)
    
    # Ensure lighter color is in numerator
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    
    return (lighter + 0.05) / (darker + 0.05)


def check_wcag_compliance(ratio: float, text_type: str) -> Dict[str, bool]:
    """
    Check if contrast ratio meets WCAG standards
    text_type: 'body', 'large', or 'ui'
    """
    if text_type == 'body':
        aa_pass = ratio >= 4.5
        aaa_pass = ratio >= 7.0
    elif text_type == 'large':
        aa_pass = ratio >= 3.0
        aaa_pass = ratio >= 4.5
    elif text_type == 'ui':
        aa_pass = ratio >= 3.0
        aaa_pass = False  # AAA not defined for UI components
    else:
        aa_pass = False
        aaa_pass = False
    
    return {
        'AA': aa_pass,
        'AAA': aaa_pass
    }


# Tailwind color palette (approximations)
COLORS = {
    # Grays
    'slate-50': '#f8fafc',
    'slate-200': '#e2e8f0',
    'slate-600': '#475569',
    'slate-700': '#334155',
    'gray-500': '#6b7280',
    'gray-600': '#4b5563',
    'gray-700': '#374151',
    'gray-800': '#1f2937',
    'gray-900': '#111827',
    
    # Orange
    'orange-50': '#fff7ed',
    'orange-100': '#ffedd5',
    'orange-200': '#fed7aa',
    'orange-500': '#f97316',
    'orange-600': '#ea580c',
    
    # Red
    'red-50': '#fef2f2',
    'red-600': '#dc2626',
    
    # Yellow
    'yellow-50': '#fefce8',
    'yellow-500': '#eab308',
    'yellow-600': '#ca8a04',
    
    # Amber
    'amber-50': '#fffbeb',
    'amber-600': '#d97706',
    
    # White
    'white': '#ffffff',
    
    # Gradient colors (using midpoint approximations)
    'gradient-purple-start': '#667eea',  # Primary gradient start
    'gradient-purple-end': '#764ba2',    # Primary gradient end
}


def test_color_combination(
    fg_name: str,
    fg_color: str,
    bg_name: str,
    bg_color: str,
    text_type: str,
    component: str
) -> Dict:
    """Test a single color combination"""
    ratio = calculate_contrast_ratio(fg_color, bg_color)
    compliance = check_wcag_compliance(ratio, text_type)
    
    return {
        'component': component,
        'foreground': f'{fg_name} ({fg_color})',
        'background': f'{bg_name} ({bg_color})',
        'text_type': text_type,
        'ratio': ratio,
        'AA': compliance['AA'],
        'AAA': compliance['AAA']
    }


def main():
    """Run all color contrast tests for Surya Namaskar module page"""
    
    print("=" * 80)
    print("COLOR CONTRAST VERIFICATION - SURYA NAMASKAR MODULE PAGE")
    print("=" * 80)
    print()
    
    results = []
    
    # Test combinations based on the template analysis
    
    # 1. Header Section
    print("1. HEADER SECTION")
    print("-" * 80)
    
    # Title gradient (approximation - testing against white background)
    results.append(test_color_combination(
        'gradient-purple', COLORS['gradient-purple-start'],
        'white/slate-50', COLORS['white'],
        'large', 'Header: Title (SURYA NAMASKAR)'
    ))
    
    # Subtitle
    results.append(test_color_combination(
        'slate-600', COLORS['slate-600'],
        'white/slate-50', COLORS['white'],
        'body', 'Header: Subtitle text'
    ))
    
    # Statistics cards
    results.append(test_color_combination(
        'orange-600', COLORS['orange-600'],
        'orange-50', COLORS['orange-50'],
        'large', 'Stats: Orange card value (10-12)'
    ))
    
    results.append(test_color_combination(
        'gray-600', COLORS['gray-600'],
        'orange-50', COLORS['orange-50'],
        'body', 'Stats: Orange card label (Minutes)'
    ))
    
    results.append(test_color_combination(
        'red-600', COLORS['red-600'],
        'red-50', COLORS['red-50'],
        'large', 'Stats: Red card value (Intermediate)'
    ))
    
    results.append(test_color_combination(
        'gray-600', COLORS['gray-600'],
        'red-50', COLORS['red-50'],
        'body', 'Stats: Red card label (Level)'
    ))
    
    results.append(test_color_combination(
        'yellow-700', '#a16207',
        'yellow-50', COLORS['yellow-50'],
        'large', 'Stats: Yellow card value (~80)'
    ))
    
    results.append(test_color_combination(
        'gray-600', COLORS['gray-600'],
        'yellow-50', COLORS['yellow-50'],
        'body', 'Stats: Yellow card label (Calories)'
    ))
    
    results.append(test_color_combination(
        'amber-600', COLORS['amber-600'],
        'amber-50', COLORS['amber-50'],
        'large', 'Stats: Amber card value (Full Body)'
    ))
    
    results.append(test_color_combination(
        'gray-600', COLORS['gray-600'],
        'amber-50', COLORS['amber-50'],
        'body', 'Stats: Amber card label (Workout)'
    ))
    
    # 2. About Section (gradient background)
    print("\n2. ABOUT SURYA NAMASKAR SECTION")
    print("-" * 80)
    
    results.append(test_color_combination(
        'white', COLORS['white'],
        'orange-700', '#c2410c',
        'large', 'About: Heading text on gradient'
    ))
    
    results.append(test_color_combination(
        'white', COLORS['white'],
        'orange-700', '#c2410c',
        'body', 'About: Body text (large) on gradient'
    ))
    
    results.append(test_color_combination(
        'white', COLORS['white'],
        'red-700', '#b91c1c',
        'body', 'About: Body text on gradient (red end)'
    ))
    
    # 3. Benefits Section
    print("\n3. BENEFITS SECTION")
    print("-" * 80)
    
    results.append(test_color_combination(
        'gray-800', COLORS['gray-800'],
        'white', COLORS['white'],
        'large', 'Benefits: Section heading'
    ))
    
    results.append(test_color_combination(
        'gray-800', COLORS['gray-800'],
        'white', COLORS['white'],
        'large', 'Benefits: Benefit titles (bold)'
    ))
    
    results.append(test_color_combination(
        'gray-600', COLORS['gray-600'],
        'white', COLORS['white'],
        'body', 'Benefits: Benefit descriptions'
    ))
    
    # 4. Pose Cards
    print("\n4. POSE CARDS")
    print("-" * 80)
    
    results.append(test_color_combination(
        'gray-800', COLORS['gray-800'],
        'orange-50', COLORS['orange-50'],
        'large', 'Pose: Section heading'
    ))
    
    results.append(test_color_combination(
        'white', COLORS['white'],
        'orange-600', COLORS['orange-600'],
        'ui', 'Pose: Number badge (white on orange)'
    ))
    
    results.append(test_color_combination(
        'gray-800', COLORS['gray-800'],
        'orange-50', COLORS['orange-50'],
        'large', 'Pose: Pose title (bold, xl)'
    ))
    
    results.append(test_color_combination(
        'gray-600', COLORS['gray-600'],
        'orange-50', COLORS['orange-50'],
        'body', 'Pose: Description text'
    ))
    
    # Mantra box
    results.append(test_color_combination(
        'gray-700', COLORS['gray-700'],
        'orange-100', COLORS['orange-100'],
        'body', 'Pose: Mantra text on orange-100'
    ))
    
    # Metadata tags
    results.append(test_color_combination(
        'gray-500', COLORS['gray-500'],
        'orange-50', COLORS['orange-50'],
        'body', 'Pose: Metadata tags (breathing, chakra)'
    ))
    
    # 5. Practice Guidelines Section
    print("\n5. PRACTICE GUIDELINES SECTION")
    print("-" * 80)
    
    results.append(test_color_combination(
        'white', COLORS['white'],
        'orange-700', '#c2410c',
        'large', 'Guidelines: Heading on gradient'
    ))
    
    results.append(test_color_combination(
        'white', COLORS['white'],
        'orange-700', '#c2410c',
        'body', 'Guidelines: Guideline text on gradient'
    ))
    
    results.append(test_color_combination(
        'white', COLORS['white'],
        'red-700', '#b91c1c',
        'body', 'Guidelines: Text on gradient (red end)'
    ))
    
    # Important note box
    results.append(test_color_combination(
        'gray-700', COLORS['gray-700'],
        'yellow-50', COLORS['yellow-50'],
        'body', 'Guidelines: Note box text'
    ))
    
    # 6. Buttons
    print("\n6. BUTTONS")
    print("-" * 80)
    
    results.append(test_color_combination(
        'white', COLORS['white'],
        'gradient-purple-start', COLORS['gradient-purple-start'],
        'ui', 'Button: Text on gradient (start)'
    ))
    
    results.append(test_color_combination(
        'white', COLORS['white'],
        'gradient-purple-end', COLORS['gradient-purple-end'],
        'ui', 'Button: Text on gradient (end)'
    ))
    
    # 7. Footer
    print("\n7. FOOTER")
    print("-" * 80)
    
    results.append(test_color_combination(
        'white', COLORS['white'],
        'gray-900', COLORS['gray-900'],
        'large', 'Footer: Brand name'
    ))
    
    results.append(test_color_combination(
        'gray-300', '#d1d5db',
        'gray-900', COLORS['gray-900'],
        'body', 'Footer: Subtitle text (gray-300)'
    ))
    
    # Print results
    print("\n" + "=" * 80)
    print("TEST RESULTS")
    print("=" * 80)
    print()
    
    passed_aa = 0
    passed_aaa = 0
    failed_aa = 0
    
    for result in results:
        status_aa = "✓ PASS" if result['AA'] else "✗ FAIL"
        status_aaa = "✓ PASS" if result['AAA'] else "✗ FAIL" if result['text_type'] != 'ui' else "N/A"
        
        print(f"Component: {result['component']}")
        print(f"  Foreground: {result['foreground']}")
        print(f"  Background: {result['background']}")
        print(f"  Text Type: {result['text_type']}")
        print(f"  Contrast Ratio: {result['ratio']:.2f}:1")
        print(f"  WCAG AA (Required): {status_aa}")
        print(f"  WCAG AAA (Enhanced): {status_aaa}")
        
        if result['AA']:
            passed_aa += 1
        else:
            failed_aa += 1
            print(f"  ⚠️  ATTENTION: This combination does not meet WCAG AA standards!")
            
            # Provide recommendations
            if result['text_type'] == 'body':
                print(f"     Required ratio: 4.5:1 (current: {result['ratio']:.2f}:1)")
            elif result['text_type'] == 'large':
                print(f"     Required ratio: 3.0:1 (current: {result['ratio']:.2f}:1)")
            elif result['text_type'] == 'ui':
                print(f"     Required ratio: 3.0:1 (current: {result['ratio']:.2f}:1)")
        
        if result['AAA'] and result['text_type'] != 'ui':
            passed_aaa += 1
        
        print()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total combinations tested: {len(results)}")
    print(f"WCAG AA Passed: {passed_aa} ({passed_aa/len(results)*100:.1f}%)")
    print(f"WCAG AA Failed: {failed_aa} ({failed_aa/len(results)*100:.1f}%)")
    print(f"WCAG AAA Passed: {passed_aaa} (Enhanced compliance)")
    print()
    
    if failed_aa == 0:
        print("✓ ALL COLOR COMBINATIONS MEET WCAG 2.1 AA STANDARDS!")
        print("  The Surya Namaskar module page is accessible and compliant.")
    else:
        print("⚠️  SOME COLOR COMBINATIONS DO NOT MEET WCAG 2.1 AA STANDARDS")
        print("  Please review the failed combinations above and adjust colors.")
    
    print()
    print("=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    print()
    print("For body text (small text):")
    print("  - Minimum contrast ratio: 4.5:1 (WCAG AA)")
    print("  - Enhanced contrast ratio: 7.0:1 (WCAG AAA)")
    print()
    print("For large text (18pt+ or 14pt+ bold):")
    print("  - Minimum contrast ratio: 3.0:1 (WCAG AA)")
    print("  - Enhanced contrast ratio: 4.5:1 (WCAG AAA)")
    print()
    print("For UI components (borders, icons, etc.):")
    print("  - Minimum contrast ratio: 3.0:1 (WCAG AA)")
    print()
    print("If any combinations failed:")
    print("  1. Darken the text color or lighten the background")
    print("  2. Use a different color combination")
    print("  3. Increase font weight or size to qualify as 'large text'")
    print("  4. Test with online tools: https://webaim.org/resources/contrastchecker/")
    print()
    
    return failed_aa == 0


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
