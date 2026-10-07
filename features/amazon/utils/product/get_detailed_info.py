from selenium import webdriver
from selenium.webdriver.common.by import By

from logging_config import logger
from ..get_text import get_text


def get_product_information(driver: webdriver.Chrome) -> dict:
    product_information = {}

    logger.info("========== PRODUCT INFORMATION EXTRACTION START ==========")

    # ---------------------------------------------------------
    # 1. Find containers
    # ---------------------------------------------------------
    containers = driver.find_elements(
        By.CSS_SELECTOR,
        "#productDetails_expanderTables_depthLeftSections, "
        "#productDetails_expanderTables_depthRightSections"
    )

    logger.info(
        "Product information containers found: %s",
        len(containers)
    )

    if not containers:
        logger.warning(
            "NO PRODUCT INFORMATION CONTAINERS FOUND"
        )
        return product_information

    # ---------------------------------------------------------
    # 2. Process containers
    # ---------------------------------------------------------
    for i, container in enumerate(containers):

        logger.info(
            "========== CONTAINER %s ==========",
            i + 1
        )

        logger.info(
            "Container ID: %s",
            container.get_attribute("id")
        )

        logger.info(
            "Container class: %s",
            container.get_attribute("class")
        )

        # -----------------------------------------------------
        # 3. Find sections
        # -----------------------------------------------------
        sections = container.find_elements(
            By.CSS_SELECTOR,
            "div.a-expander-container"
        )

        logger.info(
            "Sections found: %s",
            len(sections)
        )

        if not sections:
            logger.warning(
                "NO SECTIONS FOUND IN CONTAINER %s",
                i + 1
            )

            # Useful diagnostic
            logger.info(
                "Container HTML preview: %s",
                container.get_attribute("outerHTML")[:2000]
            )

            continue

        # -----------------------------------------------------
        # 4. Process sections
        # -----------------------------------------------------
        for j, section in enumerate(sections):

            logger.info(
                "---------- SECTION %s.%s ----------",
                i + 1,
                j + 1
            )

            logger.info(
                "Section class: %s",
                section.get_attribute("class")
            )

            # ---------------------------------------------
            # Find heading
            # ---------------------------------------------
            heading_elements = section.find_elements(
                By.CSS_SELECTOR,
                ".a-expander-prompt"
            )

            logger.info(
                "Heading elements found: %s",
                len(heading_elements)
            )

            if not heading_elements:
                logger.warning(
                    "NO HEADING FOUND FOR SECTION %s.%s",
                    i + 1,
                    j + 1
                )
                continue

            section_name = heading_elements[0].text.strip()

            logger.info(
                "Section name: %s",
                section_name
            )

            # ---------------------------------------------
            # Find table
            # ---------------------------------------------
            tables = section.find_elements(
                By.CSS_SELECTOR,
                "table.prodDetTable"
            )

            logger.info(
                "Product detail tables found: %s",
                len(tables)
            )

            if not tables:
                logger.warning(
                    "NO prodDetTable FOUND IN SECTION: %s",
                    section_name
                )
                continue

            # ---------------------------------------------
            # Find rows
            # ---------------------------------------------
            rows = section.find_elements(
                By.CSS_SELECTOR,
                "table.prodDetTable tr"
            )

            logger.info(
                "Rows found in '%s': %s",
                section_name,
                len(rows)
            )

            section_data = {}

            # ---------------------------------------------
            # Process rows
            # ---------------------------------------------
            for k, row in enumerate(rows):

                key_elements = row.find_elements(
                    By.CSS_SELECTOR,
                    "th.prodDetSectionEntry"
                )

                value_elements = row.find_elements(
                    By.TAG_NAME,
                    "td"
                )

                logger.info(
                    "Row %s | key elements: %s | value elements: %s",
                    k + 1,
                    len(key_elements),
                    len(value_elements)
                )

                if not key_elements:
                    logger.warning(
                        "Row %s has NO KEY",
                        k + 1
                    )
                    continue

                if not value_elements:
                    logger.warning(
                        "Row %s has NO VALUE",
                        k + 1
                    )
                    continue

                key = get_text(
                    row,
                    "th.prodDetSectionEntry"
                )

                value = get_text(
                    row,
                    "td"
                )

                logger.info(
                    "Extracted: %s = %s",
                    key,
                    value
                )

                if key and value:
                    section_data[key] = value

            # ---------------------------------------------
            # Store section
            # ---------------------------------------------
            logger.info(
                "Section '%s' extracted fields: %s",
                section_name,
                len(section_data)
            )

            if section_data:
                product_information[section_name] = section_data

    logger.info(
        "========== PRODUCT INFORMATION COMPLETE =========="
    )

    logger.info(
        "Total sections extracted: %s",
        len(product_information)
    )

    logger.info(
        "Product information keys: %s",
        list(product_information.keys())
    )

    return product_information