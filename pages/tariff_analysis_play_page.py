import os

from utils.download_utils import wait_for_new_file
from utils.logger import get_logger
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

logger = get_logger(__name__)


class TariffPage(BasePage):

    def __init__(self, driver):

        super().__init__(driver)

    # ==========================================================
    # LOCATORS
    # ==========================================================

    dropdown = (
        By.XPATH,
        "//select[contains(@class,'text-sm')]"
    )

    tariff_option = (
        By.XPATH,
        "//option[normalize-space()='Tariff Analysis']"
    )

    treat_checkbox = (
        By.XPATH,
        "//input[contains(@class,'w-4 h-4')]"
    )

    set_top = (
        By.XPATH,
        "//button[normalize-space()='Set as Top Level']"
    )

    run_btn = (
        By.XPATH,
        "//button[contains(normalize-space(),'Run Tariff Analysis')]"
    )

    bom_export_btn = (
        By.XPATH,
        "(//button[normalize-space()='Export to Excel'])[1]"
    )

    tariff_export_btn = (
        By.XPATH,
        "//button[contains(.,'Export to Excel')][last()]"
    )

    approve_bom_btn = (
        By.XPATH,
        "//span[normalize-space()='Approve BOM']"
    )

    tariff_heading = (
        By.XPATH,
        "//h2[contains(text(),'Tariff Analysis')]"
    )

    back_project = (
        By.XPATH,
        "//span[normalize-space()='Back to Project']"
    )

    back_btn = (
        By.XPATH,
        "//span[normalize-space()='Back']"
    )

    # ==========================================================
    # ACTIONS
    # ==========================================================

    def select_tariff_analysis(self):

        logger.info(
            "Selecting Tariff Analysis"
        )

        self.safe_click(self.dropdown)

        self.safe_click(self.tariff_option)

        self.wait_for_page_ready()

    def treat_as_assembly(self):

        checkbox = self.wait_for_presence(
            self.treat_checkbox
        )

        self.driver.execute_script(
            "arguments[0].click();",
            checkbox
        )

    def set_top_level(self):

        elements = self.driver.find_elements(
            *self.set_top
        )

        if elements:

            self.driver.execute_script(
                "arguments[0].click();",
                elements[0]
            )

    def run_tariff_analysis(self):

        logger.info(
            "Running Tariff Analysis"
        )

        self.safe_click(self.run_btn)

        self.wait_for_loader()

    # ==========================================================
    # APPROVE BOM
    # ==========================================================

    def approve_bom(self):

        logger.info("Approving BOM")

        element = self.wait_for_clickable(
            self.approve_bom_btn
        )

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

        old_button = self.wait_for_presence(
            (
                By.XPATH,
                "//button[normalize-space()='Export to Excel']"
            )
        )

        self.wait.until(
            EC.staleness_of(old_button)
        )

        self.wait_for_presence(
            (
                By.XPATH,
                "//button[normalize-space()='Export to Excel']"
            )
        )

        self.wait_for_loader()

    # ==========================================================
    # EXPORT BOM
    # ==========================================================

    def export_bom(self, download_dir):

        logger.info("Exporting BOM")

        self.wait_for_page_ready()

        before_files = set(
            os.listdir(download_dir)
        )

        element = self.wait_for_presence(
            self.bom_export_btn
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

        file_path = wait_for_new_file(
            download_dir,
            before_files,
            extension=".xlsx"
        )

        logger.info(
            f"BOM Downloaded: {file_path}"
        )

        return file_path

    # ==========================================================
    # HTS WIZARD
    # ==========================================================

    def complete_hts_wizard(self):

        logger.info(
            "Handling HTS Wizard"
        )

        try:

            for _ in range(5):

                wizard = self.driver.find_elements(
                    By.XPATH,
                    (
                        "//*[contains(text(),"
                        "'nature of the imported good')]"
                    )
                )

                if not wizard:

                    logger.info(
                        "Wizard completed"
                    )

                    return

                options = self.driver.find_elements(
                    By.XPATH,
                    "//label"
                )

                clicked = False

                for option in options:

                    if option.is_displayed():

                        self.driver.execute_script(
                            "arguments[0].click();",
                            option
                        )

                        clicked = True

                        break

                if not clicked:

                    logger.warning(
                        "No visible wizard option found"
                    )

                    break

                continue_btn = (
                    self.wait_for_clickable(
                        (
                            By.XPATH,
                            (
                                "//button[normalize-space()="
                                "'Continue']"
                            )
                        )
                    )
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    continue_btn
                )

                self.wait_for_loader()

        except Exception as e:

            logger.warning(
                f"Wizard handling skipped: {e}"
            )

    # ==========================================================
    # WAIT FOR PROCESSING
    # ==========================================================

    def wait_for_processing_complete(self):

        self.wait.until_not(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    (
                        "//div[contains(@class,'animate-spin') "
                        "or contains(text(),'Processing')]"
                    )
                )
            )
        )

    # ==========================================================
    # EXPORT TARIFF
    # ==========================================================

    def export_tariff(self, download_dir):

        logger.info(
            "Exporting Tariff Report"
        )

        self.wait_for_page_ready()

        before_files = set(
            os.listdir(download_dir)
        )

        buttons = self.wait.until(
            lambda d: d.find_elements(
                *self.tariff_export_btn
            )
        )

        button = buttons[-1]

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            button
        )

        try:

            button.click()

        except Exception:

            self.driver.execute_script(
                "arguments[0].click();",
                button
            )

        file_path = wait_for_new_file(
            download_dir,
            before_files,
            extension=".xlsx"
        )

        logger.info(
            f"Tariff file downloaded: {file_path}"
        )

        return file_path

    # ==========================================================
    # NAVIGATION
    # ==========================================================

    def go_back(self):

        logger.info("Navigating back")

        self.safe_click(self.back_project)

        self.safe_click(self.back_btn)

        self.wait_for_page_ready()