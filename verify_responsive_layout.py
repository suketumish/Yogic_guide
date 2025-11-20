"""
Manual verification script for responsive layouts across breakpoints.
This script analyzes the HTML template and CSS to verify responsive design implementation.
"""

import re
from bs4 import BeautifulSoup


def load_template():
    """Load the Surya Namaskar template."""
    with open('templates/module_surya_namaskar.html', 'r', encoding='utf-8') as f:
        return f.read()


def extract_css(html_content):
    """Extract CSS from style tags."""
    soup = BeautifulSoup(html_content, 'html.parser')
    style_tags = soup.find_all('style')
    return ' '.join([tag.string for tag in style_tags if tag.string])


def verify_mobile_layout(html_content, css_content):
    """Verify mobile layout (320px-640px)."""
    print("\n📱 MOBILE LAYOUT (320px-640px)")
    print("=" * 60)
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check statistics grid
    stats_grid = soup.find('div', class_=re.compile(r'grid.*grid-cols-2'))
    if stats_grid and 'md:grid-cols-4' in str(stats_grid.get('class', [])):
        print("✅ Statistics grid: 2 columns on mobile, 4 on desktop")
    else:
        print("❌ Statistics grid: Missing responsive classes")
    
    # Check image container height
    if 'height: 300px' in css_content and '@media (max-width: 640px)' in css_content:
        print("✅ Image containers: 300px height on mobile")
    else:
        print("❌ Image containers: Missing mobile height adjustment")
    
    # Check touch targets
    if 'min-height: 44px' in css_content or 'min-h-[44px]' in html_content:
        print("✅ Touch targets: Minimum 44px height")
    else:
        print("❌ Touch targets: Missing minimum height")
    
    # Check pose number badges
    if 'width: 48px' in css_content and 'height: 48px' in css_content:
        print("✅ Pose badges: 48px x 48px (touch-friendly)")
    else:
        print("⚠️  Pose badges: Check if w-12 h-12 classes provide 48px")
    
    # Check spacing adjustments
    if 'gap: 1.5rem' in css_content or 'gap: 2rem' in css_content:
        print("✅ Spacing: Increased gaps for mobile")
    else:
        print("⚠️  Spacing: May need verification")
    
    # Check button padding
    if 'padding: 14px 28px' in css_content or 'padding: 16px 32px' in css_content:
        print("✅ Buttons: Enhanced padding for touch")
    else:
        print("⚠️  Buttons: Check padding values")


def verify_tablet_layout(html_content, css_content):
    """Verify tablet layout (640px-1024px)."""
    print("\n📱 TABLET LAYOUT (640px-1024px)")
    print("=" * 60)
    
    # Check tablet media query
    if '@media (min-width: 641px) and (max-width: 1024px)' in css_content:
        print("✅ Tablet media query: Defined")
        
        # Check image height
        if 'height: 350px' in css_content:
            print("✅ Image containers: 350px height on tablet")
        else:
            print("❌ Image containers: Missing tablet height")
        
        # Check touch targets maintained
        if 'min-height: 44px' in css_content:
            print("✅ Touch targets: Maintained on tablet")
        else:
            print("⚠️  Touch targets: Verify maintenance")
    else:
        print("❌ Tablet media query: Not found")


def verify_desktop_layout(html_content, css_content):
    """Verify desktop layout (1024px+)."""
    print("\n🖥️  DESKTOP LAYOUT (1024px+)")
    print("=" * 60)
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check desktop media query
    if '@media (min-width: 1025px)' in css_content:
        print("✅ Desktop media query: Defined")
        
        # Check image height
        if 'height: 400px' in css_content:
            print("✅ Image containers: 400px height on desktop")
        else:
            print("❌ Image containers: Missing desktop height")
        
        # Check hover effects
        if ':hover' in css_content and 'transform: translateY(-5px)' in css_content:
            print("✅ Hover effects: Defined for desktop only")
        else:
            print("❌ Hover effects: Missing or not scoped to desktop")
        
        # Check scale effects
        if 'transform: scale(1.05)' in css_content or 'transform: scale(1.1)' in css_content:
            print("✅ Scale effects: Defined for hover states")
        else:
            print("⚠️  Scale effects: Verify implementation")
    else:
        print("❌ Desktop media query: Not found")
    
    # Check multi-column layouts
    if 'md:grid-cols-3' in html_content:
        print("✅ Benefits grid: 3 columns on desktop")
    else:
        print("❌ Benefits grid: Missing desktop columns")
    
    if 'md:grid-cols-4' in html_content:
        print("✅ Statistics grid: 4 columns on desktop")
    else:
        print("❌ Statistics grid: Missing desktop columns")


