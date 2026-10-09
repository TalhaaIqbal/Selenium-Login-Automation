import sys
import os

# Change to project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(project_root)

# Add parent directory to path to import modules
sys.path.insert(0, project_root)

from selenium_template.init_driver import init_chrome_driver
from logging_config import logger
import time


def test_init_driver_with_proxy():
    """Test init_chrome_driver with use_proxy=True"""
    logger.info("Test 1: Initializing driver with proxy")
    
    custom_url = "https://www.myip.com"
    
    try:
        # Import build_proxy_url to see which proxy is configured
        from selenium_template.proxy.proxy import build_proxy_url
        selected_proxy = build_proxy_url()

        if selected_proxy:
            logger.info(f"Selected proxy from env: {selected_proxy}")
        else:
            logger.warning("No proxy configured in env - test will run without proxy")

        driver = init_chrome_driver(use_proxy=True)
        logger.info("Driver initialized with proxy successfully")
        
        logger.info(f"Navigating to custom URL: {custom_url}")
        driver.get(custom_url)
        
        logger.info(f"Current URL: {driver.current_url}")
        logger.info(f"Page title: {driver.title}")
        
        # Take screenshot for debugging
        # driver.save_screenshot("proxy_test_screenshot.png")
        logger.info("Screenshot saved as proxy_test_screenshot.png")
        
        time.sleep(3)
        input("enter")
        
        driver.quit()
        logger.info("Driver closed successfully")
        
    except Exception as e:
        logger.error(f"Test with proxy failed: {e}")
        raise


def test_init_driver_without_proxy():
    """Test init_chrome_driver with use_proxy=False"""
    logger.info("Test 2: Initializing driver without proxy")
    
    custom_url = "https://www.myip.com"
    
    try:
        driver = init_chrome_driver(use_proxy=False)
        logger.info("Driver initialized without proxy successfully")
        
        logger.info(f"Navigating to custom URL: {custom_url}")
        driver.get(custom_url)
        
        logger.info(f"Current URL: {driver.current_url}")
        logger.info(f"Page title: {driver.title}")
        
        time.sleep(3)
        
        driver.quit()
        logger.info("Driver closed successfully")
        
    except Exception as e:
        logger.error(f"Test without proxy failed: {e}")
        raise


def test_init_driver_with_specific_proxy():
    """Test init_chrome_driver with a specific proxy override"""
    logger.info("Test 3: Initializing driver with specific proxy")
    
    custom_url = "http://httpbin.org/ip"  # Simple HTTP endpoint for testing
    
    # Use a public proxy for testing (or replace with your own)
    # Format: http://ip:port or http://user:pass@ip:port
    test_proxy = "http://162.55.8.72:3128"  # Example public proxy
    
    try:
        logger.info(f"Using specific proxy: {test_proxy}")
        driver = init_chrome_driver(use_proxy=True, proxy=test_proxy)
        logger.info("Driver initialized with specific proxy successfully")
        
        logger.info(f"Navigating to custom URL: {custom_url}")
        driver.get(custom_url)
        
        logger.info(f"Current URL: {driver.current_url}")
        logger.info(f"Page title: {driver.title}")
        
        # Log page source to see response
        logger.info(f"Page source snippet: {driver.page_source[:500]}")
        
        time.sleep(3)
        
        driver.quit()
        logger.info("Driver closed successfully")
        
    except Exception as e:
        logger.error(f"Test with specific proxy failed: {e}")
        raise


if __name__ == "__main__":
    logger.info("Starting proxy configuration tests")
    
    # Custom URL variable
    custom_url = "https://www.myip.com"
    logger.info(f"Custom URL configured: {custom_url}")
    
    try:
        # Test with proxy
        test_init_driver_with_proxy()
        
        # Test without proxy
        test_init_driver_without_proxy()
        
        # Test with specific proxy (optional - requires valid proxy)
        # test_init_driver_with_specific_proxy()
        
        logger.info("All tests completed successfully")
        
    except Exception as e:
        logger.error(f"Test suite failed: {e}")
        sys.exit(1)
