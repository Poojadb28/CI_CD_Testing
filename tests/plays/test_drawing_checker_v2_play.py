import os
import pytest


@pytest.mark.regression
def test_drawing_checker_v2_play(
    drawing_checker_v2_play
):

    v2, main_window = (
        drawing_checker_v2_play
    )

    driver = v2.driver

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

    v2.wait_for_page_ready()

    assert driver.current_url is not None

    # ==========================================================
    # SEARCH VALIDATION
    # ==========================================================

    v2.search_issue("major")

    search_box = v2.wait.until(
        lambda d: d.find_element(
            *v2.search_field
        )
    )

    assert (
        search_box.get_attribute("value")
        == "major"
    ), "Search text not entered"

    v2.clear_search()

    assert (
        search_box.get_attribute("value")
        == ""
    ), "Search field not cleared"

    # ==========================================================
    # SEVERITY FILTER VALIDATION
    # ==========================================================

    v2.filter_by_severity(
        "Critical"
    )

    severity_dropdown = v2.wait.until(
        lambda d: d.find_element(
            *v2.severity_dropdown
        )
    )

    assert (
        severity_dropdown.get_attribute("value")
        is not None
    )

    v2.filter_by_severity(
        "All Severities"
    )

    # ==========================================================
    # SOURCE FILTER VALIDATION
    # ==========================================================

    v2.filter_by_source(
        "General Engineering"
    )

    source_dropdown = v2.wait.until(
        lambda d: d.find_element(
            *v2.source_dropdown
        )
    )

    assert (
        source_dropdown.get_attribute("value")
        is not None
    )

    v2.filter_by_source(
        "All Sources"
    )

    # ==========================================================
    # DRILLDOWN
    # ==========================================================

    v2.click_drilldown()

    v2.wait_for_page_ready()

    # ==========================================================
    # DOWNLOAD REPORT
    # ==========================================================

    downloaded_file = v2.download_report(
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