from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

def get_price(driver: webdriver) -> str | None:
    try:
        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span.a-price")
            )
        )

        currency = price_element.find_element(
            By.CSS_SELECTOR, ".a-price-symbol"
        ).text.strip()

        whole = price_element.find_element(
            By.CSS_SELECTOR, ".a-price-whole"
        ).text.strip()

        fraction = price_element.find_element(
            By.CSS_SELECTOR, ".a-price-fraction"
        ).text.strip()

        return f"{currency} {whole}.{fraction}"

    except Exception:
        return None