from selenium import webdriver
from logging_config import logger


def init_chrome_driver():
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

    return driver
