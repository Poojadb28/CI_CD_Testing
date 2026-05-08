import os


from selenium.webdriver.common.by import By
from utils.logger import get_logger
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

logger = get_logger(__name__)


class ProjectPage(BasePage):

    def __init__(self, driver):

        super().__init__(driver)

    # ==========================================================
    # PROJECT SECTION
    # ==========================================================

    def click_projects(self):

        logger.info("Opening Projects")

        locator = (
            By.XPATH,
            "//span[normalize-space()='Projects']"
        )

        self.safe_click(locator)

        self.wait_for_page_ready()

        self.wait_for_loader()

        self.wait_for_visibility(
            (
                By.XPATH,
                "//div[contains(@class,'flex-1')]"
            )
        )

    # ==========================================================
    # ROOT SPACE
    # ==========================================================

    def right_click_on_canvas(self):

        self.wait_for_page_ready()

        self.wait_for_loader()

        canvas = self.wait_for_visibility(
            (
                By.XPATH,
                "//div[contains(@class,'flex-1')]"
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            canvas
        )

        ActionChains(self.driver)\
            .move_to_element(canvas)\
            .pause(1)\
            .context_click(canvas)\
            .perform()

        # IMPORTANT FOR JENKINS
        self.wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//*[contains(text(),'New Root Space')]"
                )
            )
        )

    def click_new_root_space(self):

        self.wait_for_page_ready()

        elements = self.wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//*[contains(text(),'New Root Space')]"
                )
            )
        )

        for element in elements:

            if element.is_displayed():

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    element
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    element
                )

                self.wait_for_loader()

                return

        raise Exception(
            "New Root Space option not found"
        )

    def enter_space_name(self, name):

        self.enter_text(
            (
                By.XPATH,
                "//input[@placeholder='e.g. Finance, Project Alpha...']"
            ),
            name
        )

    def open_icon_selector(self):

        self.safe_click(
            (
                By.XPATH,
                "//button[.//*[name()='svg']]"
            )
        )

    def select_color(self):

        self.safe_click(
            (
                By.XPATH,
                "//button[@title='Blue']"
            )
        )

    def click_create_space(self):

        self.safe_click(
            (
                By.XPATH,
                "//button[normalize-space()='Create Space']"
            )
        )

        self.wait_for_loader()

    def get_success_message(self):

        return self.get_text(
            (
                By.XPATH,
                "//div[contains(text(),'Space created successfully')]"
            )
        )

    # ==========================================================
    # SUB SPACE
    # ==========================================================

    def right_click_root_space(self, name):

        locator = (
            By.XPATH,
            f"//*[text()='{name}']"
        )

        self.wait_for_page_ready()

        element = self.wait_for_visibility(locator)

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

        ActionChains(self.driver)\
            .move_to_element(element)\
            .pause(1)\
            .context_click(element)\
            .perform()

        self.wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//*[contains(text(),'Edit')]"
                )
            )
        )

    def click_add_sub_space(self):

        elements = self.wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//*[contains(text(),'Add Sub')]"
                )
            )
        )

        for element in elements:

            if element.is_displayed():

                self.driver.execute_script(
                    "arguments[0].click();",
                    element
                )

                self.wait_for_loader()

                return

        raise Exception(
            "Add Sub Space option not found"
        )

    def enter_sub_space_name(self, name):

        self.enter_text(
            (
                By.XPATH,
                "//input[@placeholder='e.g. Finance, Project Alpha...']"
            ),
            name
        )

    def choose_icon(self):

        self.safe_click(
            (
                By.XPATH,
                "//button[.//*[name()='svg']]"
            )
        )

    def verify_sub_space_created(self, name):

        return self.is_displayed(
            (
                By.XPATH,
                f"//h4[normalize-space()='{name}']"
            )
        )

    # ==========================================================
    # DELETE SPACE
    # ==========================================================

    def click_delete_space(self):

        elements = self.wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//*[contains(text(),'Delete')]"
                )
            )
        )

        for element in elements:

            if element.is_displayed():

                self.driver.execute_script(
                    "arguments[0].click();",
                    element
                )

                return

        raise Exception("Delete option not found")

    def confirm_delete_space(self):

        alert = self.wait_for_alert()

        logger.info(
            f"Alert text: {alert.text}"
        )

        alert.accept()

    def verify_space_deleted(self, name):

        return self.is_displayed(
            (
                By.XPATH,
                (
                    f"//div[contains(text(),"
                    f"'Space \"{name}\" deleted successfully')]"
                )
            )
        )

    # ==========================================================
    # PROJECT CREATION
    # ==========================================================

    def open_root_space(self, name):

        locator = (
            By.XPATH,
            f"//h4[normalize-space()='{name}']"
        )

        self.safe_click(locator)

        self.wait_for_page_ready()

    def click_new_upload(self):

        self.safe_click(
            (
                By.XPATH,
                "//button[normalize-space()='New Upload']"
            )
        )

    def enter_project_name(self, name):

        self.enter_text(
            (
                By.XPATH,
                "//input[@placeholder='Enter project name']"
            ),
            name
        )

    def upload_file(self, file_path):

        file_path = os.path.abspath(file_path)

        logger.info(
            f"Uploading file: {file_path}"
        )

        upload = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//input[@type='file']"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].style.display='block';",
            upload
        )

        upload.send_keys(file_path)

    def click_upload(self):

        self.safe_click(
            (
                By.XPATH,
                "//button[normalize-space()='Upload']"
            )
        )

        self.wait_for_processing_complete()

    def wait_for_processing_complete(self):

        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'fixed inset-0')]"
                )
            )
        )

    def create_project(self, name, file_path):

        self.click_new_upload()

        self.enter_project_name(name)

        self.upload_file(file_path)

        self.click_upload()

    def verify_project_created(self, name):

        return self.is_displayed(
            (
                By.XPATH,
                f"//h3[normalize-space()='{name}']"
            )
        )

    # ==========================================================
    # OPEN PROJECT
    # ==========================================================

    def open_project(self, project_name):

        locator = (
            By.XPATH,
            f"//h3[contains(text(),'{project_name}')]"
        )

        self.wait_for_page_ready()

        self.wait.until(
            lambda d: project_name in d.page_source
        )

        element = self.wait_for_visibility(locator)

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

        try:

            element.click()

        except Exception:

            self.driver.execute_script(
                "arguments[0].click();",
                element
            )

        self.wait_for_loader()

    # ==========================================================
    # VERIFY FILE
    # ==========================================================

    def verify_file_uploaded(self, file_name):

        return self.is_displayed(
            (
                By.XPATH,
                f"//*[contains(text(),'{file_name}')]"
            )
        )

    # ==========================================================
    # EDIT DETAILS
    # ==========================================================

    def click_edit_details(self):

        elements = self.wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//*[contains(text(),'Edit Details')]"
                )
            )
        )

        for element in elements:

            if element.is_displayed():

                self.driver.execute_script(
                    "arguments[0].click();",
                    element
                )

                break

        self.wait.until(
            lambda d: len(
                d.find_elements(
                    By.XPATH,
                    "//input[@type='text']"
                )
            ) > 0
        )

    def edit_space_name(self, new_name):

        inputs = self.wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//input[@type='text']"
                )
            )
        )

        field = None

        for element in inputs:

            if element.is_displayed():

                field = element

                break

        if not field:

            raise Exception(
                "Edit input field not found"
            )

        field.clear()

        field.send_keys(new_name)

    def change_icon(self):

        self.safe_click(
            (
                By.XPATH,
                "//button[.//*[name()='svg']]"
            )
        )

    def select_purple_color(self):

        self.safe_click(
            (
                By.XPATH,
                "//button[@title='Purple']"
            )
        )

    def save_changes(self):

        locators = [
            "//button[contains(text(),'Save')]",
            "//button[contains(text(),'Update')]"
        ]

        for xpath in locators:

            buttons = self.driver.find_elements(
                By.XPATH,
                xpath
            )

            for button in buttons:

                if button.is_displayed():

                    self.driver.execute_script(
                        "arguments[0].click();",
                        button
                    )

                    try:

                        self.wait.until(
                            EC.invisibility_of_element_located(
                                (
                                    By.XPATH,
                                    "//div[contains(@class,'z-50')]"
                                )
                            )
                        )

                    except Exception as e:

                        logger.warning(
                            f"Modal close wait failed: {e}"
                        )

                    return

        raise Exception("Save button not found")

    def verify_space_updated(self, name):

        return self.is_displayed(
            (
                By.XPATH,
                f"//h4[normalize-space()='{name}']"
            )
        )