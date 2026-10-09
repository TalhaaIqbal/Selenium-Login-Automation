import os
from dotenv import load_dotenv
from selenium import webdriver

load_dotenv()

options = webdriver.ChromeOptions()
options.add_argument(f"--proxy-server=http://{os.environ['PROXY_HOST']}:{os.environ['PROXY_PORT']}")
driver = webdriver.Chrome(options=options)
driver.get("https://myip.com")
print(driver.page_source)

input("enter")
driver.quit()   