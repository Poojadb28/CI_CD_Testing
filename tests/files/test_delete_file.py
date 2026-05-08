import pytest

from selenium.webdriver.common.by import By


@pytest.mark.smoke
def test_delete_file(
    delete_file
):

    project, file_name = (
        delete_file
    )

    driver = project.driver

    # ==========================================================
    # PAGE VALIDATION
    # ==========================================================

    project.wait_for_page_ready()

    assert (
        driver.current_url is not None
    ), "Project/File page not loaded"

    # ==========================================================
    # FILE NAME VALIDATION
    # ==========================================================

    assert (
        file_name is not None
    ), "File name is None"

    assert (
        file_name.strip() != ""
    ), "File name is empty"

    # ==========================================================
    # FILE DELETE VALIDATION
    # ==========================================================

    is_deleted = project.is_file_deleted(
        file_name
    )

    assert is_deleted, (
        f"File deletion failed: {file_name}"
    )

    # ==========================================================
    # SUCCESS MESSAGE VALIDATION
    # ==========================================================

    success_message = project.wait.until(
        lambda d: d.find_element(
            By.XPATH,
            (
                f"//*[contains(text(),"
                f"'deleted successfully')]"
            )
        )
    )

    assert success_message.is_displayed(), (
        "Delete success message not displayed"
    )

    assert (
        "deleted successfully"
        in success_message.text.lower()
    ), "Incorrect delete success message"

    # ==========================================================
    # FINAL UI VALIDATION
    # ==========================================================

    deleted_files = driver.find_elements(
        By.XPATH,
        f"//*[contains(text(),'{file_name}')]"
    )

    visible_files = [

        file for file in deleted_files

        if file.is_displayed()
    ]

    assert len(visible_files) == 0, (
        "Deleted file still visible in UI"
    )

    # ==========================================================
    # FINAL VALIDATION
    # ==========================================================

    assert (
        len(driver.window_handles) > 0
    ), "Browser window closed unexpectedly"

    print(
        f"File deleted successfully: {file_name}"
    )