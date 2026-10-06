from dotenv import load_dotenv

import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from logging_config import logger
from utils.random_delay import random_delay
from utils.type_slowly import type_slowly
from utils.init_driver import init_chrome_driver

def boulevard_login():

    logger.info("Starting Boulevard login process")

    load_dotenv()

    email = os.getenv("BOULEVARD_EMAIL")
    password = os.getenv("BOULEVARD_PASSWORD")
    url = os.getenv("BOULEVARD_URL")

    driver = init_chrome_driver()

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