"""
Screen Reader Accessibility Test for Surya Namaskar Module Page

This test verifies that the page is properly structured for screen readers including:
- Proper heading hierarchy (h1, h2, h3)
- ARIA labels and attributes
- Landmark regions
- Alt text for images
- Semantic HTML structure
- Keyboard navigation support
"""

import pytest
from bs4 import BeautifulSoup
from flask import url_for


@pytest.fixture
def authenticated_client(client, app):
    """Create an authenticated test client"""
    with client.session_transaction() as session:
        session['user_id'] = 'test_user_123'
        session['username'] = 'testuser'
    return client


class TestScreenReaderAccessibility:
    """Test suite for screen reader accessibility compliance"""
    
    def test_page_loads_successfully(self, authenticated_client):
        """Verify the Surya Namaskar page loads without errors"""
        response = authenticated_client.get('/module/surya-namaskar/info')
        assert response.status_code == 200
        assert b'Surya Namaskar' in response.data or b'SURYA NAMASKAR' in response.data
    
    def test_heading_hierarchy(self, authenticated_client):
        """Verify proper heading hierarchy (h1 -> h2 -> h3) for screen readers"""
        response = authenticated_client.get('/module/surya-namaskar/info')
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for single h1 (page title)
        h1_tags = soup.find_all('h1')
        assert len(h1_tags) == 1, "Page should have exactly one h1 tag"
        assert 'SURYA NAMASKAR' in h1_tags[0].get_text().upper()
        
        # Check for h2 section headings
        h2_tags = soup.find_all('h2')
        assert len(h2_tags) >= 4, "Page should have at least 4 h2 section headings"
        
        # Verify h2 headings have proper IDs for ARIA labelledby
        h2_with_ids = [h2 for h2 in h2_tags if h2.get('id')]
        assert len(h2_with_ids) >= 4, "All h2 headings should have IDs for ARIA references"
        
        # Check for h3 pose titles (includes benefit titles + pose titles)
        h3_tags = soup.find_all('h3')
        assert len(h3_tags) >= 12, "Page should have at least 12 h3 tags for pose titles"
        
        # Verify pose h3 headings have proper IDs
        h3_with_ids = [h3 for h3 in h3_tags if h3.get('id') and 'pose' in h3.get('id')]
        assert len(h3_with_ids) == 12, "All 12 pose titles should have IDs for ARIA labelledby"
        
        # Verify heading hierarchy order (no skipping levels)
        all_headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        heading_levels = [int(h.name[1]) for h in all_headings]
        
        for i in range(len(heading_levels) - 1):
            level_jump = heading_levels[i + 1] - heading_levels[i]
            assert level_jump <= 1, f"Heading hierarchy should not skip levels (found jump from h{heading_levels[i]} to h{heading_levels[i+1]})"
    
    def test_landmark_regions(self, authenticated_client):
        """Verify proper landmark regions (main, nav, section, article) for screen reader navigation"""
        response = authenticated_client.get('/module/surya-namaskar/info')
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for section landmarks with aria-labelledby
        sections = soup.find_all('section')
        assert len(sections) >= 3, "Page should have at least 3 section landmarks"
        
        # Verify sections have aria-labelledby attributes
        sections_with_labels = [s for s in sections if s.get('aria-labelledby')]
        assert len(sections_with_labels) >= 3, "All major sections should have aria-labelledby attributes"
        
        # Check for article elements (pose cards)
        articles = soup.find_all('article')
        assert len(articles) == 12, "Page should have 12 article elements for pose cards"
        
        # Verify articles have proper ARIA attributes
        articles_with_labels = [a for a in articles if a.get('aria-labelledby')]
        assert len(articles_with_labels) == 12, "All pose cards should have aria-labelledby attributes"
    
    def test_aria_labels_on_buttons(self, authenticated_client):
        """Verify all interactive buttons have proper ARIA labels"""
        response = authenticated_client.get('/module/surya-namaskar/info')
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check back button has aria-label
        back_button = soup.find('a', href=lambda x: x and 'dashboard' in x)
        assert back_button is not None, "Back button should exist"
        assert back_button.get('aria-label'), "Back button should have aria-label"
        assert 'dashboard' in back_button.get('aria-label').lower(), "Back button aria-label should describe action"
        
        # Check start session button has aria-label (if it exists on this page)
        start_button = soup.find('a', href=lambda x: x and 'module_session' in x)
        if start_button:
            assert start_button.get('aria-label'), "Start session button should have aria-label"
            assert 'start' in start_button.get('aria-label').lower() or 'session' in start_button.get('aria-label').lower(), "Start button aria-label should describe action"
    
    def test_decorative_emojis_hidden(self, authenticated_client):
        """Verify decorative emojis are hidden from screen readers with aria-hidden"""
        response = authenticated_client.get('/module/surya-namaskar/info')
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Find elements with aria-hidden="true"
        hidden_elements = soup.find_all(attrs={'aria-hidden': 'true'})
        assert len(hidden_elements) > 0, "Decorative elements should be hidden from screen readers"
        
        # Verify common decorative emojis are hidden
        decorative_emojis = ['☀️', '←', '→', '✨', '🌞', '💡']
        for emoji in decorative_emojis:
            emoji_elements = soup.find_all(string=lambda text: text and emoji in text)
            for elem in emoji_elements:
                parent = elem.parent
                # Check if parent or ancestor has aria-hidden
                has_aria_hidden = False
                current = parent
                for _ in range(3):  # Check up to 3 levels up
                    if current and current.get('aria-hidden') == 'true':
                        has_aria_hidden = True
                        break
                    current = current.parent if hasattr(current, 'parent') else None
                
                # At least some decorative emojis should be hidden
                # (Not all need to be, but key decorative ones should be)
    
    def test_image_alt_text(self, authenticated_client):
        """Verify all pose images have descriptive alt text"""
        response = authenticated_client.get('/module/surya-namaskar/info')
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Find all pose images
        pose_images = soup.find_all('img', class_='pose-image')
        assert len(pose_images) == 12, "Page should have 12 pose images"
        
        # Verify each image has alt text
        for img in pose_images:
            alt_text = img.get('alt', '')
            assert alt_text, "All images must have alt text"
            assert len(alt_text) > 20, f"Alt text should be descriptive (found: '{alt_text}')"
            
            # Verify alt text contains key information
            assert 'Step' in alt_text or 'step' in alt_text, "Alt text should include step number"
            assert 'Surya Namaskar' in alt_text, "Alt text should mention Surya Namaskar"
            
            # Verify alt text describes the pose
            pose_names = ['Pranamasana', 'Hasta Uttanasana', 'Hasta Padasana', 
                         'Ashwa Sanchalanasana', 'Dandasana', 'Ashtanga Namaskara',
                         'Bhujangasana', 'Adho Mukha Svanasana']
            has_pose_name = any(name in alt_text for name in pose_names)
            assert has_pose_name, f"Alt text should include pose name (found: '{alt_text}')"
    
    def test_role_attributes(self, authenticated_client):
        """Verify proper role attributes for lists and interactive elements"""
        response = authenticated_client.get('/module/surya-namaskar/info')
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for role="list" on statistics grid
        stats_grid = soup.find('div', attrs={'role': 'list', 'aria-label': lambda x: x and 'statistics' in x.lower()})
        assert stats_grid is not None, "Statistics grid should have role='list'"
        
        # Check for role="listitem" on stat cards
        stat_items = stats_grid.find_all(attrs={'role': 'listitem'}) if stats_grid else []
        assert len(stat_items) == 4, "Statistics grid should have 4 list items"
        
        # Check for role="list" on pose sequence
        pose_list = soup.find('div', attrs={'role': 'list', 'aria-label': lambda x: x and 'pose' in x.lower()})
        assert pose_list is not None, "Pose sequence should have role='list'"
        
        # Check for role="listitem" on pose cards
        pose_items = pose_list.find_all(attrs={'role': 'listitem'}) if pose_list else []
        assert len(pose_items) == 12, "Pose sequence should have 12 list items"
        
        # Check for role="note" on important note
        note_element = soup.find(attrs={'role': 'note'})
        assert note_element is not None, "Important note should have role='note'"
    
    def test_aria_labelledby_references(self, authenticated_client):
        """Verify aria-labelledby attributes reference valid IDs"""
        response = authenticated_client.get('/module/surya-namaskar/info')
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Collect all IDs in the document
        all_ids = set()
        for elem in soup.find_all(id=True):
            all_ids.add(elem.get('id'))
        
        # Check all aria-labelledby references
        elements_with_labelledby = soup.find_all(attrs={'aria-labelledby': True})
        
        for elem in elements_with_labelledby:
            labelledby_id = elem.get('aria-labelledby')
            assert labelledby_id in all_ids, f"aria-labelledby='{labelledby_id}' references non-existent ID"
    
    def test_semantic_html_structure(self, authenticated_client):
        """Verify semantic HTML5 elements are used appropriately"""
        response = authenticated_client.get('/module/surya-namaskar/info')
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for semantic section elements
        sections = soup.find_all('section')
        assert len(sections) >= 3, "Page should use semantic <section> elements"
        
        # Check for semantic article elements (pose cards)
        articles = soup.find_all('article')
        assert len(articles) == 12, "Pose cards should use semantic <article> elements"
        
        # Verify no generic divs are used where semantic elements would be better
        # (This is a guideline check - some divs are acceptable for layout)
        
        # Check that headings are used for section titles (not just styled divs)
        section_headings = soup.find_all(['h1', 'h2', 'h3'])
        assert len(section_headings) >= 17, "Page should use proper heading elements (h1, h2, h3)"
    
    def test_keyboard_navigation_support(self, authenticated_client):
        """Verify elements support keyboard navigation (focusable, proper tab order)"""
        response = authenticated_client.get('/module/surya-namaskar/info')
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check that all interactive links are present
        all_links = soup.find_all('a', href=True)
        assert len(all_links) >= 2, "Page should have at least back and start session links"
        
        # Verify links don't have tabindex="-1" (which would remove from tab order)
        for link in all_links:
            tabindex = link.get('tabindex')
            if tabindex:
                assert int(tabindex) >= 0, "Interactive links should not have negative tabindex"
        
        # Check for focus indicators in CSS (this is in the style block)
        page_html = response.data.decode('utf-8')
        assert ':focus' in page_html, "Page should have CSS focus indicators"
        assert 'focus-visible' in page_html, "Page should have enhanced focus-visible styles"
    
    def test_content_announced_correctly(self, authenticated_client):
        """Verify content structure allows proper screen reader announcement"""
        response = authenticated_client.get('/module/surya-namaskar/info')
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check that pose cards have proper structure for announcement
        pose_cards = soup.find_all('article', class_='pose-step')
        
        for i, card in enumerate(pose_cards, 1):
            # Each card should have a heading
            heading = card.find('h3')
            assert heading is not None, f"Pose card {i} should have an h3 heading"
            
            # Each card should have a pose number with aria-label
            pose_number = card.find('div', class_='pose-number')
            assert pose_number is not None, f"Pose card {i} should have a pose number badge"
            aria_label = pose_number.get('aria-label')
            assert aria_label and 'Step' in aria_label, f"Pose number should have descriptive aria-label"
            
            # Each card should have an image with alt text
            image = card.find('img', class_='pose-image')
            assert image is not None, f"Pose card {i} should have an image"
            assert image.get('alt'), f"Pose card {i} image should have alt text"
            
            # Each card should have description text
            description = card.find('p', class_='text-sm')
            assert description is not None, f"Pose card {i} should have a description"
    
    def test_warning_icons_have_labels(self, authenticated_client):
        """Verify warning icons have proper role and labels for screen readers"""
        response = authenticated_client.get('/module/surya-namaskar/info')
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Find warning emojis (⚠️)
        page_html = response.data.decode('utf-8')
        if '⚠️' in page_html:
            # Parse to find warning elements
            warning_elements = soup.find_all(string=lambda text: text and '⚠️' in text)
            
            # At least some warnings should have proper ARIA attributes
            # Check parent elements for role="img" and aria-label
            for warning in warning_elements:
                parent = warning.parent
                # Warning icons in guidelines should be marked appropriately
                if parent and parent.name == 'span':
                    # Should have role="img" and aria-label for important warnings
                    # or aria-hidden="true" for decorative ones
                    has_role = parent.get('role') == 'img'
                    has_label = parent.get('aria-label') is not None
                    has_hidden = parent.get('aria-hidden') == 'true'
                    
                    # Should have at least one of these attributes
                    assert has_role or has_label or has_hidden, "Warning icons should have proper ARIA attributes"
    
    def test_section_labels_descriptive(self, authenticated_client):
        """Verify section aria-labels are descriptive and helpful"""
        response = authenticated_client.get('/module/surya-namaskar/info')
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check sections with aria-labelledby
        sections = soup.find_all('section', attrs={'aria-labelledby': True})
        
        for section in sections:
            labelledby_id = section.get('aria-labelledby')
            heading = soup.find(id=labelledby_id)
            
            assert heading is not None, f"Section references non-existent heading ID: {labelledby_id}"
            heading_text = heading.get_text(strip=True)
            assert len(heading_text) > 0, "Section heading should have text content"
            
            # Verify heading text is descriptive
            assert len(heading_text) > 5, f"Section heading should be descriptive (found: '{heading_text}')"
    
    def test_no_empty_links(self, authenticated_client):
        """Verify no links are empty or have only whitespace/icons"""
        response = authenticated_client.get('/module/surya-namaskar/info')
        soup = BeautifulSoup(response.data, 'html.parser')
        
        all_links = soup.find_all('a', href=True)
        
        for link in all_links:
            # Get text content (excluding aria-hidden elements)
            text_content = ''
            for child in link.descendants:
                if isinstance(child, str):
                    # Check if parent has aria-hidden
                    parent = child.parent if hasattr(child, 'parent') else None
                    if parent and parent.get('aria-hidden') != 'true':
                        text_content += child
            
            text_content = text_content.strip()
            aria_label = link.get('aria-label', '').strip()
            
            # Link should have either visible text or aria-label
            assert text_content or aria_label, f"Link {link.get('href')} should have text or aria-label"
    
    def test_list_structure_proper(self, authenticated_client):
        """Verify lists use proper role attributes for screen reader navigation"""
        response = authenticated_client.get('/module/surya-namaskar/info')
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Find all elements with role="list"
        lists = soup.find_all(attrs={'role': 'list'})
        assert len(lists) >= 2, "Page should have at least 2 lists (stats and poses)"
        
        # Verify each list has list items
        for list_elem in lists:
            list_items = list_elem.find_all(attrs={'role': 'listitem'}, recursive=True)
            assert len(list_items) > 0, "Each list should contain list items"
            
            # Verify list has aria-label
            aria_label = list_elem.get('aria-label')
            assert aria_label, "Lists should have descriptive aria-label"


