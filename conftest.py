# pytest_plugins = [
#     "fixtures.systemadmin_login_fixture",
#     "fixtures.user_creation_fixture",
#     "fixtures.admin_creation_fixture",
#     "fixtures.logout_fixture",
#     "fixtures.project_fixture",
#     "fixtures.subspace_fixture",
#     "fixtures.delete_root_space_fixture",
#     "fixtures.project_creation_fixture",
#     "fixtures.project_upload_fixture",
#     "fixtures.file_upload_fixture",
#     "fixtures.edit_space_fixture",
#     "fixtures.delete_project_fixture",
#     "fixtures.search_file_fixture",
#     "fixtures.available_plays_fixture",
#     "fixtures.cost_reduction_play_fixture",
#     "fixtures.design_review_fixture",
#     "fixtures.drawing_checker_both_play_fixture",
#     "fixtures.drawing_checker_general_play_fixture",
#     "fixtures.drawing_checker_v2_play_fixture",
#     "fixtures.drawing_checker_veeco_play_fixture",
#     "fixtures.tariff_analysis_play_fixture",
#     "fixtures.download_logs_fixture",
#     "fixtures.delete_file_fixture",
#     "fixtures.select_deselect_all_files_fixture",
#     "fixtures.filter_labels_fixture",
#     "fixtures.create_new_project_fixture",
#     "fixtures.export_credit_history_fixture",
#     "fixtures.export_classification_to_excel_fixture",
#     "fixtures.duplicate_admin_creation_fixture",
#     "fixtures.duplicate_user_creation_fixture",
#     "fixtures.systemadmin_creation_fixture",
#     "fixtures.duplicate_systemadmin_creation_fixture",
#     "fixtures.weight_estimation_play_fixture"
# ]

# import pytest
# import sys
# import os

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options


# # =========================
# # FIX IMPORT PATH (IMPORTANT FOR JENKINS)
# # =========================
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, BASE_DIR)


# # =========================
# # ADD COMMAND LINE OPTION
# # =========================
# def pytest_addoption(parser):
#     parser.addoption(
#         "--browser",
#         action="store",
#         default="chrome",
#         help="Browser to run tests"
#     )


# # =========================
# # DRIVER SETUP
# # =========================
# # @pytest.fixture(scope="function")
# # def browser(request):
# #     browser_name = request.config.getoption("--browser")

# #     if browser_name == "chrome":
# #         chrome_options = Options()

# #         # Required for Jenkins / headless
# #         chrome_options.add_argument("--headless=new")
# #         chrome_options.add_argument("--no-sandbox")
# #         chrome_options.add_argument("--disable-dev-shm-usage")
# #         chrome_options.add_argument("--disable-gpu")
# #         chrome_options.add_argument("--window-size=1920,1080")

# #         download_dir = os.path.abspath("downloads")
# #         os.makedirs(download_dir, exist_ok=True)

# #         # Fix download / security issues
# #         prefs = {
# #             "download.default_directory": download_dir,
# #             "download.prompt_for_download": False,
# #             "download.directory_upgrade": True,
# #             "safebrowsing.enabled": True,

# #             "profile.default_content_setting_values.automatic_downloads": 1
# #         }
# #         chrome_options.add_experimental_option("prefs", prefs)

# #         driver = webdriver.Chrome(
# #         executable_path="drivers/chromedriver.exe",
# #         options=chrome_options
# #         )

# #     else:
# #         raise Exception(f"Browser {browser_name} not supported")

# #     driver.implicitly_wait(10)

# #     yield driver

# #     driver.quit()

# @pytest.fixture(scope="function")
# def browser(request):
#     browser_name = request.config.getoption("--browser")

#     if browser_name == "chrome":
#         chrome_options = Options()

#         # Required for Jenkins / headless
#         chrome_options.add_argument("--headless=new")
#         chrome_options.add_argument("--no-sandbox")
#         chrome_options.add_argument("--disable-dev-shm-usage")
#         chrome_options.add_argument("--disable-gpu")
#         chrome_options.add_argument("--window-size=1920,1080")

#         # Shared download folder (no fixture changes needed)
#         download_dir = os.path.abspath("downloads")
#         os.makedirs(download_dir, exist_ok=True)

#         # Clean folder before each test (VERY IMPORTANT)
#         for f in os.listdir(download_dir):
#             try:
#                 os.remove(os.path.join(download_dir, f))
#             except:
#                 pass

