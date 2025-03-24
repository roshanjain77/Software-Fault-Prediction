from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# import options
from selenium.webdriver.chrome.options import Options

options = Options()
# options.add_experimental_option("debuggerAddress", "localhost:9222")
options.binary_location = "/usr/bin/chromium"


driver = webdriver.Chrome(options=options)
driver.get("http://www.python.org")

# driver.find_element(By.XPATH, "//*[@id='component-123-button']").click()