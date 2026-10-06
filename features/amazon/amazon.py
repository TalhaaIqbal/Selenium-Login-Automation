from this import s
from dotenv import load_dotenv

import random
import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from logging_config import logger
from utils.random_delay import random_delay
from utils.type_slowly import type_slowly
from utils.init_driver import init_chrome_driver


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
        
        #Check if we are on shipping continue page
        continue_buttons = driver.find_elements(
            By.CSS_SELECTOR,
            'button[alt="Continue shopping"]'
        )

        if continue_buttons:
            logger.info("Continue shopping button found")

            continue_buttons[0].click()

            random_delay(1, 2)

        else:
            logger.info(
                "Continue shopping button not found, continuing"
            )
            
            
              
        #arriving at the main page
        signin_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    'a[data-nav-role="signin"]'
                )
            )
        )

        signin_link.click()


        # Email/Phone
        logger.info("Waiting for email/phone field to appear")
        
        
        #Arriving at the email/phone entry page
        email_phone_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    'input[name="email"]'
                )
            )
        )

        random_delay(0.5, 1.5)

        logger.info("Entering email/phone")

        type_slowly(email_phone_field, phone)

        # Login button
        logger.info("Waiting for continue button")

        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    'input[aria-labelledby="continue-announce"]'
                )
            )
        )

        logger.info("Clicking Continue button")

        continue_button.click()

        # Wait for page to load after clicking continue
        random_delay(2, 3)

        #Arriving at the password page
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    'input[name="password"]'
                )
            )
        )
        
        logger.info("Clicking Sign In button")
        
        password_field.click()
        
        random_delay(0.5, 1.5)
        logger.info("Entering password")
        type_slowly(password_field, password)


        signin_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    'input[id="signInSubmit"]'
                )
            )
        )

        logger.info("Clicking Continue button")

        signin_button.click()


        # Wait for navigation
        logger.info("Waiting for login to complete")

        input("Press Enter to continue...")

    except Exception:
        logger.exception("Amazon login failed")
        raise


    finally:
        logger.info("Closing WebDriver")

        driver.quit()
    
    