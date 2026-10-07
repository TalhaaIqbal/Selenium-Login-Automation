import pandas as pd
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from logging_config import logger
from utils.random_delay import random_delay
from utils.type_slowly import type_slowly
from .get_text import get_text


def scroll_to_bottom(driver, steps=6):
    for _ in range(steps):
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight / arguments[0]);", steps)
        random_delay(0.5, 1.2)
        

def search_products(driver, query):
    logger.info("Starting product search for: %s", query)

    # Search box
    search_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (
                By.CSS_SELECTOR,
                "#twotabsearchtextbox"
            )
        )
    )

    search_box.click()

    logger.info("Entering search query")
    type_slowly(search_box, query)

    # Submit Search
    search_box.send_keys(Keys.ENTER)

    # Wait for results
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (
                By.CSS_SELECTOR,
                'div[data-component-type="s-search-result"]'
            )
        )
    )

    results = []
    seen_asins = set()

    # Progressive scrolling to load all products, scrolling 2 times to end while extracting data
    scroll_passes = 2
    for pass_num in range(scroll_passes):
        logger.info("Scrolling pass %s/%s", pass_num + 1, scroll_passes)
        
        # Scroll in small increments to trigger lazy loading
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # Scroll down by a chunk
            driver.execute_script("window.scrollBy(0, 500);")
            random_delay(0.3, 0.6)
            
            # Extract products that are now in view
            products = driver.find_elements(
                By.CSS_SELECTOR,
                'div[data-component-type="s-search-result"]'
            )
            
            for product in products:
                asin = product.get_attribute("data-asin")
                
                # Skip duplicates or products without ASIN
                if not asin or asin in seen_asins:
                    continue
                seen_asins.add(asin)
                
                # Scroll product into view to ensure content loads
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", product)
                random_delay(0.2, 0.4)
                
                title = get_text(product, "h2")
                
                # Skip if no title (not loaded yet)
                if not title:
                    continue
                
                # main price only, skip the struck-through "Typical/List price"
                price = get_text(product, ".a-price:not(.a-text-price) .a-offscreen")
                
                # "4.5 out of 5 stars"
                rating = get_text(product, '[data-cy="reviews-block"] .a-icon-alt')
                
                # "1,308 ratings" lives in the aria-label of the count link
                try:
                    reviews = product.find_element(
                        By.CSS_SELECTOR,
                        'a[aria-label$="ratings"]'
                    ).get_attribute("aria-label")
                except NoSuchElementException:
                    reviews = None
                
                # clean link built from ASIN
                link = urljoin(driver.current_url, f"/dp/{asin}") if asin else None
                
                results.append({
                    "asin": asin,
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "reviews": reviews,
                    "link": link,
                })
            
            # Check if we've reached the bottom
            new_height = driver.execute_script("return document.body.scrollHeight")
            if driver.execute_script("return window.innerHeight + window.scrollY") >= new_height - 100:
                break
            
            # If page height changed (more content loaded), continue scrolling
            if new_height != last_height:
                last_height = new_height
        
        logger.info("Completed scroll pass %s", pass_num + 1)
        random_delay(1, 2)

    logger.info("Extracted %s unique product details", len(results))

    # Save to CSV
    df = pd.DataFrame(results)
    df.to_csv("amazon_search_results.csv", index=False)
    logger.info("Results saved to amazon_search_results.csv")

    return results
