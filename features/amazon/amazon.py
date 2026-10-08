from dotenv import load_dotenv

import os
import time

from logging_config import logger
from utils.random_delay import random_delay
from utils.init_driver import init_chrome_driver
from .utils.login import amazon_login
from .utils.search import search_products_links
from .utils.search import extract_product_details
from .utils.save.google_sheets import get_google_sheet, save_product


query = "laptop"


def amazon_search():
    logger.info("Starting Amazon search process")
    overall_start = time.time()

    load_dotenv()

    phone = os.getenv("AMAZON_PHONE")
    password = os.getenv("AMAZON_PASSWORD")
    url = os.getenv("AMAZON_URL")
    product_count = os.getenv("PRODUCT_COUNT")

    driver = init_chrome_driver()

    try:
        logger.warning("check")
        # Open website
        logger.info("Navigating to URL: %s", url)
        driver.get(url)
        random_delay(1, 2)

        # Call login function
        amazon_login(driver, phone, password)

        # Call search function to get product links
        search_start = time.time()
        product_links = search_products_links(driver, query)
        search_duration = time.time() - search_start
        logger.info("Search completed in %.2f seconds", search_duration)

        # Process product count if specified
        products_to_process = product_links[:int(product_count)] if product_count else product_links

        # Connect to Google Sheet once
        worksheet = get_google_sheet()

        # Extract Product Details
        extraction_start = time.time()


        for index, product_data in enumerate(products_to_process, start=1):
            product_link = product_data.get("link")

            logger.info("Processing product no. %s: %s", index, product_link)
            product_start = time.time()

            try:
                product = extract_product_details(driver, product_link)
                product_duration = time.time() - product_start
                logger.info("Product %s extracted in %.2f seconds", index, product_duration)

                if product:
                    save_product(worksheet, product)
                    logger.info("Product %s saved to Google Sheets", index)

            except Exception as e:
                product_duration = time.time() - product_start
                logger.error("Failed to process %s after %.2f seconds: %s", product_link, product_duration, e)

        extraction_duration = time.time() - extraction_start
        logger.info("Product details extraction completed in %.2f seconds", extraction_duration)

        overall_duration = time.time() - overall_start
        logger.info("Total execution time: %.2f seconds (%.2f minutes)", overall_duration, overall_duration / 60)

        input("Press Enter to continue...")

    except Exception:
        logger.exception("Amazon search failed")
        raise

    finally:
        logger.info("Closing WebDriver")
        driver.quit()