from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def get_text(element, selector):
    try:
        child = element.find_element(By.CSS_SELECTOR, selector)
    except NoSuchElementException:
        return None
    
    # .text is empty for visually-hidden elements (a-offscreen), textContent isn't
    text = (child.get_attribute("textContent") or "").replace("\xa0", " ").strip()
    return text or None