#         # Chrome download preferences
#         prefs = {
#             "download.default_directory": download_dir,
#             "download.prompt_for_download": False,
#             "download.directory_upgrade": True,
#             "safebrowsing.enabled": True,
#             "profile.default_content_setting_values.automatic_downloads": 1
#         }
#         chrome_options.add_experimental_option("prefs", prefs)

#         driver = webdriver.Chrome(
#             executable_path="drivers/chromedriver.exe",
#             options=chrome_options
#         )

#         # Optional: attach for future use (no need to change tests now)
#         driver.download_dir = download_dir

#     else:
#         raise Exception(f"Browser {browser_name} not supported")

#     driver.implicitly_wait(10)

#     yield driver

#     driver.quit()


# # =========================
# # PYTEST HOOK (OPTIONAL - FOR LOGGING)
# # =========================
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()

#     if report.when == "call" and report.failed:
#         driver = item.funcargs.get("browser", None)
#         if driver:
#             screenshots_dir = os.path.join(BASE_DIR, "screenshots")
#             os.makedirs(screenshots_dir, exist_ok=True)

#             file_name = os.path.join(
#                 screenshots_dir,
#                 f"{item.name}.png"
#             )
#             driver.save_screenshot(file_name)

# pytest_plugins = [
#     "fixtures.systemadmin_login_fixture",
#     "fixtures.user_creation_fixture",
#     "fixtures.admin_creation_fixture",
#     "fixtures.logout_fixture",
#     "fixtures.project_fixture",
#     "fixtures.subspace_fixture",
#     "fixtures.delete_root_space_fixture",
#     "fixtures.project_creation_fixture",
#     "fixtures.project_upload_fixture",
#     "fixtures.file_upload_fixture",
#     "fixtures.edit_space_fixture",
#     "fixtures.delete_project_fixture",
#     "fixtures.search_file_fixture",
#     "fixtures.available_plays_fixture",
#     "fixtures.cost_reduction_play_fixture",
#     "fixtures.design_review_fixture",
#     "fixtures.drawing_checker_both_play_fixture",
#     "fixtures.drawing_checker_v2_play_fixture",
#     "fixtures.drawing_checker_general_play_fixture",
#     "fixtures.drawing_checker_veeco_play_fixture",
#     "fixtures.tariff_analysis_play_fixture",
#     "fixtures.download_logs_fixture",
#     "fixtures.delete_file_fixture",
#     "fixtures.select_deselect_all_files_fixture",
#     "fixtures.filter_labels_fixture",
#     "fixtures.create_new_project_fixture",
#     "fixtures.export_credit_history_fixture",
#     "fixtures.export_classification_to_excel_fixture",
#     "fixtures.duplicate_admin_creation_fixture",
#     "fixtures.duplicate_user_creation_fixture",
#     "fixtures.systemadmin_creation_fixture",
#     "fixtures.duplicate_systemadmin_creation_fixture",
#     "fixtures.weight_estimation_play_fixture"
# ]

# import pytest
# import sys
# import os
# from datetime import datetime

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

# # Safe import for report plugin
# try:
#     import pytest_html
# except ImportError:
#     pytest_html = None


# # =========================
# # PATH SETUP
# # =========================
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, BASE_DIR)


# # =========================
# # CLI OPTIONS
# # =========================
# def pytest_addoption(parser):
#     parser.addoption("--browser", action="store", default="chrome")
#     parser.addoption("--headless", action="store_true", help="Run in headless mode")


# # =========================
# # SAFE DRIVER SETUP
# # =========================
# def get_driver_service():
#     try:
#         path = ChromeDriverManager().install()

#         # Fix for Windows chromedriver path issue
#         if "THIRD_PARTY_NOTICES" in path:
#             path = os.path.join(os.path.dirname(path), "chromedriver.exe")

#         return Service(path)

#     except Exception:
#         # Fallback (VERY IMPORTANT for Jenkins / offline)
#         local_path = os.path.join(BASE_DIR, "drivers", "chromedriver.exe")

#         if not os.path.exists(local_path):
#             raise Exception("Chromedriver not found locally or via webdriver-manager")

#         return Service(local_path)


# # =========================
# # BROWSER FIXTURE
# # =========================
# @pytest.fixture(scope="function")
# def browser(request):
#     browser_name = request.config.getoption("--browser")
#     headless = request.config.getoption("--headless")

