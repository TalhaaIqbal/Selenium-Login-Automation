"""
Test cases for selenium_template init_chrome_driver with different configurations.
Each test initializes the driver with different options, then closes it.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path so we can import from project root
sys.path.insert(0, str(Path(__file__).parent.parent))

import time
from selenium_template import init_chrome_driver
from logging_config import logger


def test_default_config():
    """Test 1: Default configuration with flags enabled."""
    logger.info("=" * 60)
    logger.info("TEST 1: Default configuration")
    logger.info("=" * 60)

    driver = init_chrome_driver(
        use_flags=True,
        use_user_agent=False,
        patch_webdriver_flag=False,
        headless=False,
        docker=False,
    )

    logger.info("Driver created successfully, waiting 2 seconds...")
    time.sleep(2)

    driver.quit()
    logger.info("Driver closed successfully")
    logger.info("")


def test_headless_mode():
    """Test 2: Headless mode (no UI)."""
    logger.info("=" * 60)
    logger.info("TEST 2: Headless mode")
    logger.info("=" * 60)

    driver = init_chrome_driver(
        use_flags=True,
        use_user_agent=False,
        patch_webdriver_flag=False,
        headless=True,
        docker=False,
    )

    logger.info("Driver created successfully, waiting 2 seconds...")
    time.sleep(2)

    driver.quit()
    logger.info("Driver closed successfully")
    logger.info("")


def test_matched_user_agent():
    """Test 3: With matched user agent."""
    logger.info("=" * 60)
    logger.info("TEST 3: Matched user agent")
    logger.info("=" * 60)

    driver = init_chrome_driver(
        use_flags=True,
        use_user_agent=True,
        ua_mode="matched",
        patch_webdriver_flag=False,
        headless=False,
        docker=False,
    )

    logger.info("Driver created successfully, waiting 2 seconds...")
    time.sleep(2)

    driver.quit()
    logger.info("Driver closed successfully")
    logger.info("")


def test_random_user_agent():
    """Test 4: With random user agent."""
    logger.info("=" * 60)
    logger.info("TEST 4: Random user agent")
    logger.info("=" * 60)

    driver = init_chrome_driver(
        use_flags=True,
        use_user_agent=True,
        ua_mode="random",
        patch_webdriver_flag=False,
        headless=False,
        docker=False,
    )

    logger.info("Driver created successfully, waiting 2 seconds...")
    time.sleep(2)

    driver.quit()
    logger.info("Driver closed successfully")
    logger.info("")


def test_no_flags():
    """Test 5: Without any flags (minimal configuration)."""
    logger.info("=" * 60)
    logger.info("TEST 5: No flags (minimal)")
    logger.info("=" * 60)

    driver = init_chrome_driver(
        use_flags=False,
        use_user_agent=False,
        patch_webdriver_flag=False,
        headless=False,
        docker=False,
    )

    logger.info("Driver created successfully, waiting 2 seconds...")
    time.sleep(2)

    driver.quit()
    logger.info("Driver closed successfully")
    logger.info("")


def test_headless_with_user_agent():
    """Test 6: Headless mode with matched user agent."""
    logger.info("=" * 60)
    logger.info("TEST 6: Headless + matched user agent")
    logger.info("=" * 60)

    driver = init_chrome_driver(
        use_flags=True,
        use_user_agent=True,
        ua_mode="matched",
        patch_webdriver_flag=False,
        headless=True,
        docker=False,
    )

    logger.info("Driver created successfully, waiting 2 seconds...")
    time.sleep(2)

    driver.quit()
    logger.info("Driver closed successfully")
    logger.info("")


def test_with_webdriver_patch():
    """Test 7: With webdriver patch enabled."""
    logger.info("=" * 60)
    logger.info("TEST 7: With webdriver patch")
    logger.info("=" * 60)

    driver = init_chrome_driver(
        use_flags=True,
        use_user_agent=False,
        patch_webdriver_flag=True,
        headless=False,
        docker=False,
    )

    logger.info("Driver created successfully, waiting 2 seconds...")
    time.sleep(2)

    driver.quit()
    logger.info("Driver closed successfully")
    logger.info("")


def test_all_options():
    """Test 8: All options enabled (except proxy/profile)."""
    logger.info("=" * 60)
    logger.info("TEST 8: All options enabled")
    logger.info("=" * 60)

    driver = init_chrome_driver(
        use_flags=True,
        use_user_agent=True,
        ua_mode="matched",
        patch_webdriver_flag=True,
        headless=False,
        docker=False,
    )

    logger.info("Driver created successfully, waiting 2 seconds...")
    time.sleep(2)

    driver.quit()
    logger.info("Driver closed successfully")
    logger.info("")


def run_all_tests():
    """Run all test cases sequentially."""
    logger.info("\n" + "=" * 60)
    logger.info("STARTING ALL DRIVER CONFIGURATION TESTS")
    logger.info("=" * 60 + "\n")

    test_default_config()
    test_headless_mode()
    test_matched_user_agent()
    test_random_user_agent()
    test_no_flags()
    test_headless_with_user_agent()
    test_with_webdriver_patch()
    test_all_options()

    logger.info("=" * 60)
    logger.info("ALL TESTS COMPLETED")
    logger.info("=" * 60)


if __name__ == "__main__":
    run_all_tests()
