import logging
import time

import markdownify as md
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


class GeminiAPI:

    def __init__(self, debug=False, markdown=False):
        profile_path = "/home/roshan/.mozilla/firefox/4vu0d5mf.default-release"

        options = Options()

        if not debug:
            options.add_argument("--headless")

        if profile_path:  # Use profile path if provided
            options.add_argument(f"-profile {profile_path}")

        self.driver = webdriver.Firefox(service=FirefoxService(
            GeckoDriverManager().install()), options=options)
        self.driver.get("https://gemini.google.com/app")
        time.sleep(7)

        self.history = []
        self.markdown = markdown

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print("-"*50)
        print("History:")
        for result in self.history:
            print(result)
        self.driver.close()

    def inference_complete_signal(self):
        # time.sleep(20)
        # return
        while True:
            time.sleep(2)
            if self.driver.find_elements(By.XPATH, '//div[contains(@class, "multi-response-container") and @style=""]'):
                return

    def query(self, text):
        logger = logging.getLogger(__name__)
        if '\'' in text or '"' in text:
            logger.warning(
                "Single quotes & Double quotes are not supported by the Gemini API. Replacing with `.")
            text = text.replace('\'', '`').replace('"', '`')

        html_text = ""
        for line in text.split('\n'):
            html_text += "<p>" + line + "</p>"

        element = self.driver.find_element(By.XPATH, '//rich-textarea/div')
        self.driver.execute_script(
            f"arguments[0].innerHTML = '{html_text}'", element)
        self.driver.find_element(
            By.XPATH, '//div[contains(@class, "send-button-container")]').click()

        self.inference_complete_signal()

        responses = self.driver.find_elements(
            By.XPATH, '//div[contains(@class, "response-container-content")]')

        last_response = responses[-1]
        if self.markdown:
            innerHTML = responses[-1].get_attribute("innerHTML")
            last_response = md.markdownify(innerHTML)
        else:
            last_response = last_response.text

        result = {'query': text, 'response': last_response}
        self.history.append(result)

        return last_response


if __name__ == "__main__":
    with GeminiAPI() as gemini:
        while True:
            print(gemini.query(input()))