#     if browser_name.lower() == "chrome":
#         chrome_options = Options()

#         if headless:
#             chrome_options.add_argument("--headless=new")

#         # Stability for Jenkins
#         chrome_options.add_argument("--no-sandbox")
#         chrome_options.add_argument("--disable-dev-shm-usage")
#         chrome_options.add_argument("--disable-gpu")
#         chrome_options.add_argument("--window-size=1920,1080")

#         # Download directory setup
#         download_dir = os.path.join(BASE_DIR, "downloads")
#         os.makedirs(download_dir, exist_ok=True)

#         prefs = {
#             "download.default_directory": download_dir,
#             "download.prompt_for_download": False,
#             "download.directory_upgrade": True,
#             "safebrowsing.enabled": True,
#             "profile.default_content_setting_values.automatic_downloads": 1
#         }
#         chrome_options.add_experimental_option("prefs", prefs)

#         service = get_driver_service()
#         driver = webdriver.Chrome(service=service, options=chrome_options)

#     else:
#         raise Exception(f"Unsupported browser: {browser_name}")

#     driver.implicitly_wait(10)

#     yield driver

#     driver.quit()


# # =========================
# # SCREENSHOT + HTML REPORT
# # =========================
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()

#     if report.when == "call" and report.failed:
#         driver = item.funcargs.get("browser", None)

#         if driver:
#             screenshots_dir = os.path.join(BASE_DIR, "screenshots")
#             os.makedirs(screenshots_dir, exist_ok=True)

#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             file_name = f"{item.name}_{timestamp}.png"
#             file_path = os.path.join(screenshots_dir, file_name)

#             driver.save_screenshot(file_path)

#             # Attach screenshot to HTML report
#             if pytest_html:
#                 extra = getattr(report, "extra", [])
#                 extra.append(pytest_html.extras.image(file_path))
#                 report.extra = extra

pytest_plugins = [
    "fixtures.systemadmin_login_fixture",
    "fixtures.user_creation_fixture",
    "fixtures.admin_creation_fixture",
    "fixtures.logout_fixture",
    "fixtures.project_fixture",
    "fixtures.subspace_fixture",
    "fixtures.delete_root_space_fixture",
    "fixtures.project_creation_fixture",
    "fixtures.project_upload_fixture",
    "fixtures.file_upload_fixture",
    "fixtures.edit_space_fixture",
    "fixtures.delete_project_fixture",
    "fixtures.search_file_fixture",
    "fixtures.available_plays_fixture",
    "fixtures.cost_reduction_play_fixture",
    "fixtures.design_review_fixture",
    "fixtures.drawing_checker_both_play_fixture",
    "fixtures.drawing_checker_v2_play_fixture",
    "fixtures.drawing_checker_general_play_fixture",
    "fixtures.drawing_checker_veeco_play_fixture",
    "fixtures.tariff_analysis_play_fixture",
    "fixtures.download_logs_fixture",
    "fixtures.delete_file_fixture",
    "fixtures.select_deselect_all_files_fixture",
    "fixtures.filter_labels_fixture",
    "fixtures.create_new_project_fixture",
    "fixtures.export_credit_history_fixture",
    "fixtures.export_classification_to_excel_fixture",
    "fixtures.duplicate_admin_creation_fixture",
    "fixtures.duplicate_user_creation_fixture",
    "fixtures.systemadmin_creation_fixture",
    "fixtures.duplicate_systemadmin_creation_fixture",
    "fixtures.weight_estimation_play_fixture"
]

import os
import sys
from datetime import datetime

import pytest

from selenium import webdriver
from utils.logger import get_logger
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager

# =========================
# OPTIONAL HTML REPORT
# =========================
try:
    import pytest_html
except ImportError:
    pytest_html = None


# =========================
# BASE DIRECTORY
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)


# =========================
# CREATE REQUIRED FOLDERS
# =========================
REQUIRED_DIRS = [
    "screenshots",
    "reports",
    "downloads",
    "logs",
    "page_source"
]

for folder in REQUIRED_DIRS:
    os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)


# =========================
# LOGGING CONFIGURATION
# =========================

logger = get_logger(__name__)


# =========================
# PYTEST CLI OPTIONS
# =========================
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser Name"
    )

    parser.addoption(
        "--headless",
        action="store_true",
        help="Run browser in headless mode"
    )


