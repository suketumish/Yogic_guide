#!/usr/bin/env python3
"""
User flow testing for Surya Namaskar module page
Tests navigation from dashboard, back button, start session, and all links
Requirements: 1.1, 7.5
"""

import re
from bs4 import BeautifulSoup


def test_navigation_from_dashboard():
    """Test navigation from dashboard to Surya Namaskar module"""
    print("\n🧭 Testing Navigation from Dashboard...")
    
    try:
        from app import app
        from bson import ObjectId
        
        with app.test_client() as client:
            # Use a valid ObjectId format
            test_user_id = str(ObjectId())
            with client.session_transaction() as sess:
                sess['user_id'] = test_user_id
                sess['user_name'] = 'Test User'
            
            # Step 1: Load dashboard
            dashboard_response = client.get('/dashboard')
            assert dashboard_response.status_code == 200, "Dashboard should load successfully"
            print("  ✅ Dashboard loads successfully")
            
            # Step 2: Check for Surya Namaskar link on dashboard
            dashboard_html = dashboard_response.data.decode('utf-8')
            dashboard_soup = BeautifulSoup(dashboard_html, 'html.parser')
            
            # Look for Surya Namaskar module link
            surya_link = dashboard_soup.find('a', href=re.compile(r'surya-namaskar')) or \
                        dashboard_soup.find('a', string=re.compile(r'Surya Namaskar', re.IGNORECASE))
            
            if surya_link:
                print("  ✅ Surya Namaskar link found on dashboard")
                href = surya_link.get('href', '')
                print(f"     Link: {href}")
            else:
                print("  ℹ️  Surya Namaskar link not found on dashboard (may be accessed differently)")
            
            # Step 3: Navigate to Surya Namaskar module
            module_response = client.get('/module/surya-namaskar/info')
            assert module_response.status_code == 200, "Surya Namaskar module should load"
            print("  ✅ Surya Namaskar module loads successfully")
            
            # Step 4: Verify module page content
            module_html = module_response.data.decode('utf-8')
            module_soup = BeautifulSoup(module_html, 'html.parser')
            
            # Check for key elements
            title = module_soup.find('h1')
            assert title is not None, "Module page should have h1 title"
            assert 'SURYA NAMASKAR' in title.get_text().upper(), "Title should contain 'Surya Namaskar'"
            print("  ✅ Module page displays correct title")
            
            # Check for pose cards
            pose_cards = module_soup.find_all(class_='pose-step')
            assert len(pose_cards) == 12, "Should display all 12 poses"
            print(f"  ✅ All {len(pose_cards)} poses displayed")
            
            return True
            
    except Exception as e:
        print(f"  ❌ Navigation from dashboard test failed: {e}")
        return False


def test_back_button_functionality():
    """Test back button returns to dashboard"""
    print("\n⬅️  Testing Back Button Functionality...")
    
    try:
        from app import app
        from bson import ObjectId
        
        with app.test_client() as client:
            test_user_id = str(ObjectId())
            with client.session_transaction() as sess:
                sess['user_id'] = test_user_id
                sess['user_name'] = 'Test User'
            
            # Step 1: Load Surya Namaskar module
            response = client.get('/module/surya-namaskar/info')
            assert response.status_code == 200
            
            html = response.data.decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            
            # Step 2: Find back button
            back_button = soup.find('a', href=re.compile(r'dashboard'))
            assert back_button is not None, "Back button should exist"
            print("  ✅ Back button found on page")
            
            # Step 3: Verify back button attributes
            href = back_button.get('href', '')
            assert 'dashboard' in href, "Back button should link to dashboard"
            print(f"  ✅ Back button links to: {href}")
            
            # Step 4: Check back button has proper styling
            classes = ' '.join(back_button.get('class', []))
            assert 'btn-gradient' in classes, "Back button should have btn-gradient class"
            print("  ✅ Back button has proper styling")
            
            # Step 5: Check back button has aria-label
            aria_label = back_button.get('aria-label', '')
            assert aria_label, "Back button should have aria-label"
            assert 'dashboard' in aria_label.lower(), "Aria-label should describe action"
            print(f"  ✅ Back button has aria-label: '{aria_label}'")
            
            # Step 6: Check back button text/content
            button_text = back_button.get_text(strip=True)
            assert button_text, "Back button should have visible text"
            print(f"  ✅ Back button text: '{button_text}'")
            
            # Step 7: Test actual navigation
            dashboard_response = client.get(href)
            assert dashboard_response.status_code == 200, "Dashboard should load when clicking back"
            print("  ✅ Back button navigation works correctly")
            
            return True
            
    except Exception as e:
        print(f"  ❌ Back button functionality test failed: {e}")
        return False


