import os
from datetime import datetime

from selenium.webdriver.common.by import By
from utils.logger import get_logger
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    NoSuchElementException
)

logger = get_logger(__name__)


class BasePage:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(driver, 30)

        self.short_wait = WebDriverWait(driver, 10)

    # ==========================================================
    # PAGE READY
    # ==========================================================

    def wait_for_page_ready(self):

        self.wait.until(
            lambda d: d.execute_script(
                "return document.readyState"
            ) == "complete"
        )

    # ==========================================================
    # WAIT FOR CLICKABLE
    # ==========================================================

    def wait_for_clickable(self, locator):

        logger.info(
            f"Waiting for clickable: {locator}"
        )

        return self.wait.until(
            EC.element_to_be_clickable(locator)
        )

    # ==========================================================
    # WAIT FOR VISIBILITY
    # ==========================================================

    def wait_for_visibility(self, locator):

        logger.info(
            f"Waiting for visibility: {locator}"
        )

        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    # ==========================================================
    # WAIT FOR PRESENCE
    # ==========================================================

    def wait_for_presence(self, locator):

        logger.info(
            f"Waiting for presence: {locator}"
        )

        return self.wait.until(
            EC.presence_of_element_located(locator)
        )

    # ==========================================================
    # WAIT FOR LOADER
    # ==========================================================

    def wait_for_loader(self):

        try:

            self.wait.until(
                EC.invisibility_of_element_located(
                    (
                        By.XPATH,
                        (
                            "//div[contains(@class,'animate-spin') "
                            "or contains(text(),'Processing') "
                            "or contains(@class,'loading')]"
                        )
                    )
                )
            )

            logger.info("Loader disappeared")

        except TimeoutException:

            logger.warning(
                "Loader still visible after timeout"
            )

    # ==========================================================
    # SAFE JS CLICK
    # ==========================================================

    def safe_click(self, locator):

        logger.info(
            f"Clicking element: {locator}"
        )

        retries = 3

        for attempt in range(retries):

            try:

                element = self.wait.until(
                    EC.element_to_be_clickable(locator)
                )

                self.driver.execute_script(
                    (
                        "arguments[0].scrollIntoView("
                        "{block:'center'});"
                    ),
                    element
                )

                try:

                    element.click()

                except Exception:

                    self.driver.execute_script(
                        "arguments[0].click();",
                        element
                    )

                return

            except (
                StaleElementReferenceException,
                ElementClickInterceptedException
            ) as e:

                logger.warning(
                    (
                        f"Retry click "
                        f"{attempt + 1}/{retries}: {e}"
                    )
                )

                if attempt == retries - 1:
                    raise

    # ==========================================================
    # ENTER TEXT
    # ==========================================================

    def enter_text(self, locator, text):

        logger.info(
            f"Entering text into: {locator}"
        )

        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

        element.clear()

        element.send_keys(text)

    # ==========================================================
    # GET TEXT
    # ==========================================================

    def get_text(self, locator):

        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )

        return element.text.strip()

    # ==========================================================
    # IS ELEMENT DISPLAYED
    # ==========================================================

    def is_displayed(self, locator):

        try:

            return self.wait.until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()

        except TimeoutException:

            return False

    # ==========================================================
    # TAKE SCREENSHOT
    # ==========================================================

    def take_screenshot(self, name="screenshot"):

        screenshot_dir = os.path.abspath(
            "screenshots"
        )

        os.makedirs(
            screenshot_dir,
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        file_path = os.path.join(
            screenshot_dir,
            f"{name}_{timestamp}.png"
        )

        self.driver.save_screenshot(file_path)

        logger.info(
            f"Screenshot saved: {file_path}"
        )

        return file_path

    # ==========================================================
    # WAIT FOR URL CONTAINS
    # ==========================================================

    def wait_for_url_contains(
        self,
        text
    ):

        logger.info(
            f"Waiting for URL contains: {text}"
        )

        self.wait.until(
            EC.url_contains(text)
        )

    # ==========================================================
    # WAIT FOR TITLE CONTAINS
    # ==========================================================

    def wait_for_title_contains(
        self,
        text
    ):

        logger.info(
            f"Waiting for title contains: {text}"
        )

        self.wait.until(
            EC.title_contains(text)
        )

    # ==========================================================
    # SCROLL TO ELEMENT
    # ==========================================================

    def scroll_to_element(self, locator):

        element = self.wait.until(
            EC.presence_of_element_located(locator)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

    # ==========================================================
    # WAIT AND SWITCH TO ALERT
    # ==========================================================

    def wait_for_alert(self):

        logger.info("Waiting for alert")

        return self.wait.until(
            EC.alert_is_present()
        )

    # ==========================================================
    # REFRESH PAGE
    # ==========================================================

    def refresh_page(self):

        logger.info("Refreshing page")

        self.driver.refresh()

        self.wait_for_page_ready()

    # ==========================================================
    # VERIFY ELEMENT EXISTS
    # ==========================================================

    def element_exists(self, locator):

        try:

            self.driver.find_element(*locator)

            return True

        except NoSuchElementException:

            return False