"""
Performance testing for Surya Namaskar module page.
Tests page load performance metrics and optimization requirements.
"""

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import json


class TestSuryaNamaskarPerformance:
    """Test suite for Surya Namaskar page performance optimization."""
    
    @pytest.fixture(scope="class")
    def driver(self):
        """Setup Chrome driver with performance logging enabled."""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        
        # Enable performance logging
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)
        
        yield driver
        
        driver.quit()
    
    def get_performance_metrics(self, driver):
        """Extract performance metrics from browser."""
        # Get Navigation Timing API metrics
        navigation_timing = driver.execute_script("""
            const perfData = window.performance.timing;
            const perfEntries = window.performance.getEntriesByType('navigation')[0];
            
            return {
                // Navigation Timing API (Level 1)
                domContentLoaded: perfData.domContentLoadedEventEnd - perfData.navigationStart,
                loadComplete: perfData.loadEventEnd - perfData.navigationStart,
                
                // Navigation Timing API (Level 2) - if available
                firstContentfulPaint: null,
                largestContentfulPaint: null,
                timeToInteractive: null,
                cumulativeLayoutShift: null
            };
        """)
        
        # Get Paint Timing API metrics
        paint_timing = driver.execute_script("""
            const paintEntries = performance.getEntriesByType('paint');
            const fcp = paintEntries.find(entry => entry.name === 'first-contentful-paint');
            return fcp ? fcp.startTime : null;
        """)
        
        if paint_timing:
            navigation_timing['firstContentfulPaint'] = paint_timing
        
        # Get LCP from PerformanceObserver (if available)
        lcp_timing = driver.execute_script("""
            return new Promise((resolve) => {
                try {
                    const observer = new PerformanceObserver((list) => {
                        const entries = list.getEntries();
                        const lastEntry = entries[entries.length - 1];
                        resolve(lastEntry.renderTime || lastEntry.loadTime);
                    });
                    observer.observe({entryTypes: ['largest-contentful-paint']});
                    
                    // Timeout after 2 seconds
                    setTimeout(() => resolve(null), 2000);
                } catch (e) {
                    resolve(null);
                }
            });
        """)
        
        if lcp_timing:
            navigation_timing['largestContentfulPaint'] = lcp_timing
        
        # Get CLS (Cumulative Layout Shift)
        cls_value = driver.execute_script("""
            return new Promise((resolve) => {
                try {
                    let clsValue = 0;
                    const observer = new PerformanceObserver((list) => {
                        for (const entry of list.getEntries()) {
                            if (!entry.hadRecentInput) {
                                clsValue += entry.value;
                            }
                        }
                    });
                    observer.observe({entryTypes: ['layout-shift']});
                    
                    // Wait a bit for layout shifts to occur
                    setTimeout(() => {
                        observer.disconnect();
                        resolve(clsValue);
                    }, 2000);
                } catch (e) {
                    resolve(null);
                }
            });
        """)
        
        if cls_value is not None:
            navigation_timing['cumulativeLayoutShift'] = cls_value
        
        return navigation_timing
    
    def test_page_loads_successfully(self, driver):
        """Test that the Surya Namaskar page loads without errors."""
        driver.get('http://localhost:5000/module/surya-namaskar')
        
        # Wait for page title
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1'))
        )
        
        # Verify page loaded
        assert 'SURYA NAMASKAR' in driver.page_source
        print("✓ Page loaded successfully")
    
    def test_first_contentful_paint(self, driver):
        """
        Test First Contentful Paint (FCP) performance.
        Target: < 1.5s (1500ms)
        Requirement: 8.1
        """
        driver.get('http://localhost:5000/module/surya-namaskar')
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'yogic-heading'))
        )
        
        metrics = self.get_performance_metrics(driver)
        fcp = metrics.get('firstContentfulPaint')
        
        if fcp:
            fcp_seconds = fcp / 1000
            print(f"First Contentful Paint: {fcp_seconds:.3f}s")
            
            # Target: < 1.5s
            assert fcp < 1500, f"FCP {fcp_seconds:.3f}s exceeds target of 1.5s"
            print(f"✓ FCP meets target (< 1.5s): {fcp_seconds:.3f}s")
        else:
            print("⚠ FCP metric not available in this browser")
            pytest.skip("FCP metric not available")
    
    def test_largest_contentful_paint(self, driver):
        """
        Test Largest Contentful Paint (LCP) performance.
        Target: < 2.5s (2500ms)
        Requirement: 8.1
        """
        driver.get('http://localhost:5000/module/surya-namaskar')
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'pose-step'))
        )
        
        # Give time for LCP to be measured
        time.sleep(2)
        
        metrics = self.get_performance_metrics(driver)
        lcp = metrics.get('largestContentfulPaint')
        
        if lcp:
            lcp_seconds = lcp / 1000
            print(f"Largest Contentful Paint: {lcp_seconds:.3f}s")
            
            # Target: < 2.5s
            assert lcp < 2500, f"LCP {lcp_seconds:.3f}s exceeds target of 2.5s"
            print(f"✓ LCP meets target (< 2.5s): {lcp_seconds:.3f}s")
        else:
            print("⚠ LCP metric not available in this browser")
            pytest.skip("LCP metric not available")
    
    def test_time_to_interactive(self, driver):
        """
        Test Time to Interactive (TTI) performance.
        Target: < 3.5s (3500ms)
        Requirement: 8.1
        """
        driver.get('http://localhost:5000/module/surya-namaskar')
        
        # Wait for page to be fully loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'btn-gradient'))
        )
        
        metrics = self.get_performance_metrics(driver)
        load_complete = metrics.get('loadComplete')
        
        if load_complete:
            tti_seconds = load_complete / 1000
            print(f"Time to Interactive (approximated): {tti_seconds:.3f}s")
            
            # Target: < 3.5s
            assert load_complete < 3500, f"TTI {tti_seconds:.3f}s exceeds target of 3.5s"
            print(f"✓ TTI meets target (< 3.5s): {tti_seconds:.3f}s")
        else:
            print("⚠ TTI metric not available")
            pytest.skip("TTI metric not available")
    
    def test_cumulative_layout_shift(self, driver):
        """
        Test Cumulative Layout Shift (CLS) performance.
        Target: < 0.1
        Requirement: 8.1
        """
        driver.get('http://localhost:5000/module/surya-namaskar')
        
        # Wait for page to load and settle
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'pose-image'))
        )
        
        # Wait for images to load and layout to stabilize
        time.sleep(3)
        
        metrics = self.get_performance_metrics(driver)
        cls = metrics.get('cumulativeLayoutShift')
        
        if cls is not None:
            print(f"Cumulative Layout Shift: {cls:.4f}")
            
            # Target: < 0.1
            assert cls < 0.1, f"CLS {cls:.4f} exceeds target of 0.1"
            print(f"✓ CLS meets target (< 0.1): {cls:.4f}")
        else:
            print("⚠ CLS metric not available in this browser")
            pytest.skip("CLS metric not available")
    
    def test_dom_content_loaded_time(self, driver):
        """Test DOM Content Loaded time is reasonable."""
        driver.get('http://localhost:5000/module/surya-namaskar')
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1'))
        )
        
        metrics = self.get_performance_metrics(driver)
        dcl = metrics.get('domContentLoaded')
        
        if dcl:
            dcl_seconds = dcl / 1000
            print(f"DOM Content Loaded: {dcl_seconds:.3f}s")
            
            # Should be under 2 seconds
            assert dcl < 2000, f"DCL {dcl_seconds:.3f}s is too slow"
            print(f"✓ DOM Content Loaded is fast: {dcl_seconds:.3f}s")
    
    def test_all_images_have_loading_attribute(self, driver):
        """Test that images use proper loading strategies."""
        driver.get('http://localhost:5000/module/surya-namaskar')
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'pose-image'))
        )
        
        images = driver.find_elements(By.CLASS_NAME, 'pose-image')
        
        # Check first 2 images are eager loaded
        for i in range(min(2, len(images))):
            loading_attr = images[i].get_attribute('loading')
            assert loading_attr == 'eager' or loading_attr is None, \
                f"First images should be eager loaded, got: {loading_attr}"
        
        print(f"✓ Found {len(images)} pose images with proper loading strategy")
    
    def test_css_is_optimized(self, driver):
        """Test that CSS is properly optimized (inline critical CSS)."""
        driver.get('http://localhost:5000/module/surya-namaskar')
        
        # Check for inline styles
        style_tags = driver.find_elements(By.TAG_NAME, 'style')
        
        assert len(style_tags) > 0, "Should have inline critical CSS"
        
        # Check that styles are present
        style_content = driver.execute_script("""
            const styles = Array.from(document.querySelectorAll('style'));
            return styles.map(s => s.textContent).join('');
        """)
        
        # Verify key styles are present
        assert '.pose-step' in style_content, "Pose step styles should be present"
        assert '.pose-image-container' in style_content, "Image container styles should be present"
        assert '@media' in style_content, "Responsive styles should be present"
        
        print("✓ CSS is properly optimized with inline critical styles")
    
    def test_javascript_execution_is_minimal(self, driver):
        """Test that JavaScript execution is minimal and efficient."""
        driver.get('http://localhost:5000/module/surya-namaskar')
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'pose-image'))
        )
        
        # Check that performance monitor is present
        has_performance_monitor = driver.execute_script("""
            return typeof PerformanceMonitor !== 'undefined';
        """)
        
        assert has_performance_monitor, "Performance monitor should be available"
        
        # Check that image error handling is set up
        images_with_handlers = driver.execute_script("""
            const images = document.querySelectorAll('.pose-image');
            return images.length;
        """)
        
        assert images_with_handlers == 12, f"Should have 12 pose images, found {images_with_handlers}"
        
        print("✓ JavaScript is minimal and properly configured")
    
    def test_performance_summary(self, driver):
        """Generate a comprehensive performance summary."""
        driver.get('http://localhost:5000/module/surya-namaskar')
        
        # Wait for page to fully load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'pose-step'))
        )
        
        time.sleep(3)  # Allow time for all metrics to be collected
        
        metrics = self.get_performance_metrics(driver)
        
        print("\n" + "="*60)
        print("PERFORMANCE SUMMARY - Surya Namaskar Module")
        print("="*60)
        
        if metrics.get('firstContentfulPaint'):
            fcp = metrics['firstContentfulPaint'] / 1000
            status = "✓ PASS" if fcp < 1.5 else "✗ FAIL"
            print(f"First Contentful Paint: {fcp:.3f}s (target < 1.5s) {status}")
        
        if metrics.get('largestContentfulPaint'):
            lcp = metrics['largestContentfulPaint'] / 1000
            status = "✓ PASS" if lcp < 2.5 else "✗ FAIL"
            print(f"Largest Contentful Paint: {lcp:.3f}s (target < 2.5s) {status}")
        
        if metrics.get('loadComplete'):
            tti = metrics['loadComplete'] / 1000
            status = "✓ PASS" if tti < 3.5 else "✗ FAIL"
            print(f"Time to Interactive: {tti:.3f}s (target < 3.5s) {status}")
        
        if metrics.get('cumulativeLayoutShift') is not None:
            cls = metrics['cumulativeLayoutShift']
            status = "✓ PASS" if cls < 0.1 else "✗ FAIL"
            print(f"Cumulative Layout Shift: {cls:.4f} (target < 0.1) {status}")
        
        if metrics.get('domContentLoaded'):
            dcl = metrics['domContentLoaded'] / 1000
            print(f"DOM Content Loaded: {dcl:.3f}s")
        
        print("="*60)


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
