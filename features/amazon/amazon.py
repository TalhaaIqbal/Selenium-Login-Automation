from dotenv import load_dotenv

import os
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from logging_config import logger
from utils.random_delay import random_delay
from utils.type_slowly import type_slowly
from utils.init_driver import init_chrome_driver
from .utils.login import amazon_login
from .utils.get_text import get_text

import pandas as pd

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
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    'div[data-component-type="s-search-result"]'
                )
            )
        )


        logger.info("Found %s products", len(products))


        results = []

        for product in products:
            asin = product.get_attribute("data-asin")

            title = get_text(product, "h2")

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
            
        print(results)
        
        df = pd.DataFrame(results)
        df.to_csv("amazon_search_results.csv", index=False)

        
    except Exception:
        logger.exception("Amazon search failed")
        raise

    finally:
        logger.info("Closing WebDriver")
        driver.quit()
