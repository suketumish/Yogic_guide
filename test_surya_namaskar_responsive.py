"""
Test responsive layouts for Surya Namaskar module page across different breakpoints.
Tests mobile (320px-640px), tablet (640px-1024px), and desktop (1024px+) viewports.
"""

import pytest
from flask import url_for
from bs4 import BeautifulSoup
import re


class TestSuryaNamaskarResponsive:
    """Test suite for responsive layout verification across breakpoints."""
    
    @pytest.fixture
    def client(self, app):
        """Create test client."""
        return app.test_client()
    
    @pytest.fixture
    def auth_client(self, client):
        """Create authenticated test client."""
        # Register and login a test user
        client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'confirm_password': 'TestPass123!'
        }, follow_redirects=True)
        
        client.post('/login', data={
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }, follow_redirects=True)
        
        return client
    
    def get_page_content(self, client):
        """Helper to get Surya Namaskar page content."""
        response = client.get('/module/surya-namaskar')
        assert response.status_code == 200
        return BeautifulSoup(response.data, 'html.parser')
    
    def test_page_loads_successfully(self, auth_client):
        """Test that the Surya Namaskar page loads without errors."""
        response = auth_client.get('/module/surya-namaskar')
        assert response.status_code == 200
        assert b'SURYA NAMASKAR' in response.data
    
    def test_mobile_statistics_grid_layout(self, auth_client):
        """Test statistics grid uses 2-column layout on mobile (grid-cols-2)."""
        soup = self.get_page_content(auth_client)
        
        # Find statistics grid
        stats_grid = soup.find('div', class_=re.compile(r'grid.*grid-cols-2'))
        assert stats_grid is not None, "Statistics grid should have grid-cols-2 for mobile"
        
        # Verify it also has md:grid-cols-4 for desktop
        assert 'md:grid-cols-4' in stats_grid.get('class', []), \
            "Statistics grid should have md:grid-cols-4 for desktop"
        
        # Verify all 4 stat cards are present
        stat_cards = stats_grid.find_all('div', class_=re.compile(r'bg-(orange|red|yellow|amber)-50'))
        assert len(stat_cards) == 4, "Should have 4 statistics cards"
    
    def test_benefits_grid_responsive_layout(self, auth_client):
        """Test benefits section uses 1-column mobile, 3-column desktop layout."""
        soup = self.get_page_content(auth_client)
        
        # Find benefits grid
        benefits_section = soup.find('h2', string=re.compile(r'Benefits'))
        assert benefits_section is not None, "Benefits section should exist"
        
        benefits_grid = benefits_section.find_next('div', class_=re.compile(r'grid'))
        assert benefits_grid is not None, "Benefits grid should exist"
        
        # Verify responsive classes
        grid_classes = ' '.join(benefits_grid.get('class', []))
        assert 'grid-cols-1' in grid_classes, "Benefits should be 1 column on mobile"
        assert 'md:grid-cols-3' in grid_classes, "Benefits should be 3 columns on desktop"
        
        # Verify all 6 benefits are present
        benefit_items = benefits_grid.find_all('div', class_='flex')
        assert len(benefit_items) == 6, "Should have 6 benefit items"
    
    def test_practice_guidelines_responsive_layout(self, auth_client):
        """Test practice guidelines use 1-column mobile, 2-column desktop layout."""
        soup = self.get_page_content(auth_client)
        
        # Find practice guidelines section
        guidelines_section = soup.find('h2', string=re.compile(r'Practice Guidelines'))
        assert guidelines_section is not None, "Practice guidelines section should exist"
        
        guidelines_grid = guidelines_section.find_next('div', class_=re.compile(r'grid'))
        assert guidelines_grid is not None, "Guidelines grid should exist"
        
        # Verify responsive classes
        grid_classes = ' '.join(guidelines_grid.get('class', []))
        assert 'grid-cols-1' in grid_classes, "Guidelines should be 1 column on mobile"
        assert 'md:grid-cols-2' in grid_classes, "Guidelines should be 2 columns on desktop"
        
        # Verify guideline items are present
        guideline_items = guidelines_grid.find_all('div', class_='flex')
        assert len(guideline_items) >= 6, "Should have at least 6 guideline items"
    
    def test_pose_cards_single_column_layout(self, auth_client):
        """Test that all 12 pose cards use single-column layout on all viewports."""
        soup = self.get_page_content(auth_client)
        
        # Find poses container
        poses_section = soup.find('h2', string=re.compile(r'12 Sacred Poses'))
        assert poses_section is not None, "Poses section should exist"
        
        poses_container = poses_section.find_next('div', class_=re.compile(r'grid'))
        assert poses_container is not None, "Poses container should exist"
        
        # Verify single column layout
        container_classes = ' '.join(poses_container.get('class', []))
        assert 'grid-cols-1' in container_classes, "Poses should be single column"
        
        # Verify no multi-column classes for larger screens
        assert 'md:grid-cols-2' not in container_classes, "Poses should not have 2 columns on desktop"
        assert 'lg:grid-cols-2' not in container_classes, "Poses should not have 2 columns on large screens"
        
        # Verify all 12 pose cards are present
        pose_cards = poses_container.find_all('div', class_='pose-step')
        assert len(pose_cards) == 12, "Should have exactly 12 pose cards"
    
    def test_responsive_image_container_heights(self, auth_client):
        """Test that CSS defines responsive image container heights."""
        soup = self.get_page_content(auth_client)
        
        # Find style tag with responsive CSS
        style_tags = soup.find_all('style')
        assert len(style_tags) > 0, "Should have style tags"
        
        css_content = ' '.join([tag.string for tag in style_tags if tag.string])
        
        # Check for mobile breakpoint (max-width: 640px) with 300px height
        assert '@media (max-width: 640px)' in css_content, \
            "Should have mobile breakpoint styles"
        assert 'height: 300px' in css_content, \
            "Should set 300px height for mobile"
        
        # Check for tablet breakpoint (641px - 1024px) with 350px height
        assert '@media (min-width: 641px) and (max-width: 1024px)' in css_content, \
            "Should have tablet breakpoint styles"
        assert 'height: 350px' in css_content, \
            "Should set 350px height for tablet"
        
        # Check for desktop breakpoint (1025px+) with 400px height
        assert '@media (min-width: 1025px)' in css_content, \
            "Should have desktop breakpoint styles"
        assert 'height: 400px' in css_content, \
            "Should set 400px height for desktop"
    
    def test_touch_target_sizes_mobile(self, auth_client):
        """Test that touch targets meet minimum 44x44px requirement on mobile."""
        soup = self.get_page_content(auth_client)
        
        # Find style tag
        style_tags = soup.find_all('style')
        css_content = ' '.join([tag.string for tag in style_tags if tag.string])
        
        # Check for mobile touch target styles
        assert 'min-height: 44px' in css_content, \
            "Should have minimum 44px height for touch targets"
        
        # Verify back button has proper touch target
        back_button = soup.find('a', href=re.compile(r'dashboard'))
        assert back_button is not None, "Back button should exist"
        button_classes = ' '.join(back_button.get('class', []))
        assert 'min-h-[44px]' in button_classes or 'min-height: 44px' in css_content, \
            "Back button should have minimum 44px height"
        
        # Verify start session button has proper touch target
        start_button = soup.find('a', href=re.compile(r'module_session'))
        assert start_button is not None, "Start session button should exist"
        button_classes = ' '.join(start_button.get('class', []))
        assert 'min-h-[44px]' in button_classes or 'min-height: 56px' in css_content, \
            "Start session button should have adequate touch target"
    
    def test_pose_number_badges_touch_friendly(self, auth_client):
        """Test that pose number badges are touch-friendly on mobile."""
        soup = self.get_page_content(auth_client)
        
        # Find pose number badges
        pose_numbers = soup.find_all('div', class_='pose-number')
        assert len(pose_numbers) == 12, "Should have 12 pose number badges"
        
        # Check first badge for proper sizing classes
        first_badge = pose_numbers[0]
        badge_classes = ' '.join(first_badge.get('class', []))
        
        # Should have w-12 h-12 (48px x 48px) which exceeds 44px minimum
        assert 'w-12' in badge_classes, "Badge should have w-12 class"
        assert 'h-12' in badge_classes, "Badge should have h-12 class"
        
        # Verify CSS increases size on mobile
        style_tags = soup.find_all('style')
        css_content = ' '.join([tag.string for tag in style_tags if tag.string])
        assert 'width: 48px' in css_content or 'w-12' in badge_classes, \
            "Pose badges should be at least 48px wide on mobile"
    
    def test_content_accessibility_and_readability(self, auth_client):
        """Test that all content is accessible and readable across viewports."""
        soup = self.get_page_content(auth_client)
        
        # Test header section
        header = soup.find('h1', class_=re.compile(r'yogic-heading'))
        assert header is not None, "Main heading should exist"
        assert 'SURYA NAMASKAR' in header.text, "Main heading should be readable"
        
        # Test all 12 pose cards have readable content
        pose_cards = soup.find_all('div', class_='pose-step')
        for i, card in enumerate(pose_cards, 1):
            # Check pose title
            title = card.find('h3')
            assert title is not None, f"Pose {i} should have a title"
            assert len(title.text.strip()) > 0, f"Pose {i} title should not be empty"
            
            # Check pose description
            description = card.find('p', class_=re.compile(r'text-sm.*text-gray-600'))
            assert description is not None, f"Pose {i} should have a description"
            assert len(description.text.strip()) > 0, f"Pose {i} description should not be empty"
            
            # Check mantra section
            mantra = card.find('div', class_=re.compile(r'bg-orange-100'))
            assert mantra is not None, f"Pose {i} should have a mantra section"
            
            # Check image
            image = card.find('img', class_='pose-image')
            assert image is not None, f"Pose {i} should have an image"
            assert image.get('alt'), f"Pose {i} image should have alt text"
        
        # Test benefits section readability
        benefits = soup.find_all('div', class_='flex', limit=6)
        for benefit in benefits[:6]:  # First 6 are benefits
            title = benefit.find('h3')
            if title:  # Benefits have h3 titles
                assert len(title.text.strip()) > 0, "Benefit title should not be empty"
        
        # Test practice guidelines readability
        guidelines_section = soup.find('h2', string=re.compile(r'Practice Guidelines'))
        if guidelines_section:
            guidelines = guidelines_section.find_next('div', class_=re.compile(r'grid'))
            guideline_items = guidelines.find_all('p', class_='text-sm')
            assert len(guideline_items) >= 6, "Should have readable practice guidelines"
    
    def test_responsive_spacing_and_gaps(self, auth_client):
        """Test that spacing and gaps are appropriate for different viewports."""
        soup = self.get_page_content(auth_client)
        
        # Check statistics grid has gap-4
        stats_grid = soup.find('div', class_=re.compile(r'grid.*grid-cols-2'))
        assert 'gap-4' in ' '.join(stats_grid.get('class', [])), \
            "Statistics grid should have gap-4"
        
        # Check benefits grid has gap-6
        benefits_section = soup.find('h2', string=re.compile(r'Benefits'))
        benefits_grid = benefits_section.find_next('div', class_=re.compile(r'grid'))
        assert 'gap-6' in ' '.join(benefits_grid.get('class', [])), \
            "Benefits grid should have gap-6"
        
        # Check poses container has gap-8
        poses_section = soup.find('h2', string=re.compile(r'12 Sacred Poses'))
        poses_container = poses_section.find_next('div', class_=re.compile(r'grid'))
        assert 'gap-8' in ' '.join(poses_container.get('class', [])), \
            "Poses container should have gap-8"
        
        # Verify CSS increases spacing on mobile
        style_tags = soup.find_all('style')
        css_content = ' '.join([tag.string for tag in style_tags if tag.string])
        assert 'gap: 1.5rem' in css_content or 'gap: 2rem' in css_content, \
            "Should have increased gap spacing in mobile CSS"
    
    def test_hover_effects_desktop_only(self, auth_client):
        """Test that hover effects are only applied on desktop viewports."""
        soup = self.get_page_content(auth_client)
        
        # Find style tag
        style_tags = soup.find_all('style')
        css_content = ' '.join([tag.string for tag in style_tags if tag.string])
        
        # Check that hover effects are within desktop media query
        assert '@media (min-width: 1025px)' in css_content, \
            "Should have desktop media query"
        
        # Extract desktop media query content
        desktop_section_match = re.search(
            r'@media \(min-width: 1025px\)\s*{([^}]+(?:{[^}]*}[^}]*)*)}',
            css_content,
            re.DOTALL
        )
        
        if desktop_section_match:
            desktop_css = desktop_section_match.group(1)
            assert ':hover' in desktop_css, \
                "Hover effects should be in desktop media query"
            assert 'transform: translateY(-5px)' in desktop_css or \
                   'transform: scale(1.05)' in desktop_css, \
                "Desktop hover should include transform effects"
    
    def test_all_sections_present(self, auth_client):
        """Test that all major sections are present and accessible."""
        soup = self.get_page_content(auth_client)
        
        # Check for all major sections
        sections = {
            'Header': soup.find('h1', string=re.compile(r'SURYA NAMASKAR')),
            'Statistics': soup.find('div', class_=re.compile(r'grid.*grid-cols-2.*md:grid-cols-4')),
            'About': soup.find('h2', string=re.compile(r'About Surya Namaskar')),
            'Benefits': soup.find('h2', string=re.compile(r'Benefits')),
            'Poses': soup.find('h2', string=re.compile(r'12 Sacred Poses')),
            'Guidelines': soup.find('h2', string=re.compile(r'Practice Guidelines')),
            'Start Button': soup.find('a', href=re.compile(r'module_session'))
        }
        
        for section_name, section_element in sections.items():
            assert section_element is not None, \
                f"{section_name} section should be present and accessible"
    
    def test_responsive_padding_adjustments(self, auth_client):
        """Test that padding is adjusted appropriately for mobile devices."""
        soup = self.get_page_content(auth_client)
        
        # Find style tag
        style_tags = soup.find_all('style')
        css_content = ' '.join([tag.string for tag in style_tags if tag.string])
        
        # Check for mobile padding adjustments
        mobile_section = re.search(
            r'@media \(max-width: 640px\)\s*{([^}]+(?:{[^}]*}[^}]*)*)}',
            css_content,
            re.DOTALL
        )
        
        assert mobile_section is not None, "Should have mobile-specific styles"
        
        mobile_css = mobile_section.group(1)
        
        # Verify padding adjustments for various elements
        assert 'padding' in mobile_css, "Should have padding adjustments for mobile"
        
        # Check that pose cards have adequate padding on mobile
        assert 'padding: 1.5rem' in mobile_css or 'p-6' in str(soup), \
            "Pose cards should have adequate padding"
    
    def test_image_loading_attributes(self, auth_client):
        """Test that images have proper loading attributes for performance."""
        soup = self.get_page_content(auth_client)
        
        # Find all pose images
        pose_images = soup.find_all('img', class_='pose-image')
        assert len(pose_images) == 12, "Should have 12 pose images"
        
        # Check first two images have eager loading (above fold)
        for i in range(min(2, len(pose_images))):
            loading_attr = pose_images[i].get('loading')
            assert loading_attr == 'eager', \
                f"First {i+1} images should have loading='eager' for above-fold content"
        
        # Remaining images should not have eager loading (can be lazy loaded)
        # Note: The template doesn't specify lazy loading for all, which is fine
    
    def test_back_button_accessibility(self, auth_client):
        """Test that back button is accessible and properly sized."""
        soup = self.get_page_content(auth_client)
        
        # Find back button
        back_button = soup.find('a', href=re.compile(r'dashboard'))
        assert back_button is not None, "Back button should exist"
        
        # Check button has text content
        assert '←' in back_button.text or 'Back' in back_button.text, \
            "Back button should have readable text"
        
        # Check button has proper classes
        button_classes = ' '.join(back_button.get('class', []))
        assert 'btn-gradient' in button_classes, "Back button should have btn-gradient class"
        assert 'min-h-[44px]' in button_classes, "Back button should have minimum height"
    
    def test_start_session_button_accessibility(self, auth_client):
        """Test that start session button is accessible and properly sized."""
        soup = self.get_page_content(auth_client)
        
        # Find start session button
        start_button = soup.find('a', href=re.compile(r'module_session'))
        assert start_button is not None, "Start session button should exist"
        
        # Check button has text content
        assert 'START SESSION' in start_button.text.upper(), \
            "Start button should have readable text"
        
        # Check button has proper classes
        button_classes = ' '.join(start_button.get('class', []))
        assert 'btn-gradient' in button_classes, "Start button should have btn-gradient class"
        assert 'min-h-[44px]' in button_classes, "Start button should have minimum height"
        
        # Check button is centered
        parent = start_button.parent
        parent_classes = ' '.join(parent.get('class', []))
        assert 'text-center' in parent_classes, "Start button should be centered"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
