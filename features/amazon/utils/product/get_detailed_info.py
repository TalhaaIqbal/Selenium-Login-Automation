from selenium import webdriver
from selenium.webdriver.common.by import By

from logging_config import logger
from ..get_text import get_text


def get_product_information(driver: webdriver.Chrome) -> dict:
    product_information = {}

    containers = driver.find_elements(
        By.CSS_SELECTOR,
        "#productDetails_expanderTables_depthLeftSections, "
        "#productDetails_expanderTables_depthRightSections"
    )

    logger.info("Containers found: %s", len(containers))

    if not containers:
        logger.warning("No product information containers found")
        return product_information

    for i, container in enumerate(containers):
        sections = container.find_elements(By.CSS_SELECTOR, "div.a-expander-container")
        logger.info("Container %s: %s sections", i + 1, len(sections))

        if not sections:
            continue

        for j, section in enumerate(sections):
            heading_elements = section.find_elements(By.CSS_SELECTOR, ".a-expander-prompt")

            if not heading_elements:
                continue

            section_name = heading_elements[0].text.strip()
            tables = section.find_elements(By.CSS_SELECTOR, "table.prodDetTable")

            if not tables:
                continue

            rows = section.find_elements(By.CSS_SELECTOR, "table.prodDetTable tr")
            section_data = {}

            for row in rows:
                key_elements = row.find_elements(By.CSS_SELECTOR, "th.prodDetSectionEntry")
                value_elements = row.find_elements(By.TAG_NAME, "td")

                if not key_elements or not value_elements:
                    continue

                key = get_text(driver, row, "th.prodDetSectionEntry")
                value = get_text(driver, row, "td")

                if key and value:
                    section_data[key] = value

            if section_data:
                product_information[section_name] = section_data

    logger.info("Total sections extracted: %s", len(product_information))
    return product_information