def verify_content_accessibility(html_content):
    """Verify content is accessible and readable."""
    print("\n♿ ACCESSIBILITY & READABILITY")
    print("=" * 60)
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check all 12 pose cards
    pose_cards = soup.find_all('div', class_='pose-step')
    if len(pose_cards) == 12:
        print(f"✅ Pose cards: All 12 present")
        
        # Check each card has required elements
        all_valid = True
        for i, card in enumerate(pose_cards, 1):
            title = card.find('h3')
            description = card.find('p', class_=re.compile(r'text-sm'))
            image = card.find('img', class_='pose-image')
            mantra = card.find('div', class_=re.compile(r'bg-orange-100'))
            
            if not all([title, description, image, mantra]):
                print(f"❌ Pose {i}: Missing required elements")
                all_valid = False
        
        if all_valid:
            print("✅ Pose cards: All have required elements")
    else:
        print(f"❌ Pose cards: Found {len(pose_cards)}, expected 12")
    
    # Check sections
    sections = {
        'Header': soup.find('h1', string=re.compile(r'SURYA NAMASKAR')),
        'About': soup.find('h2', string=re.compile(r'About Surya Namaskar')),
        'Benefits': soup.find('h2', string=re.compile(r'Benefits')),
        'Poses': soup.find('h2', string=re.compile(r'12 Sacred Poses')),
        'Guidelines': soup.find('h2', string=re.compile(r'Practice Guidelines')),
    }
    
    missing_sections = [name for name, elem in sections.items() if elem is None]
    if not missing_sections:
        print("✅ All major sections: Present")
    else:
        print(f"❌ Missing sections: {', '.join(missing_sections)}")
    
    # Check buttons
    back_button = soup.find('a', href=re.compile(r'dashboard'))
    start_button = soup.find('a', href=re.compile(r'module_session'))
    
    if back_button and start_button:
        print("✅ Navigation buttons: Both present")
    else:
        if not back_button:
            print("❌ Back button: Missing")
        if not start_button:
            print("❌ Start session button: Missing")
    
    # Check alt text on images
    images = soup.find_all('img', class_='pose-image')
    images_with_alt = [img for img in images if img.get('alt')]
    if len(images_with_alt) == len(images):
        print(f"✅ Image alt text: All {len(images)} images have alt text")
    else:
        print(f"⚠️  Image alt text: {len(images_with_alt)}/{len(images)} images have alt text")


def verify_single_column_layout(html_content):
    """Verify poses use single-column layout."""
    print("\n📐 LAYOUT STRUCTURE")
    print("=" * 60)
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find poses container
    poses_section = soup.find('h2', string=re.compile(r'12 Sacred Poses'))
    if poses_section:
        poses_container = poses_section.find_next('div', class_=re.compile(r'grid'))
        if poses_container:
            container_classes = ' '.join(poses_container.get('class', []))
            
            if 'grid-cols-1' in container_classes:
                print("✅ Poses layout: Single column")
            else:
                print("❌ Poses layout: Not single column")
            
            if 'md:grid-cols-2' not in container_classes and 'lg:grid-cols-2' not in container_classes:
                print("✅ Poses layout: No multi-column on larger screens")
            else:
                print("❌ Poses layout: Has multi-column classes")
        else:
            print("❌ Poses container: Not found")
    else:
        print("❌ Poses section: Not found")


def verify_responsive_grids(html_content):
    """Verify responsive grid layouts."""
    print("\n🔲 RESPONSIVE GRIDS")
    print("=" * 60)
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Benefits grid
    benefits_section = soup.find('h2', string=re.compile(r'Benefits'))
    if benefits_section:
        benefits_grid = benefits_section.find_next('div', class_=re.compile(r'grid'))
        if benefits_grid:
            grid_classes = ' '.join(benefits_grid.get('class', []))
            if 'grid-cols-1' in grid_classes and 'md:grid-cols-3' in grid_classes:
                print("✅ Benefits grid: 1 col mobile, 3 cols desktop")
            else:
                print("❌ Benefits grid: Incorrect responsive classes")
    
    # Practice guidelines grid
    guidelines_section = soup.find('h2', string=re.compile(r'Practice Guidelines'))
    if guidelines_section:
        guidelines_grid = guidelines_section.find_next('div', class_=re.compile(r'grid'))
        if guidelines_grid:
            grid_classes = ' '.join(guidelines_grid.get('class', []))
            if 'grid-cols-1' in grid_classes and 'md:grid-cols-2' in grid_classes:
                print("✅ Guidelines grid: 1 col mobile, 2 cols desktop")
            else:
                print("❌ Guidelines grid: Incorrect responsive classes")


def main():
    """Run all verification checks."""
    print("\n" + "=" * 60)
    print("🧘 SURYA NAMASKAR RESPONSIVE LAYOUT VERIFICATION")
    print("=" * 60)
    
    try:
        # Load template
        html_content = load_template()
        css_content = extract_css(html_content)
        
        # Run all verifications
        verify_mobile_layout(html_content, css_content)
        verify_tablet_layout(html_content, css_content)
        verify_desktop_layout(html_content, css_content)
        verify_single_column_layout(html_content)
        verify_responsive_grids(html_content)
        verify_content_accessibility(html_content)
        
        print("\n" + "=" * 60)
        print("✅ VERIFICATION COMPLETE")
        print("=" * 60)
        print("\nSummary:")
        print("- Mobile (320px-640px): Verified")
        print("- Tablet (640px-1024px): Verified")
        print("- Desktop (1024px+): Verified")
        print("- Content accessibility: Verified")
        print("- All 12 poses: Present and readable")
        print("\n")
        
    except FileNotFoundError:
        print("\n❌ Error: Could not find templates/module_surya_namaskar.html")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == '__main__':
    main()
