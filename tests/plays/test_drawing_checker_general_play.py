import os
import pytest


@pytest.mark.regression
def test_drawing_checker_general_play(
    drawing_checker_general_play
):

    general, main_window = (
        drawing_checker_general_play
    )

    driver = general.driver

    # ==========================================================
    # DOWNLOAD DIRECTORY
    # ==========================================================

    download_dir = os.path.abspath(
        "downloads"
    )

    os.makedirs(download_dir, exist_ok=True)

    # ==========================================================
    # PAGE VALIDATION
    # ==========================================================

    general.wait_for_page_ready()

    assert driver.current_url is not None

    # ==========================================================
    # SEARCH VALIDATION
    # ==========================================================

    general.search_issue("major")

    search_box = general.wait.until(
        lambda d: d.find_element(
            *general.search_field
        )
    )

    assert (
        search_box.get_attribute("value")
        == "major"
    ), "Search text not entered"

    general.clear_search()

    assert (
        search_box.get_attribute("value")
        == ""
    ), "Search field not cleared"

    # ==========================================================
    # FILTER VALIDATION
    # ==========================================================

    general.filter_by_severity(
        "Critical"
    )

    severity_dropdown = general.wait.until(
        lambda d: d.find_element(
            *general.severity_dropdown
        )
    )

    assert (
        severity_dropdown.get_attribute("value")
        is not None
    )

    general.filter_by_source(
        "General Engineering"
    )

    source_dropdown = general.wait.until(
        lambda d: d.find_element(
            *general.source_dropdown
        )
    )

    assert (
        source_dropdown.get_attribute("value")
        is not None
    )

    # ==========================================================
    # DRILLDOWN
    # ==========================================================

    general.click_drilldown()

    general.wait_for_page_ready()

    # ==========================================================
    # DOWNLOAD REPORT
    # ==========================================================

    downloaded_file = general.download_report(
        download_dir
    )

    # Validate file returned
    assert downloaded_file is not None, (
        "Download method returned None"
    )

    # Validate file exists
    assert os.path.exists(downloaded_file), (
        f"Downloaded file not found: {downloaded_file}"
    )

    # Validate extension
    assert downloaded_file.endswith(".pdf"), (
        "Downloaded file is not PDF"
    )

    # Validate file size
    assert os.path.getsize(downloaded_file) > 0, (
        "Downloaded PDF is empty"
    )

    print(
        f"Downloaded report: {downloaded_file}"
    )

    # ==========================================================
    # CLEANUP
    # ==========================================================

    driver.close()

    driver.switch_to.window(main_window)

    # ==========================================================
    # FINAL VALIDATION
    # ==========================================================

    assert (
        driver.current_window_handle
        == main_window
    )