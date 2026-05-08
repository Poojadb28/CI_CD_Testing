import os
import time

from selenium.webdriver.common.by import By
from utils.logger import get_logger
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

logger = get_logger(__name__)


class DrawingCheckerGeneralPage(BasePage):

    def __init__(self, driver):

        super().__init__(driver)

    # ==========================================================
    # LOCATORS
    # ==========================================================

    dropdown = (
        By.XPATH,
        "//select[contains(@class,'text-sm')]"
    )

    option = (
        By.XPATH,
        "//option[normalize-space()='Drawing Checker - General']"
    )

    run_btn = (
        By.XPATH,
        "//button[contains(text(),'Run Drawing Checker - General')]"
    )

    view_results = (
        By.XPATH,
        "//button[normalize-space()='View Results']"
    )

    search_field = (
        By.XPATH,
        "//input[@id='issue-search']"
    )

    severity_dropdown = (
        By.XPATH,
        "//select[@id='severity-filter']"
    )

    source_dropdown = (
        By.XPATH,
        "//select[@id='source-filter']"
    )

    drilldown_btn = (
        By.XPATH,
        "//button[contains(@class,'drill') or contains(.,'Drill')]"
    )

    download_btn = (
        By.XPATH,
        "//a[normalize-space()='Download PDF Report']"
    )

    # ==========================================================
    # ACTIONS
    # ==========================================================

    def select_drawing_checker_general(self):

        logger.info(
            "Selecting Drawing Checker - General"
        )

        self.safe_click(self.dropdown)

        self.safe_click(self.option)

        self.wait_for_page_ready()

    def click_run(self):

        logger.info(
            "Running Drawing Checker"
        )

        self.safe_click(self.run_btn)

        self.wait_for_loader()

    def wait_for_processing(self):

        self.wait_for_clickable(
            self.view_results
        )

    def click_view_results(self):

        logger.info(
            "Opening results page"
        )

        self.safe_click(
            self.view_results
        )

        self.wait_for_page_ready()

    # ==========================================================
    # SEARCH
    # ==========================================================

    def search_issue(self, text):

        self.enter_text(
            self.search_field,
            text
        )

    def clear_search(self):

        field = self.wait_for_visibility(
            self.search_field
        )

        field.clear()

    # ==========================================================
    # FILTERS
    # ==========================================================

    def filter_by_severity(self, value):

        dropdown = self.wait_for_clickable(
            self.severity_dropdown
        )

        dropdown.click()

        option = (
            By.XPATH,
            (
                f"//select[@id='severity-filter']"
                f"/option[normalize-space()='{value}']"
            )
        )

        self.safe_click(option)

        self.wait_for_loader()

    def filter_by_source(self, value):

        dropdown = self.wait_for_clickable(
            self.source_dropdown
        )

        dropdown.click()

        option = (
            By.XPATH,
            (
                f"//select[@id='source-filter']"
                f"/option[normalize-space()='{value}']"
            )
        )

        self.safe_click(option)

        self.wait_for_loader()

    # ==========================================================
    # DRILLDOWN
    # ==========================================================

    def click_drilldown(self):

        logger.info(
            "Opening drilldown"
        )

        buttons = self.wait.until(
            EC.presence_of_all_elements_located(
                self.drilldown_btn
            )
        )

        logger.info(
            f"Drilldown buttons found: {len(buttons)}"
        )

        for button in buttons:

            if button.is_displayed():

                self.driver.execute_script(
                    (
                        "arguments[0].scrollIntoView("
                        "{block:'center'});"
                    ),
                    button
                )

                try:

                    button.click()

                except Exception:

                    self.driver.execute_script(
                        "arguments[0].click();",
                        button
                    )

                self.wait_for_page_ready()

                self.wait_for_loader()

                return

        raise Exception(
            "Drilldown button not found"
        )

    # ==========================================================
    # DOWNLOAD REPORT
    # ==========================================================

    def download_report(self, download_dir):

        logger.info(
            "Downloading PDF report"
        )

        if not os.path.exists(download_dir):

            raise FileNotFoundError(
                (
                    "Download directory not found: "
                    f"{download_dir}"
                )
            )

        before_files = set(
            os.listdir(download_dir)
        )

        button = self.wait_for_clickable(
            self.download_btn
        )

        self.driver.execute_script(
            (
                "arguments[0].scrollIntoView("
                "{block:'center'});"
            ),
            button
        )

        try:

            button.click()

        except Exception:

            self.driver.execute_script(
                "arguments[0].click();",
                button
            )

        timeout = 120

        end_time = time.time() + timeout

        while time.time() < end_time:

            after_files = set(
                os.listdir(download_dir)
            )

            new_files = (
                after_files - before_files
            )

            completed_files = [

                file for file in new_files

                if (
                    file.endswith(".pdf")
                    and not file.endswith(
                        ".crdownload"
                    )
                )
            ]

            if completed_files:

                downloaded_file = (
                    completed_files[0]
                )

                logger.info(
                    (
                        "Downloaded file: "
                        f"{downloaded_file}"
                    )
                )

                return os.path.join(
                    download_dir,
                    downloaded_file
                )

            time.sleep(1)

        raise Exception(
            "PDF report download not detected"
        )