import random
import time


def human_delay(a: float = 0.8, b: float = 2.5) -> None:
    time.sleep(random.uniform(a, b))


def human_type(element, text: str) -> None:
    for ch in text:
        element.send_keys(ch)
        time.sleep(random.uniform(0.05, 0.2))
