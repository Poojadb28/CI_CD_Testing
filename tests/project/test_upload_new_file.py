import pytest

from selenium.webdriver.common.by import By


@pytest.mark.regression
def test_upload_new_file(
    upload_new_file
):

    project, file_name = (
        upload_new_file
    )

    driver = project.driver

    # ==========================================================
    # PAGE VALIDATION
    # ==========================================================

    project.wait_for_page_ready()

    assert (
        driver.current_url is not None
    ), "Project page not loaded"

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
    # FILE UPLOAD VALIDATION
    # ==========================================================

    is_uploaded = project.verify_file_uploaded(
        file_name
    )

    assert is_uploaded, (
        f"File not uploaded: {file_name}"
    )

    # ==========================================================
    # UI VALIDATION
    # ==========================================================

    uploaded_file = project.wait.until(
        lambda d: d.find_element(
            By.XPATH,
            f"//*[contains(text(),'{file_name}')]"
        )
    )

    assert uploaded_file.is_displayed(), (
        "Uploaded file is not visible"
    )

    # ==========================================================
    # FILE NAME VALIDATION IN UI
    # ==========================================================

    assert (
        file_name.lower()
        in uploaded_file.text.lower()
    ), "Uploaded file name mismatch"

    # ==========================================================
    # FINAL VALIDATION
    # ==========================================================

    assert (
        len(driver.window_handles) > 0
    ), "Browser window closed unexpectedly"

    print(
        f"File uploaded successfully: {file_name}"
    )