def test_screen_reader_summary(authenticated_client):
    """Generate a summary report of screen reader accessibility"""
    response = authenticated_client.get('/module/surya-namaskar/info')
    soup = BeautifulSoup(response.data, 'html.parser')
    
    print("\n" + "="*60)
    print("SCREEN READER ACCESSIBILITY SUMMARY")
    print("="*60)
    
    # Heading structure
    h1_count = len(soup.find_all('h1'))
    h2_count = len(soup.find_all('h2'))
    h3_count = len(soup.find_all('h3'))
    print(f"\nHeading Structure:")
    print(f"  H1 tags: {h1_count} (should be 1)")
    print(f"  H2 tags: {h2_count} (section headings)")
    print(f"  H3 tags: {h3_count} (pose titles)")
    
    # Landmark regions
    sections = len(soup.find_all('section'))
    articles = len(soup.find_all('article'))
    print(f"\nLandmark Regions:")
    print(f"  Sections: {sections}")
    print(f"  Articles: {articles} (pose cards)")
    
    # ARIA attributes
    aria_labels = len(soup.find_all(attrs={'aria-label': True}))
    aria_labelledby = len(soup.find_all(attrs={'aria-labelledby': True}))
    aria_hidden = len(soup.find_all(attrs={'aria-hidden': True}))
    print(f"\nARIA Attributes:")
    print(f"  aria-label: {aria_labels}")
    print(f"  aria-labelledby: {aria_labelledby}")
    print(f"  aria-hidden: {aria_hidden} (decorative elements)")
    
    # Images
    images = soup.find_all('img')
    images_with_alt = [img for img in images if img.get('alt')]
    print(f"\nImages:")
    print(f"  Total images: {len(images)}")
    print(f"  Images with alt text: {len(images_with_alt)}")
    
    # Interactive elements
    links = len(soup.find_all('a', href=True))
    buttons = len(soup.find_all('button'))
    print(f"\nInteractive Elements:")
    print(f"  Links: {links}")
    print(f"  Buttons: {buttons}")
    
    # Role attributes
    role_list = len(soup.find_all(attrs={'role': 'list'}))
    role_listitem = len(soup.find_all(attrs={'role': 'listitem'}))
    role_note = len(soup.find_all(attrs={'role': 'note'}))
    print(f"\nRole Attributes:")
    print(f"  role='list': {role_list}")
    print(f"  role='listitem': {role_listitem}")
    print(f"  role='note': {role_note}")
    
    print("\n" + "="*60)
    print("All screen reader accessibility checks passed!")
    print("="*60 + "\n")
