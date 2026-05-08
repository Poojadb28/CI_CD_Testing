import pytest

from selenium.webdriver.common.by import By


@pytest.mark.smoke
def test_create_project(
    create_project
):

    project, project_name = (
        create_project
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

    is_created = project.verify_project_created(
        project_name
    )

    assert is_created, (
        f"Project not created: {project_name}"
    )

    # ==========================================================
    # UI ELEMENT VALIDATION
    # ==========================================================

    created_project = project.wait.until(
        lambda d: d.find_element(
            By.XPATH,
            f"//h3[normalize-space()='{project_name}']"
        )
    )

    assert created_project.is_displayed(), (
        "Created project is not visible in UI"
    )

    # ==========================================================
    # FINAL VALIDATION
    # ==========================================================

    assert (
        created_project.text.strip()
        == project_name
    ), "Project name mismatch"

    print(
        f"Project created successfully: {project_name}"
    )