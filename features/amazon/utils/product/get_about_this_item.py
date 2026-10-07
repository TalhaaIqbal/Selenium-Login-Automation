from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def get_about_this_item(driver: webdriver.Chrome) -> list[str]:
    try:
        container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#feature-bullets")
            )
        )

        bullet_elements = container.find_elements(
            By.CSS_SELECTOR,
            "ul li span.a-list-item"
        )

        return [
            bullet.text.strip()
            for bullet in bullet_elements
            if bullet.text.strip()
        ]

    except Exception:
        return []