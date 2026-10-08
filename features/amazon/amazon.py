from dotenv import load_dotenv

import os
import pandas as pd

from logging_config import logger
from utils.random_delay import random_delay
from utils.init_driver import init_chrome_driver
from .utils.login import amazon_login
from .utils.search import search_products_links
from .utils.search import extract_product_details
from .utils.save.google_sheets import get_google_sheet, save_product
from .utils.save.save_results import save_results
from .utils.save.save_links import save_links
from .utils.exception_check.get_completed_asins import get_completed_asins


query = "laptop"
LINK_RESULTS_CSV = "amazon_search_link_results.csv"


def get_existing_link_results():
    """Read existing link results from CSV if it exists."""
    if not os.path.exists(LINK_RESULTS_CSV):
        return None

    try:
        df = pd.read_csv(LINK_RESULTS_CSV)
        if df.empty:
            return None
        return df.to_dict('records')
    except Exception as e:
        logger.warning("Error reading link results CSV: %s", e)
        return None


def module_init_driver():
    """Module 1: Initialize Chrome WebDriver."""
    logger.info("Module 1: Initializing Chrome WebDriver")
    return init_chrome_driver()


def module_navigate_and_login(driver, url, phone, password):
    """Module 2: Navigate to Amazon and login."""
    logger.info("Module 2: Navigating to Amazon and logging in")

    logger.info("Navigating to URL: %s", url)
    driver.get(url)

    logger.info("Starting login process")
    amazon_login(driver, phone, password)
    logger.info("Login successful")


def module_get_product_links(driver, query, results_csv):
    """Module 3: Get product links (from existing CSV or search)."""
    logger.info("Module 3: Getting product links")

    existing_links = get_existing_link_results()
    completed_asins = get_completed_asins(results_csv)
    logger.info("Already completed ASINs: %s", len(completed_asins))

    if existing_links:
        logger.info("Found existing link results with %s products", len(existing_links))

        remaining_products = []
        for product_data in existing_links:
            product_link = product_data.get("link")

            if not product_link:
                continue

            asin = product_data.get("asin")

            if not asin:
                asin = product_link.rstrip("/").split("/")[-1]

            product_data["asin"] = asin

            if asin in completed_asins:
                logger.info("Skipping already completed ASIN: %s", asin)
                continue

            remaining_products.append(product_data)

        product_links = remaining_products
        logger.info("Remaining products from existing links: %s", len(product_links))
    else:
        logger.info("No existing link results found, running search")
        product_links = search_products_links(driver, query)
        save_links(product_links)
        logger.info("Search completed, saved %s product links", len(product_links))

    return product_links, completed_asins


def module_process_products(driver, product_links, worksheet, completed_asins, product_count=None):
    """Module 4: Process and extract product details."""
    logger.info("Module 4: Processing products")

    logger.info("Total products to process: %s", len(product_links))

    if product_count:
        product_count = int(product_count)
        products_to_process = product_links[:product_count]
    else:
        products_to_process = product_links

    logger.info("Products to process this run: %s", len(products_to_process))

    for index, product_data in enumerate(products_to_process, start=1):
        product_link = product_data.get("link")
        asin = product_data.get("asin")

        if not asin:
            asin = product_link.rstrip("/").split("/")[-1]
            product_data["asin"] = asin

        logger.info("Processing product no. %s | ASIN: %s | URL: %s", index, asin, product_link)

        try:
            product = extract_product_details(driver, product_link)

            if product:
                save_product(worksheet, product)
                save_results([product])
                completed_asins.add(asin)
                logger.info("Product %s saved to Google Sheets and CSV", index)

        except Exception as e:
            logger.error("Failed to process ASIN %s: %s", asin, e)
            continue


def module_cleanup(driver):
    """Module 5: Cleanup - close driver."""
    logger.info("Module 5: Closing WebDriver")
    driver.quit()


def amazon_search():
    """Main function to run all modules in sequence."""
    logger.info("Starting Amazon search process")

    load_dotenv()

    phone = os.getenv("AMAZON_PHONE")
    password = os.getenv("AMAZON_PASSWORD")
    url = os.getenv("AMAZON_URL")
    product_count = os.getenv("PRODUCT_COUNT")
    results_csv = os.getenv("RESULTS_CSV", "amazon_search_results.csv")

    driver = None

    try:
        # Module 1: Initialize driver
        driver = module_init_driver()

        # Module 2: Navigate and login
        module_navigate_and_login(driver, url, phone, password)

        # Module 3: Get product links
        product_links, completed_asins = module_get_product_links(driver, query, results_csv)

        # Module 4: Process products
        worksheet = get_google_sheet()
        module_process_products(driver, product_links, worksheet, completed_asins, product_count)

        input("Press Enter to continue...")

    except Exception:
        logger.exception("Amazon search failed")
        raise

    finally:
        # Module 5: Cleanup
        if driver:
            module_cleanup(driver)

