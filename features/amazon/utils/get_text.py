from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def get_text(driver, element, selector):
    try:
        child = element.find_element(
            By.CSS_SELECTOR,
            selector
        )
    except NoSuchElementException:
        return None

    text = driver.execute_script("""
        const element = arguments[0].cloneNode(true);

        element.querySelectorAll('script, style').forEach(
            el => el.remove()
        );

        return element.textContent;
    """, child)

    text = " ".join(
        (text or "")
        .replace("\xa0", " ")
        .split()
    )

    return text or None