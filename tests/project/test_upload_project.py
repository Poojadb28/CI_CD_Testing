import pytest

from selenium.webdriver.common.by import By


@pytest.mark.smoke
def test_add_new_project(
    upload_project
):

    projects, project_name = (
        upload_project
    )

    driver = projects.driver

    # ==========================================================
    # PAGE VALIDATION
    # ==========================================================

    projects.wait_for_page_ready()

    assert (
        driver.current_url is not None
    ), "Project page not loaded"

    # ==========================================================
    # PROJECT NAME VALIDATION
    # ==========================================================

    assert (
        project_name is not None
    ), "Project name is None"

    assert (
        project_name.strip() != ""
    ), "Project name is empty"

    # ==========================================================
    # PROJECT CREATION VALIDATION
    # ==========================================================

    is_created = projects.verify_project_created(
        project_name
    )

    assert is_created, (
        f"Project not created: {project_name}"
    )

    # ==========================================================
    # UI VALIDATION
    # ==========================================================

    created_project = projects.wait.until(
        lambda d: d.find_element(
            By.XPATH,
            f"//h3[normalize-space()='{project_name}']"
        )
    )

    assert created_project.is_displayed(), (
        "Created project is not visible"
    )

    # ==========================================================
    # PROJECT TEXT VALIDATION
    # ==========================================================

    assert (
        created_project.text.strip()
        == project_name
    ), "Project name mismatch"

    # ==========================================================
    # FINAL VALIDATION
    # ==========================================================

    assert (
        len(driver.window_handles) > 0
    ), "Browser window closed unexpectedly"

    print(
        f"Project uploaded successfully: {project_name}"
    )