import logging
import sys
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Add parent directory to path to import features module
sys.path.insert(0, str(Path(__file__).parent.parent))
from features.amazon.utils.search import extract_product_details

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# First 2 product links from CSV
test_links = [
    "https://www.amazon.com/dp/B0GPYBKBW6",
    "https://www.amazon.com/dp/B0GNBKLLBC"
]

def main():
    # Initialize Chrome WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        for i, link in enumerate(test_links, 1):
            logger.info("Testing product {}: {}".format(i, link))
            product_details = extract_product_details(driver, link)
            logger.info("Product {} details: {}".format(i, product_details))
            logger.info("-" * 80)

    finally:
        driver.quit()
        logger.info("WebDriver closed")

if __name__ == "__main__":
    main()
