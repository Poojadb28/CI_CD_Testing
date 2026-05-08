import pytest


@pytest.mark.smoke
def test_create_new_project(
    create_new_project
):

    project, project_name = (
        create_new_project
    )

    # ==========================================================
    # PAGE VALIDATION
    # ==========================================================

    project.wait_for_page_ready()

    assert (
        project.driver.current_url is not None
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
    # UI VALIDATION
    # ==========================================================

    created_project = project.wait.until(
        lambda d: d.find_element(
            *(
                "xpath",
                f"//h3[normalize-space()='{project_name}']"
            )
        )
    )

    assert created_project.is_displayed(), (
        "Created project is not visible"
    )

    print(
        f"Project created successfully: {project_name}"
    )