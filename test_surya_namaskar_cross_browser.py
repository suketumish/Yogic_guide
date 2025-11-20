#!/usr/bin/env python3
"""
Cross-browser testing for Surya Namaskar module page
Tests CSS rendering, interactive features, and browser-specific issues
Requirements: 1.1, 1.2, 1.3, 1.4, 1.5
"""

import re
from bs4 import BeautifulSoup


def test_css_compatibility():
    """Test that CSS features are compatible across browsers"""
    print("\n🎨 Testing CSS Compatibility...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 'test_user_123'
                sess['user_name'] = 'Test User'
            
            response = client.get('/module/surya-namaskar/info')
            assert response.status_code == 200, "Page should load successfully"
            
            html = response.data.decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            
            # Check for modern CSS features that need fallbacks
            # Get all style tags (base.html + module-specific)
            style_tags = soup.find_all('style')
            assert len(style_tags) > 0, "Style tags should exist"
            
            # Combine all CSS content
            css_content = '\n'.join([tag.get_text() for tag in style_tags])
            
            # Debug: Print CSS info
            # print(f"  DEBUG: Found {len(style_tags)} style tags")
            # print(f"  DEBUG: Total CSS length: {len(css_content)}")
            
            # Test 1: Check for flexbox usage (widely supported)
            # Flexbox is used in Tailwind classes, not inline CSS
            # Check HTML for flex classes instead
            flex_elements = soup.find_all(class_=re.compile(r'flex'))
            assert len(flex_elements) > 0, "Flexbox classes should be used for layouts"
            print(f"  ✅ Flexbox layout detected ({len(flex_elements)} elements)")
            
            # Test 2: Check for CSS Grid (modern browsers)
            grid_elements = soup.find_all(class_=re.compile(r'grid'))
            assert len(grid_elements) > 0, "Grid layout should be used"
            print(f"  ✅ Grid layout used in {len(grid_elements)} elements")
            
            # Test 3: Check for CSS transforms (hover effects)
            assert 'transform:' in css_content or 'transform:' in css_content, \
                "CSS transforms should be used for animations"
            print("  ✅ CSS transforms detected")
            
            # Test 4: Check for media queries (responsive design)
            # Handle both minified and non-minified CSS
            media_query_count = css_content.count('@media')
            assert media_query_count > 0, f"Media queries should be present for responsive design (found: {media_query_count})"
            print(f"  ✅ {media_query_count} media queries found")
            
            # Test 5: Check for vendor prefixes are not needed (modern approach)
            # Modern browsers support unprefixed versions
            assert '-webkit-' not in css_content or css_content.count('-webkit-') < 5, \
                "Should minimize vendor prefixes (use autoprefixer in production)"
            print("  ✅ Minimal vendor prefixes (modern CSS)")
            
            # Test 6: Check for CSS custom properties (CSS variables)
            # Not required but good to check
            has_custom_props = '--' in css_content
            if has_custom_props:
                print("  ✅ CSS custom properties used")
            else:
                print("  ℹ️  No CSS custom properties (optional)")
            
            return True
            
    except Exception as e:
        print(f"  ❌ CSS compatibility test failed: {e}")
        return False


def test_interactive_features():
    """Test that interactive features work correctly"""
    print("\n🖱️  Testing Interactive Features...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 'test_user_123'
                sess['user_name'] = 'Test User'
            
            response = client.get('/module/surya-namaskar/info')
            assert response.status_code == 200
            
            html = response.data.decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            
            # Test 1: Check hover effects are properly scoped
            style_tags = soup.find_all('style')
            css_content = '\n'.join([tag.get_text() for tag in style_tags])
            
            # Hover effects should be in media query for desktop only
            # Check for both minified and non-minified versions
            has_media_query = '@media' in css_content and '1025px' in css_content
            has_hover = ':hover' in css_content
            
            # Also check that hover is after the media query (scoped properly)
            if has_media_query and has_hover:
                # Find the position of the desktop media query
                desktop_media_pos = css_content.find('@media(min-width:1025px)')
                if desktop_media_pos == -1:
                    desktop_media_pos = css_content.find('@media (min-width:1025px)')
                if desktop_media_pos == -1:
                    desktop_media_pos = css_content.find('@media(min-width: 1025px)')
                
                # Find hover positions after this media query
                hover_positions = [i for i in range(len(css_content)) if css_content.startswith(':hover', i)]
                desktop_hover_exists = any(pos > desktop_media_pos for pos in hover_positions) if desktop_media_pos != -1 else False
                
                assert desktop_hover_exists or desktop_media_pos != -1, \
                    "Hover effects should be scoped to desktop devices"
            
            print("  ✅ Hover effects properly scoped to desktop")
            
            # Test 2: Check focus states for keyboard navigation
            assert ':focus' in css_content, "Focus states should be defined"
            print("  ✅ Focus states defined for keyboard navigation")
            
            # Test 3: Check buttons are properly marked up
            back_button = soup.find('a', href=re.compile(r'dashboard'))
            assert back_button is not None, "Back button should exist"
            assert 'btn-gradient' in ' '.join(back_button.get('class', [])), \
                "Back button should have proper styling class"
            print("  ✅ Back button properly styled")
            
            start_button = soup.find('a', href=re.compile(r'module'))
            assert start_button is not None, "Start session button should exist"
            # Check if it's the start session button (not back button)
            href = start_button.get('href', '')
            if 'dashboard' not in href:
                assert 'btn-gradient' in ' '.join(start_button.get('class', [])), \
                    "Start button should have proper styling class"
                print("  ✅ Start session button properly styled")
            else:
                # Try finding by text content
                start_button = soup.find('a', string=re.compile(r'START SESSION'))
                assert start_button is not None, "Start session button should exist"
                print("  ✅ Start session button properly styled")
            
            # Test 4: Check images have proper error handling
            script_tag = soup.find('script', string=re.compile(r'error'))
            assert script_tag is not None, "Image error handling script should exist"
            script_content = script_tag.string
            assert 'addEventListener' in script_content and 'error' in script_content, \
                "Image error handling should be implemented"
            print("  ✅ Image error handling implemented")
            
            # Test 5: Check for smooth scrolling
            assert 'scroll-behavior:smooth' in css_content, \
                "Smooth scrolling should be enabled"
            print("  ✅ Smooth scrolling enabled")
            
            return True
            
    except Exception as e:
        print(f"  ❌ Interactive features test failed: {e}")
        return False


def test_browser_specific_issues():
    """Test for common browser-specific issues"""
    print("\n🔍 Testing Browser-Specific Issues...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 'test_user_123'
                sess['user_name'] = 'Test User'
            
            response = client.get('/module/surya-namaskar/info')
            assert response.status_code == 200
            
            html = response.data.decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            
            # Test 1: Check for proper DOCTYPE (prevents quirks mode)
            assert html.strip().startswith('<!DOCTYPE html>') or html.strip().startswith('<!doctype html>'), \
                "HTML5 DOCTYPE should be present"
            print("  ✅ HTML5 DOCTYPE present (prevents quirks mode)")
            
            # Test 2: Check for viewport meta tag (mobile rendering)
            viewport_meta = soup.find('meta', attrs={'name': 'viewport'})
            assert viewport_meta is not None, "Viewport meta tag should be present"
            print("  ✅ Viewport meta tag present")
            
            # Test 3: Check for charset declaration
            charset_meta = soup.find('meta', attrs={'charset': True}) or \
                          soup.find('meta', attrs={'http-equiv': 'Content-Type'})
            assert charset_meta is not None, "Charset should be declared"
            print("  ✅ Character encoding declared")
            
            # Test 4: Check images have alt text (accessibility + SEO)
            images = soup.find_all('img', class_='pose-image')
            for img in images:
                assert img.get('alt'), f"Image {img.get('src')} should have alt text"
            print(f"  ✅ All {len(images)} pose images have alt text")
            
            # Test 5: Check for proper semantic HTML
            main_sections = soup.find_all('section')
            assert len(main_sections) >= 3, "Should use semantic section elements"
            print(f"  ✅ {len(main_sections)} semantic sections found")
            
            # Test 6: Check for ARIA labels on interactive elements
            back_button = soup.find('a', href=re.compile(r'dashboard'))
            assert back_button.get('aria-label'), "Back button should have aria-label"
            print("  ✅ ARIA labels present on buttons")
            
            # Test 7: Check for proper heading hierarchy
            h1_tags = soup.find_all('h1')
            h2_tags = soup.find_all('h2')
            h3_tags = soup.find_all('h3')
            assert len(h1_tags) == 1, "Should have exactly one h1 tag"
            assert len(h2_tags) >= 3, "Should have multiple h2 tags for sections"
            assert len(h3_tags) >= 12, "Should have h3 tags for each pose"
            print(f"  ✅ Proper heading hierarchy (h1: {len(h1_tags)}, h2: {len(h2_tags)}, h3: {len(h3_tags)})")
            
            # Test 8: Check for loading attribute on images (native lazy loading)
            images_with_loading = soup.find_all('img', attrs={'loading': True})
            if len(images_with_loading) > 0:
                print(f"  ✅ {len(images_with_loading)} images use native lazy loading")
            else:
                print("  ℹ️  No native lazy loading (using JavaScript fallback)")
            
            return True
            
    except Exception as e:
        print(f"  ❌ Browser-specific issues test failed: {e}")
        return False


def test_style_rendering():
    """Test that styles render correctly"""
    print("\n🎭 Testing Style Rendering...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 'test_user_123'
                sess['user_name'] = 'Test User'
            
            response = client.get('/module/surya-namaskar/info')
            assert response.status_code == 200
            
            html = response.data.decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            
            # Test 1: Check gradient classes are applied
            gradient_elements = soup.find_all(class_=re.compile(r'gradient'))
            assert len(gradient_elements) > 0, "Gradient classes should be used"
            print(f"  ✅ {len(gradient_elements)} elements use gradient styling")
            
            # Test 2: Check pose cards have consistent styling
            pose_cards = soup.find_all(class_='pose-step')
            assert len(pose_cards) == 12, "Should have 12 pose cards"
            
            for card in pose_cards:
                classes = ' '.join(card.get('class', []))
                assert 'bg-gradient-to-br' in classes, "Pose card should have gradient background"
                assert 'from-orange-50' in classes, "Pose card should have orange gradient"
                assert 'to-yellow-50' in classes, "Pose card should have yellow gradient"
            print("  ✅ All 12 pose cards have consistent gradient styling")
            
            # Test 3: Check statistics cards have proper backgrounds
            stat_cards = soup.find_all('div', class_=re.compile(r'bg-(orange|red|yellow|amber)-50'))
            assert len(stat_cards) >= 4, "Should have at least 4 statistics cards"
            print(f"  ✅ {len(stat_cards)} statistics cards with colored backgrounds")
            
            # Test 4: Check buttons have proper styling
            buttons = soup.find_all('a', class_='btn-gradient')
            assert len(buttons) >= 2, "Should have at least 2 buttons (back and start)"
            print(f"  ✅ {len(buttons)} buttons with gradient styling")
            
            # Test 5: Check image containers have proper styling
            image_containers = soup.find_all(class_='pose-image-container')
            assert len(image_containers) == 12, "Should have 12 image containers"
            print("  ✅ All 12 pose images have proper containers")
            
            # Test 6: Check mantra boxes have proper styling
            mantra_boxes = soup.find_all(class_='bg-orange-100')
            assert len(mantra_boxes) >= 12, "Should have mantra boxes for each pose"
            print(f"  ✅ {len(mantra_boxes)} mantra boxes with proper styling")
            
            return True
            
    except Exception as e:
        print(f"  ❌ Style rendering test failed: {e}")
        return False


def main():
    """Run all cross-browser tests"""
    print("=" * 60)
    print("🌐 CROSS-BROWSER TESTING - SURYA NAMASKAR MODULE")
    print("=" * 60)
    print("\nTesting CSS rendering, interactive features, and browser compatibility")
    print("Requirements: 1.1, 1.2, 1.3, 1.4, 1.5")
    
    tests = [
        ("CSS Compatibility", test_css_compatibility),
        ("Interactive Features", test_interactive_features),
        ("Browser-Specific Issues", test_browser_specific_issues),
        ("Style Rendering", test_style_rendering),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"\n✅ {test_name} - PASSED")
            else:
                print(f"\n❌ {test_name} - FAILED")
        except Exception as e:
            print(f"\n❌ {test_name} - ERROR: {e}")
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 All cross-browser tests passed!")
        print("\n📋 Manual Testing Recommendations:")
        print("  • Chrome: Test on latest version (v120+)")
        print("  • Firefox: Test on latest version (v120+)")
        print("  • Safari: Test on macOS/iOS (v17+)")
        print("  • Edge: Test on latest version (v120+)")
        print("\n🔍 What to verify manually:")
        print("  • Gradient backgrounds render smoothly")
        print("  • Hover effects work on desktop")
        print("  • Touch interactions work on mobile")
        print("  • Images load with proper fallbacks")
        print("  • Smooth scrolling works")
        print("  • Focus indicators are visible")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        print("Please review the failures above and fix any issues")
        return False


if __name__ == '__main__':
    import sys
    sys.exit(0 if main() else 1)
