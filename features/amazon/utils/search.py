import time
from urllib.parse import urljoin

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
from .get_text import get_text

CARD_SELECTOR = 'div[data-component-type="s-search-result"]'
OUTPUT_FILE = "amazon_search_results.csv"


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

                title = get_text(product, "h2")
                if not title:
                    continue  # not rendered yet, retried on the next sweep

                price = get_text(product, ".a-price:not(.a-text-price) .a-offscreen")
                rating = get_text(product, '[data-cy="reviews-block"] .a-icon-alt')

                try:
                    reviews = product.find_element(
                        By.CSS_SELECTOR, 'a[aria-label$="ratings"]'
                    ).get_attribute("aria-label")
                except NoSuchElementException:
                    reviews = None

                # only mark as seen once it was actually extracted
                seen_asins.add(asin)
                results.append({
                    "asin": asin,
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "reviews": reviews,
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


def save(results):
    pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)
    logger.info("Saved %s products to %s", len(results), OUTPUT_FILE)


def search_products(driver, query, wait_timeout=90, max_rounds=5):
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
    save(results)
    logger.info(f"Saved the results to {OUTPUT_FILE}")
    # driver.execute_script("window.scrollTo(0, 0);")
    random_delay(1, 2)

    # Now try to click "Show results" button for up to 5 times
    for round_num in range(1, max_rounds + 1):
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
        save(results)

    logger.info("Extracted %s unique products", len(results))
    return results