# =========================
# SAFE CHROMEDRIVER SERVICE
# =========================
def get_driver_service():
    """
    Stable chromedriver setup for:
    - Local execution
    - Jenkins execution
    - Offline execution
    """

    try:
        path = ChromeDriverManager().install()

        # webdriver-manager Windows fix
        if "THIRD_PARTY_NOTICES" in path:
            path = os.path.join(
                os.path.dirname(path),
                "chromedriver.exe"
            )

        logger.info(f"Using WebDriverManager driver: {path}")

        return Service(path)

    except Exception as e:

        logger.warning(
            f"WebDriverManager failed: {str(e)}"
        )

        local_driver = os.path.join(
            BASE_DIR,
            "drivers",
            "chromedriver.exe"
        )

        if not os.path.exists(local_driver):
            raise FileNotFoundError(
                "Chromedriver not found locally or via webdriver-manager"
            )

        logger.info(f"Using local driver: {local_driver}")

        return Service(local_driver)


# =========================
# BROWSER FIXTURE
# =========================
@pytest.fixture(scope="function")
def browser(request):

    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    logger.info(f"Starting browser: {browser_name}")

    if browser_name.lower() != "chrome":
        raise ValueError(f"Unsupported browser: {browser_name}")

    chrome_options = Options()

    # =========================
    # HEADLESS MODE
    # =========================
    if headless:
        chrome_options.add_argument("--headless=new")

    # =========================
    # JENKINS STABILITY OPTIONS
    # =========================
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1920,1080")

    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")

    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-running-insecure-content")

    chrome_options.add_argument("--remote-allow-origins=*")

    # =========================
    # PERFORMANCE IMPROVEMENTS
    # =========================
    chrome_options.page_load_strategy = "normal"

    chrome_options.add_experimental_option(
        "excludeSwitches",
        ["enable-logging"]
    )

    # =========================
    # DOWNLOAD SETTINGS
    # =========================
    download_dir = os.path.join(BASE_DIR, "downloads")

    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "profile.default_content_setting_values.automatic_downloads": 1
    }

    chrome_options.add_experimental_option("prefs", prefs)

    # =========================
    # DRIVER CREATION
    # =========================
    service = get_driver_service()

    driver = webdriver.Chrome(
        service=service,
        options=chrome_options
    )

    # =========================
    # DRIVER CONFIGURATION
    # =========================
    driver.maximize_window()

    driver.implicitly_wait(5)
    driver.set_page_load_timeout(120)

    logger.info("Browser launched successfully")

    yield driver

    # =========================
    # CLEANUP
    # =========================
    try:
        driver.quit()
        logger.info("Browser closed successfully")

    except Exception as e:
        logger.error(f"Driver quit failed: {str(e)}")


# =========================
# EXPLICIT WAIT FIXTURE
# =========================
@pytest.fixture(scope="function")
def wait(browser):
    return WebDriverWait(browser, 20)


# =========================
# PYTEST REPORT HEADER
# =========================
def pytest_configure(config):
    config._metadata = {
        "Project": "Veeco Sourceoptima",
        "Framework": "PyTest + Selenium",
        "Execution": "Jenkins Compatible"
    }


# =========================
# SCREENSHOT ON FAILURE
# =========================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    setattr(item, "rep_" + report.when, report)

    if report.when == "call" and report.failed:

        driver = item.funcargs.get("browser", None)

        if driver:

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            test_name = item.name

            screenshot_path = os.path.join(
                BASE_DIR,
                "screenshots",
                f"{test_name}_{timestamp}.png"
            )

            html_path = os.path.join(
                BASE_DIR,
                "page_source",
                f"{test_name}_{timestamp}.html"
            )

            try:
                # =========================
                # SAVE SCREENSHOT
                # =========================
                driver.save_screenshot(screenshot_path)

                logger.error(
                    f"Screenshot saved: {screenshot_path}"
                )

                # =========================
                # SAVE PAGE SOURCE
                # =========================
                with open(
                    html_path,
                    "w",
                    encoding="utf-8"
                ) as f:
                    f.write(driver.page_source)

                logger.error(
                    f"Page source saved: {html_path}"
                )

                # =========================
                # HTML REPORT ATTACHMENT
                # =========================
                if pytest_html:
                    extra = getattr(report, "extra", [])

                    extra.append(
                        pytest_html.extras.image(
                            screenshot_path
                        )
                    )

                    report.extra = extra

            except Exception as e:
                logger.error(
                    f"Failed to capture screenshot: {str(e)}"
                )