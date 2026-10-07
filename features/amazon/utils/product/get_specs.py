from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By



def get_product_specs(driver: webdriver.Chrome) -> dict:
    specs = {}

    try:
        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "table.a-normal tr[role='listitem']")
            )
        )

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")

            if len(cells) >= 2:
                key = cells[0].text.strip()
                value = cells[1].text.strip()

                if key and value:
                    specs[key] = value

    except Exception:
        pass

    return specs