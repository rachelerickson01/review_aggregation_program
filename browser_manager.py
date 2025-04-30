from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium import webdriver
import os

class BrowserSessionManager:
    def __init__(
        self,
        use_brightdata=True,
        brightdata_username=None,
        brightdata_password=None,
        executable_path="/Users/rachelerickson/repos/review_aggregation_program/chromedriver",  # for local fallback
    ):
        """
        :param use_brightdata: Set to True for BrightData API, False for local Chrome
        :param brightdata_username:  BrightData username (only used if use_brightdata=True)
        :param brightdata_password:  BrightData password
        :param executable_path: Path to your local chromedriver for local mode
        """
        self.use_brightdata = use_brightdata
        self.brightdata_username = brightdata_username
        self.brightdata_password = brightdata_password
        self.executable_path = executable_path
        self.driver = None

    # warns if no credentials provided
    def _build_brightdata_url(self):
        if not self.brightdata_username or not self.brightdata_password:
            raise ValueError("BrightData credentials must be provided.")
        return f"https://{self.brightdata_username}:{self.brightdata_password}@brd.superproxy.io:9515"

    def start_session(self):
        options = Options()
        options.add_argument("--start-maximized")

        if self.use_brightdata:
            print("[INFO] Connecting to BrightData Scraping Browser via Remote API...")
            url = self._build_brightdata_url()
            connection = ChromiumRemoteConnection(url, "goog", "chrome")
            options = Options()
            self.driver = Remote(connection, options=options)
        else:
            print("[INFO] Launching local Chrome session...")
            if not os.path.exists(self.executable_path):
                raise FileNotFoundError(f"Could not find ChromeDriver at: {self.executable_path}")
            service = Service(executable_path=self.executable_path)
            self.driver = webdriver.Chrome(service=service, options=options)
        
        return self.driver

    def close_session(self):
        if self.driver:
            self.driver.quit()
            print("[INFO] Browser session closed.")
