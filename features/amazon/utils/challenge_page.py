import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By

from logging_config import logger
from utils.random_delay import random_delay

CHALLENGE_URL_PARTS = ("/ap/cvf", "/ap/mfa", "/ap/challenge", "validateCaptcha")

CHALLENGE_SELECTORS = ", ".join([
    "#captchacharacters",
    "#auth-captcha-guess",
    "#auth-mfa-otpcode",
    "input[name='otpCode']",
    "#cvf-input-code",
    "#cvf-aamation-challenge-iframe",
    "#aacb-captcha-header",
])


def is_challenge(driver):
    if any(part in driver.current_url for part in CHALLENGE_URL_PARTS):
        return True
    return bool(driver.find_elements(By.CSS_SELECTOR, CHALLENGE_SELECTORS))


def is_logged_in(driver):
    try:
        el = driver.find_element(By.ID, "nav-link-accountList-nav-line-1")
        return "sign in" not in el.get_attribute("textContent").lower()
    except NoSuchElementException:
        return False


def wait_while_challenge(driver, timeout=300):
    if not is_challenge(driver):
        return

    logger.warning("Challenge detected. Solve it in the browser...")
    deadline = time.time() + timeout
    while time.time() < deadline:
        if not is_challenge(driver):
            logger.info("Challenge cleared, continuing")
            random_delay(1, 2)
            return
        time.sleep(1)

    raise TimeoutException("Challenge was not solved in time")


def wait_for_login(driver, timeout=300):
    deadline = time.time() + timeout
    warned = False

    while time.time() < deadline:
        if is_logged_in(driver):
            logger.info("Login successful")
            return

        if driver.find_elements(By.CSS_SELECTOR, "#auth-error-message-box"):
            raise RuntimeError("Amazon rejected the credentials")

        if is_challenge(driver) and not warned:
            logger.warning("Extra verification required. Solve it in the browser...")
            warned = True

        time.sleep(1)

    raise TimeoutException("Login did not complete in time")

