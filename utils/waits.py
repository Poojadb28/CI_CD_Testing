import time
import logging

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    NoSuchElementException
)

logger = logging.getLogger(__name__)


class WaitUtils:

    def __init__(
        self,
        driver,
        timeout=30,
        short_timeout=10
    ):

        self.driver = driver

        self.timeout = timeout

        self.short_timeout = short_timeout

        self.wait = WebDriverWait(
            driver,
            timeout
        )

        self.short_wait = WebDriverWait(
            driver,
            short_timeout
        )

    # ==========================================================
    # PAGE LOAD WAIT
    # ==========================================================

    def wait_for_page_load(self):

        logger.info(
            "Waiting for page load"
        )

        self.wait.until(
            lambda d: d.execute_script(
                "return document.readyState"
            ) == "complete"
        )

    # ==========================================================
    # WAIT FOR CLICKABLE
    # ==========================================================

    def wait_for_clickable(
        self,
        locator
    ):

        logger.info(
            f"Waiting for clickable: {locator}"
        )

        return self.wait.until(
            EC.element_to_be_clickable(
                locator
            )
        )

    # ==========================================================
    # WAIT FOR VISIBILITY
    # ==========================================================

    def wait_for_visibility(
        self,
        locator
    ):

        logger.info(
            f"Waiting for visibility: {locator}"
        )

        return self.wait.until(
            EC.visibility_of_element_located(
                locator
            )
        )

    # ==========================================================
    # WAIT FOR PRESENCE
    # ==========================================================

    def wait_for_presence(
        self,
        locator
    ):

        logger.info(
            f"Waiting for presence: {locator}"
        )

        return self.wait.until(
            EC.presence_of_element_located(
                locator
            )
        )

    # ==========================================================
    # WAIT FOR INVISIBILITY
    # ==========================================================

    def wait_for_invisibility(
        self,
        locator
    ):

        logger.info(
            f"Waiting for invisibility: {locator}"
        )

        return self.wait.until(
            EC.invisibility_of_element_located(
                locator
            )
        )

    # ==========================================================
    # WAIT FOR TEXT
    # ==========================================================

    def wait_for_text(
        self,
        locator,
        text
    ):

        logger.info(
            f"Waiting for text '{text}'"
        )

        return self.wait.until(
            EC.text_to_be_present_in_element(
                locator,
                text
            )
        )

    # ==========================================================
    # WAIT FOR URL
    # ==========================================================

    def wait_for_url_contains(
        self,
        text
    ):

        logger.info(
            f"Waiting for URL contains: {text}"
        )

        return self.wait.until(
            EC.url_contains(text)
        )

    # ==========================================================
    # WAIT FOR TITLE
    # ==========================================================

    def wait_for_title_contains(
        self,
        text
    ):

        logger.info(
            f"Waiting for title contains: {text}"
        )

        return self.wait.until(
            EC.title_contains(text)
        )

    # ==========================================================
    # WAIT FOR LOADER
    # ==========================================================

    def wait_for_loader(self):

        logger.info(
            "Waiting for loader to disappear"
        )

        try:

            self.wait.until(
                EC.invisibility_of_element_located(
                    (
                        By.XPATH,
                        (
                            "//div[contains(@class,"
                            "'animate-spin') "
                            "or contains(text(),"
                            "'Processing') "
                            "or contains(@class,"
                            "'loading')]"
                        )
                    )
                )
            )

        except TimeoutException:

            logger.warning(
                "Loader still visible after timeout"
            )

    # ==========================================================
    # WAIT FOR STALENESS
    # ==========================================================

    def wait_for_staleness(
        self,
        element
    ):

        logger.info(
            "Waiting for element staleness"
        )

        self.wait.until(
            EC.staleness_of(element)
        )

    # ==========================================================
    # SAFE CLICK
    # ==========================================================

    def safe_click(
        self,
        locator,
        retries=3
    ):

        logger.info(
            f"Safe clicking: {locator}"
        )

        for attempt in range(retries):

            try:

                element = self.wait.until(
                    EC.element_to_be_clickable(
                        locator
                    )
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

                time.sleep(1)

    # ==========================================================
    # RETRY FIND ELEMENT
    # ==========================================================

    def retry_find_element(
        self,
        locator,
        retries=3
    ):

        logger.info(
            f"Retry finding element: {locator}"
        )

        for attempt in range(retries):

            try:

                return self.driver.find_element(
                    *locator
                )

            except (
                StaleElementReferenceException,
                NoSuchElementException
            ) as e:

                logger.warning(
                    (
                        f"Retry find "
                        f"{attempt + 1}/{retries}: {e}"
                    )
                )

                if attempt == retries - 1:

                    raise

                time.sleep(1)

    # ==========================================================
    # RETRY ACTION WRAPPER
    # ==========================================================

    def retry_action(
        self,
        action,
        retries=3,
        delay=1
    ):

        logger.info(
            "Executing retry wrapper"
        )

        last_exception = None

        for attempt in range(retries):

            try:

                return action()

            except Exception as e:

                last_exception = e

                logger.warning(
                    (
                        f"Retry action "
                        f"{attempt + 1}/{retries}: {e}"
                    )
                )

                time.sleep(delay)

        raise last_exception

    # ==========================================================
    # WAIT FOR ELEMENT COUNT
    # ==========================================================

    def wait_for_elements_count(
        self,
        locator,
        minimum=1
    ):

        logger.info(
            (
                f"Waiting for minimum "
                f"{minimum} elements"
            )
        )

        self.wait.until(
            lambda d: len(
                d.find_elements(*locator)
            ) >= minimum
        )

    # ==========================================================
    # WAIT FOR WINDOW COUNT
    # ==========================================================

    def wait_for_window_count(
        self,
        count
    ):

        logger.info(
            f"Waiting for {count} windows"
        )

        self.wait.until(
            lambda d: len(
                d.window_handles
            ) == count
        )

    # ==========================================================
    # CUSTOM WAIT
    # ==========================================================

    def custom_wait(
        self,
        condition,
        timeout=None
    ):

        logger.info(
            "Executing custom wait"
        )

        WebDriverWait(
            self.driver,
            timeout or self.timeout
        ).until(condition)