from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from time import sleep
import undetected_chromedriver as uc

class ViewBot:
    def __init__(self, url):
        self.driver = None
        self.url = url

    def setup_driver(self):
        # TODO: explore chrome options
        chrome_options = Options()
        # chrome_options.add_experimental_option("detach", True)
        self.driver = uc.Chrome(headless=False,use_subprocess=False, options=chrome_options)

    def view_stream(self):
        self.setup_driver()
        self.driver.get(self.url)
        sleep(10)
        # get "Start Watching" button in case where stream is age restricted
        button = self.driver.find_element(By.CSS_SELECTOR, "button.variant-action.size-sm")
        button.click()
        sleep(300)
        

    
if __name__ == "__main__":
    bot = ViewBot("https://kick.com/xqcow")
    bot.view_stream()