from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By



def get_reviews(driver: webdriver.Chrome) -> dict:
    try:
        reviews_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#averageCustomerReviews")
            )
        )

        # Rating: 4.0
        rating = reviews_container.find_element(
            By.CSS_SELECTOR, "#acrPopover .a-icon-alt"
        ).get_attribute("innerHTML")

        # Convert "4.0 out of 5 stars" -> "4.0"
        rating = rating.split(" ")[0]

        # Reviews: (357)
        review_text = reviews_container.find_element(
            By.CSS_SELECTOR, "#acrCustomerReviewText"
        ).text.strip()

        # Convert "(357)" -> "357"
        review_count = review_text.strip("()").replace(",", "")

        # ASIN
        asin = reviews_container.get_attribute("data-asin")

        return {
            "rating": rating,
            "review_count": review_count,
            "asin": asin
        }

    except Exception:
        return {
            "rating": None,
            "review_count": None,
            "asin": None
        }