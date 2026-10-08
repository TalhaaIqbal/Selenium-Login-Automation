import time
import os
from urllib.parse import urljoin
from dotenv import load_dotenv

import pandas as pd
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from logging_config import logger
from utils.random_delay import random_delay
from utils.type_slowly import type_slowly
from .product.get_price import get_price
from .product.get_review_related import get_reviews
from .product.get_specs import get_product_specs
from .product.get_about_this_item import get_about_this_item
from .product.get_images import get_product_images
from .product.get_detailed_info import get_product_information

from .save.save_links import save_links


load_dotenv()


CARD_SELECTOR = 'div[data-component-type="s-search-result"]'
WAIT_TIMEOUT = int(os.getenv("WAIT_TIMEOUT", "90"))
CRAWL_SHOW_RESULT_ROUNDS = int(os.getenv("CRAWL_SHOW_RESULT_ROUNDS", "0"))
LINK_OUTPUT_FILE = "amazon_search_link_results.csv"


def card_asins(driver):
    asins = set()
    for card in driver.find_elements(By.CSS_SELECTOR, CARD_SELECTOR):
        try:
            asin = card.get_attribute("data-asin")
        except StaleElementReferenceException:
            continue
        if asin:
            asins.add(asin)
    return asins


def extract_to_bottom(driver, results, seen_asins):
    """Scroll from the current position down to the bottom, extracting cards
    as they render. Returns how many new products were added."""
    added = 0

    while True:
        driver.execute_script("window.scrollBy(0, 500);")
        random_delay(0.3, 0.6)

        for product in driver.find_elements(By.CSS_SELECTOR, CARD_SELECTOR):
            try:
                asin = product.get_attribute("data-asin")
                if not asin or asin in seen_asins:
                    continue

                # bring the card on screen so Amazon renders it
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", product
                )
                random_delay(0.2, 0.4)

                seen_asins.add(asin)
                results.append({
                    "link": urljoin(driver.current_url, f"/dp/{asin}"),
                })
                added += 1

            except StaleElementReferenceException:
                continue

        at_bottom = driver.execute_script(
            "return window.innerHeight + window.scrollY >= document.body.scrollHeight - 1200"
        )
        if at_bottom:
            break

    return added


def click_show_results(driver):
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//span[contains(normalize-space(), 'Show more results')]/ancestor::span[contains(@class, 's-show-more-results-button')]//input"
                )
            )
        )

        button.click()
        logger.info("Clicked 'Show results' button")
        random_delay(2, 3)
        return True
    except Exception:
        return False



def search_products_links(driver, query, wait_timeout=WAIT_TIMEOUT, CRAWL_SHOW_RESULT_ROUNDS=CRAWL_SHOW_RESULT_ROUNDS):
    logger.info("Starting product search for: %s", query)

    search_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#twotabsearchtextbox"))
    )
    search_box.click()

    logger.info("Entering search query")
    type_slowly(search_box, query)
    search_box.send_keys(Keys.ENTER)

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, CARD_SELECTOR))
    )

    results = []
    seen_asins = set()

    added = extract_to_bottom(driver, results, seen_asins)
    logger.info("Initial pass: +%s new, %s total", added, len(results))
    save_links(results)
    logger.info(f"Saved the results to {LINK_OUTPUT_FILE}")

    random_delay(1, 2)

    # click "Show results" button for up to CRAWL_SHOW_RESULT_ROUNDS times
    for round_num in range(1, CRAWL_SHOW_RESULT_ROUNDS + 1):
        known = card_asins(driver)

        # Try to auto-click the "Show results" button
        if not click_show_results(driver):
            logger.info("No 'Show results' button found, stopping")
            break

        # Wait for new products to appear after clicking
        deadline = time.time() + wait_timeout
        while time.time() < deadline:
            if card_asins(driver) - known:
                random_delay(2, 3)  # let the new batch settle
                break
            time.sleep(1)
        else:
            logger.info("No new products appeared after clicking, stopping")
            break

        # Extract new products that appeared
        added = extract_to_bottom(driver, results, seen_asins)
        logger.info(
            "Round %s: +%s new, %s total", round_num, added, len(results)
        )
        save_links(results)


    logger.info("Extracted %s unique products", len(results))
    return results



def extract_product_details(driver, product_link):
    logger.info("Extracting product details from links")
    driver.get(product_link)
    
    # Wait for the page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#productTitle"))
    )
    
    # Extract product details
    title_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#productTitle")
        )
    )
    title = title_element.text.strip()

    product_price = get_price(driver)
    product_reviews = get_reviews(driver)
    product_specs = get_product_specs(driver)
    product_about = get_about_this_item(driver)
    product_images = get_product_images(driver)
    product_detailed_info = get_product_information(driver)
    
    
    return {
        "title": title,
        "price": product_price,
        "rating": product_reviews["rating"],
        "review_count": product_reviews["review_count"],
        "asin": product_reviews["asin"],
        "overview_specs": product_specs,
        "about": product_about,
        "detailed_info": product_detailed_info,
        "images": product_images,
        "link": product_link
    }
    