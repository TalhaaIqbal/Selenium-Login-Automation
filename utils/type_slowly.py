import random
import time
from selenium.webdriver.remote.webelement import WebElement


def type_slowly(element: WebElement, text: str, min_delay: float = 0.05, max_delay: float = 0.15) -> None:
    for character in text:
        element.send_keys(character)

        time.sleep(
            random.uniform(
                min_delay,
                max_delay
            )
        )

