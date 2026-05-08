import pytest

from selenium.webdriver.common.by import By


@pytest.mark.smoke
def test_delete_project(
    delete_project
):

    project, project_name = (
        delete_project
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
    # PROJECT DELETE VALIDATION
    # ==========================================================

    is_deleted = project.verify_project_deleted(
        project_name
    )

    assert is_deleted, (
        f"Project deletion failed: {project_name}"
    )

    # ==========================================================
    # SUCCESS MESSAGE VALIDATION
    # ==========================================================

    success_message = project.wait.until(
        lambda d: d.find_element(
            By.XPATH,
            (
                f"//*[contains(text(),"
                f"'Project \"{project_name}\" deleted successfully')]"
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
    # FINAL VALIDATION
    # ==========================================================

    deleted_projects = driver.find_elements(
        By.XPATH,
        f"//h3[normalize-space()='{project_name}']"
    )

    assert len(deleted_projects) == 0, (
        "Deleted project still visible in UI"
    )

    print(
        f"Project deleted successfully: {project_name}"
    )