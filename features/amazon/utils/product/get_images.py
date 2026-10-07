from selenium import webdriver
from selenium.webdriver.common.by import By


def get_product_images(driver: webdriver.Chrome) -> list[dict]:
    try:
        image_elements = driver.find_elements(
            By.CSS_SELECTOR,
            "#main-image-container img[data-old-hires]"
        )

        product_images = []

        for index, image in enumerate(image_elements):
            high_res_url = image.get_attribute("data-old-hires")
            image_url = image.get_attribute("src")
            alt_text = image.get_attribute("alt")

            # Some Amazon images have no alt attribute
            if not alt_text:
                try:
                    parent = image.find_element(
                        By.XPATH,
                        "./ancestor::*[@data-mb-pv-slot-index][1]"
                    )

                    alt_text = parent.find_element(
                        By.CSS_SELECTOR,
                        ".a-offscreen"
                    ).text.strip()

                except Exception:
                    alt_text = None

            product_images.append({
                "index": index,
                "image_url": high_res_url or image_url,
                "thumbnail_url": image_url,
                "alt": alt_text
            })

        return product_images

    except Exception:
        return []