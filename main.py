from dotenv import load_dotenv

import random
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from logging_config import logger


def random_delay(min_seconds=1, max_seconds=2):
    time.sleep(
        random.uniform(
            min_seconds,
            max_seconds
        )
    )


def type_slowly(element, text, min_delay=0.05, max_delay=0.15):
    for character in text:
        element.send_keys(character)

        time.sleep(
            random.uniform(
                min_delay,
                max_delay
            )
        )


def boulevard_login():

    logger.info("Starting Boulevard login process")

    load_dotenv()

    email = os.getenv("BOULEVARD_EMAIL")
    password = os.getenv("BOULEVARD_PASSWORD")
    url = os.getenv("BOULEVARD_URL")

    # Chrome settings
    logger.info("Initializing Chrome WebDriver")

    options = webdriver.ChromeOptions()

    # browser window size
    options.add_argument("--start-maximized")

    # language
    options.add_argument("--lang=en-US")
    
    # Excludes the automation switch that triggers the banner
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # Disables the automation extension
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(
        options=options
    )

    try:
        # Open website
        logger.info("Navigating to URL: %s", url)

        driver.get(url)

        random_delay(1, 2)


        # Email
        logger.info("Waiting for email field to appear")

        email_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    'input[name="email"]'
                )
            )
        )

        random_delay(0.5, 1.5)

        logger.info("Entering email")

        type_slowly(email_field, email)

        # Password
        logger.info("Waiting for password field")

        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    'input[name="password"]'
                )
            )
        )

        random_delay(0.5, 1.5)

        logger.info("Entering password")

        type_slowly(password_field, password)


        # Login button
        logger.info("Waiting for login button")

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    'button[type="submit"]'
                )
            )
        )

        random_delay(0.5, 1.5)

        logger.info("Clicking login button")

        login_button.click()


        # Wait for navigation
        logger.info("Waiting for login to complete")

        input("Press Enter to continue...")

    except Exception:
        logger.exception("Boulevard login failed")
        raise


    finally:
        logger.info("Closing WebDriver")

        driver.quit()


if __name__ == "__main__":
    boulevard_login()