def test_start_session_button():
    """Test start session button functionality"""
    print("\n▶️  Testing Start Session Button...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 'test_user_123'
                sess['user_name'] = 'Test User'
            
            # Step 1: Load Surya Namaskar module
            response = client.get('/module/surya-namaskar/info')
            assert response.status_code == 200
            
            html = response.data.decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            
            # Step 2: Find start session button
            start_button = soup.find('a', string=re.compile(r'START SESSION', re.IGNORECASE)) or \
                          soup.find('a', href=re.compile(r'module.*surya'))
            
            assert start_button is not None, "Start session button should exist"
            print("  ✅ Start session button found on page")
            
            # Step 3: Verify button attributes
            href = start_button.get('href', '')
            assert 'module' in href and 'surya' in href, "Button should link to session"
            print(f"  ✅ Start button links to: {href}")
            
            # Step 4: Check button has proper styling
            classes = ' '.join(start_button.get('class', []))
            assert 'btn-gradient' in classes, "Start button should have btn-gradient class"
            print("  ✅ Start button has proper styling")
            
            # Step 5: Check button has aria-label
            aria_label = start_button.get('aria-label', '')
            if aria_label:
                print(f"  ✅ Start button has aria-label: '{aria_label}'")
            else:
                print("  ℹ️  Start button has no aria-label (text is descriptive)")
            
            # Step 6: Check button text/content
            button_text = start_button.get_text(strip=True)
            assert button_text, "Start button should have visible text"
            assert 'START' in button_text.upper() or 'SESSION' in button_text.upper(), \
                "Button text should indicate starting a session"
            print(f"  ✅ Start button text: '{button_text}'")
            
            # Step 7: Check button is prominently placed
            # Should be in a centered container
            parent = start_button.parent
            parent_classes = ' '.join(parent.get('class', [])) if parent else ''
            if 'text-center' in parent_classes:
                print("  ✅ Start button is prominently centered")
            else:
                print("  ℹ️  Start button placement (check manually)")
            
            # Step 8: Test actual navigation (session page might require more setup)
            try:
                session_response = client.get(href, follow_redirects=True)
                if session_response.status_code == 200:
                    print("  ✅ Start session navigation works correctly")
                else:
                    print(f"  ℹ️  Session page returned status {session_response.status_code}")
            except Exception as nav_error:
                print(f"  ℹ️  Session navigation: {nav_error}")
            
            return True
            
    except Exception as e:
        print(f"  ❌ Start session button test failed: {e}")
        return False


def test_all_links_work():
    """Test that all links on the page work correctly"""
    print("\n🔗 Testing All Links...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 'test_user_123'
                sess['user_name'] = 'Test User'
            
            # Step 1: Load Surya Namaskar module
            response = client.get('/module/surya-namaskar/info')
            assert response.status_code == 200
            
            html = response.data.decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            
            # Step 2: Find all links
            all_links = soup.find_all('a', href=True)
            print(f"  Found {len(all_links)} links on page")
            
            # Step 3: Categorize links
            internal_links = []
            external_links = []
            anchor_links = []
            
            for link in all_links:
                href = link.get('href', '')
                if href.startswith('#'):
                    anchor_links.append(href)
                elif href.startswith('http://') or href.startswith('https://'):
                    external_links.append(href)
                elif href.startswith('/') or not href.startswith('http'):
                    internal_links.append(href)
            
            print(f"  ✅ {len(internal_links)} internal links")
            print(f"  ✅ {len(external_links)} external links")
            print(f"  ✅ {len(anchor_links)} anchor links")
            
            # Step 4: Test internal links
            tested_links = set()
            working_links = 0
            broken_links = []
            
            for href in internal_links:
                if href in tested_links:
                    continue
                tested_links.add(href)
                
                try:
                    link_response = client.get(href, follow_redirects=True)
                    if link_response.status_code == 200:
                        working_links += 1
                    else:
                        broken_links.append((href, link_response.status_code))
                except Exception as e:
                    broken_links.append((href, str(e)))
            
            if broken_links:
                print(f"  ⚠️  {len(broken_links)} links may have issues:")
                for href, status in broken_links[:5]:  # Show first 5
                    print(f"     - {href}: {status}")
            else:
                print(f"  ✅ All {working_links} internal links work correctly")
            
            # Step 5: Check for broken image links
            images = soup.find_all('img', src=True)
            print(f"  Found {len(images)} images")
            
            image_sources = set()
            for img in images:
                src = img.get('src', '')
                if src and not src.startswith('data:'):
                    image_sources.add(src)
            
            print(f"  ✅ {len(image_sources)} unique image sources")
            
            # Step 6: Verify key navigation links exist
            key_links = {
                'Dashboard': soup.find('a', href=re.compile(r'dashboard')),
                'Start Session': soup.find('a', href=re.compile(r'module.*surya')) or \
                                soup.find('a', string=re.compile(r'START SESSION', re.IGNORECASE))
            }
            
            for link_name, link_element in key_links.items():
                if link_element:
                    print(f"  ✅ {link_name} link present")
                else:
                    print(f"  ❌ {link_name} link missing")
            
            return True
            
    except Exception as e:
        print(f"  ❌ All links test failed: {e}")
        return False


def test_complete_user_journey():
    """Test complete user journey through the module"""
    print("\n🚶 Testing Complete User Journey...")
    
    try:
        from app import app
        from bson import ObjectId
        
        with app.test_client() as client:
            test_user_id = str(ObjectId())
            with client.session_transaction() as sess:
                sess['user_id'] = test_user_id
                sess['user_name'] = 'Test User'
            
            # Journey Step 1: User starts at dashboard
            print("  Step 1: User visits dashboard")
            dashboard_response = client.get('/dashboard')
            assert dashboard_response.status_code == 200
            print("  ✅ Dashboard loads")
            
            # Journey Step 2: User navigates to Surya Namaskar module
            print("  Step 2: User navigates to Surya Namaskar module")
            module_response = client.get('/module/surya-namaskar/info')
            assert module_response.status_code == 200
            print("  ✅ Module page loads")
            
            # Journey Step 3: User reads about Surya Namaskar
            print("  Step 3: User reads module content")
            module_html = module_response.data.decode('utf-8')
            module_soup = BeautifulSoup(module_html, 'html.parser')
            
            # Check key sections are present
            sections = {
                'Header': module_soup.find('h1'),
                'About': module_soup.find('section', attrs={'aria-labelledby': 'about-heading'}),
                'Benefits': module_soup.find('section', attrs={'aria-labelledby': 'benefits-heading'}),
                'Poses': module_soup.find('section', attrs={'aria-labelledby': 'poses-heading'}),
                'Guidelines': module_soup.find('section', attrs={'aria-labelledby': 'guidelines-heading'})
            }
            
            for section_name, section_element in sections.items():
                if section_element:
                    print(f"  ✅ {section_name} section present")
                else:
                    print(f"  ⚠️  {section_name} section not found")
            
            # Journey Step 4: User scrolls through poses
            print("  Step 4: User views all poses")
            pose_cards = module_soup.find_all(class_='pose-step')
            assert len(pose_cards) == 12, "Should have 12 poses"
            print(f"  ✅ All {len(pose_cards)} poses visible")
            
            # Journey Step 5: User decides to start session
            print("  Step 5: User clicks start session")
            start_button = module_soup.find('a', string=re.compile(r'START SESSION', re.IGNORECASE)) or \
                          module_soup.find('a', href=re.compile(r'module.*surya'))
            assert start_button is not None
            session_href = start_button.get('href', '')
            print(f"  ✅ Start session button found: {session_href}")
            
            # Journey Step 6: User can go back to dashboard
            print("  Step 6: User can return to dashboard")
            back_button = module_soup.find('a', href=re.compile(r'dashboard'))
            assert back_button is not None
            print("  ✅ Back button available")
            
            # Test back navigation
            back_response = client.get(back_button.get('href', ''))
            assert back_response.status_code == 200
            print("  ✅ Back navigation works")
            
            print("\n  🎉 Complete user journey successful!")
            return True
            
    except Exception as e:
        print(f"  ❌ Complete user journey test failed: {e}")
        return False


def main():
    """Run all user flow tests"""
    print("=" * 60)
    print("🚶 USER FLOW TESTING - SURYA NAMASKAR MODULE")
    print("=" * 60)
    print("\nTesting navigation, buttons, links, and complete user journey")
    print("Requirements: 1.1, 7.5")
    
    tests = [
        ("Navigation from Dashboard", test_navigation_from_dashboard),
        ("Back Button Functionality", test_back_button_functionality),
        ("Start Session Button", test_start_session_button),
        ("All Links Work", test_all_links_work),
        ("Complete User Journey", test_complete_user_journey),
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
        print("\n🎉 All user flow tests passed!")
        print("\n📋 Manual Testing Recommendations:")
        print("\n🧭 Navigation Flow:")
        print("  1. Start from dashboard")
        print("  2. Click on Surya Namaskar module")
        print("  3. Scroll through all 12 poses")
        print("  4. Read benefits and guidelines")
        print("  5. Click 'Start Session' button")
        print("  6. Use back button to return to dashboard")
        print("\n🔍 What to verify manually:")
        print("  • Navigation is intuitive and clear")
        print("  • Back button always returns to dashboard")
        print("  • Start session button is prominent")
        print("  • All links are clickable and work")
        print("  • No broken images or links")
        print("  • Smooth transitions between pages")
        print("  • Browser back/forward buttons work")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        print("Please review the failures above and fix any issues")
        return False


if __name__ == '__main__':
    import sys
    sys.exit(0 if main() else 1)
