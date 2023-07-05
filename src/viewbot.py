from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from multiprocessing import Process
from time import sleep
import undetected_chromedriver as uc

# TODO: add retries for cases where stream is not found

class ViewBot:
    def __init__(self, url):
        self.driver = None
        self.url = url

    def setup_driver(self):
        # TODO: explore chrome options to optimize effieciency

        options = Options()
        # options.add_argument('--disable-extensions')   
        # options.add_argument('--disable-gpu')   
        # options.add_argument("--no-sandbox")   
        # options.add_argument("--window-size=1920,1080")   
        # options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--start-maximized")
        options.add_argument("--mute-audio")
        self.driver = uc.Chrome(headless=False, options=options)

    def view_stream(self, duration):
        self.setup_driver()
        self.driver.get(self.url)
        sleep(5)
        # get "Start Watching" button in case where stream is age restricted
        try:
            button = self.driver.find_element(By.CSS_SELECTOR, "button.variant-action.size-sm")
            button.click()
            print("pressed age restriction button", flush=True)
        except NoSuchElementException:
            if "Oops, Something went wrong" in self.driver.page_source:
                self.driver.quit()
                raise RuntimeError("Something went wrong, url is likely invalid")

            print("Stream not age restricted, continue")
        sleep(duration)
        self.driver.quit()


def start_script(url, threads, duration=300):
    processes = []
    for _ in range(threads):
        bot = ViewBot(url)
        process = Process(target=bot.view_stream, args=(duration,))
        process.start()
        print("process started")
        processes.append(process)
        sleep(8)
    for process in processes:
        process.join()
        print("process done")


    
if __name__ == "__main__":
    start_script("https://kick.com/xqc", 2, 300)