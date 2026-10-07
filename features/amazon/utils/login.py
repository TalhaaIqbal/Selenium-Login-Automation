import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from logging_config import logger
from utils.random_delay import random_delay
from utils.type_slowly import type_slowly
from .challenge_page import wait_while_challenge
from .challenge_page import wait_for_login


def amazon_login(driver, phone, password):
    logger.info("Starting Amazon login process")

    continue_buttons = driver.find_elements(
        By.CSS_SELECTOR, 'button[alt="Continue shopping"]'
    )
    if continue_buttons:
        logger.info("Continue shopping button found")
        continue_buttons[0].click()
        random_delay(1, 2)
    else:
        logger.info("Continue shopping button not found, continuing")

    signin_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-nav-role="signin"]'))
    )
    signin_link.click()

    logger.info("Waiting for email/phone field to appear")
    email_phone_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="email"]'))
    )

    random_delay(0.5, 1.5)
    logger.info("Entering email/phone")
    type_slowly(email_phone_field, phone)

    logger.info("Waiting for continue button")
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'input[aria-labelledby="continue-announce"]')
        )
    )

    logger.info("Clicking Continue button")
    continue_button.click()
    random_delay(2, 3)

    # CHANGE 1: pause here if a captcha shows up after the email step
    wait_while_challenge(driver)

    password_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]'))
    )

    logger.info("Clicking password field")
    password_field.click()

    random_delay(0.5, 1.5)
    logger.info("Entering password")
    type_slowly(password_field, password)

    signin_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[id="signInSubmit"]'))
    )

    logger.info("Clicking Sign In button")
    signin_button.click()

    # CHANGE 2: wait for login, pausing for captcha/OTP/puzzle
    wait_for_login(driver)