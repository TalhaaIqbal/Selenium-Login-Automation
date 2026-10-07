from dotenv import load_dotenv

import os

from logging_config import logger
from utils.random_delay import random_delay
from utils.init_driver import init_chrome_driver
from .utils.login import amazon_login
from .utils.search import search_products_links
from .utils.search import extract_product_details

query = "laptop"


def amazon_search():
    logger.info("Starting Amazon search process")

    load_dotenv()

    phone = os.getenv("AMAZON_PHONE")
    password = os.getenv("AMAZON_PASSWORD")
    url = os.getenv("AMAZON_URL")

    driver = init_chrome_driver()

    try:
        # Open website
        logger.info("Navigating to URL: %s", url)
        driver.get(url)
        random_delay(1, 2)
        

        # Call login function
        amazon_login(driver, phone, password)

        # Call search function to get product links
        results = search_products_links(driver, query)
        
        #Extract Product Details
        for result in results[:2]:
            product_details = extract_product_details(driver, result["link"])
            logger.info(product_details)
        
        input("Press Enter to continue...")

    except Exception:
        logger.exception("Amazon search failed")
        raise

    finally:
        logger.info("Closing WebDriver")
        driver.quit()
