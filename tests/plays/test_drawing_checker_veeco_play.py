import os
import pytest


@pytest.mark.regression
def test_drawing_checker_veeco_play(
    drawing_checker_veeco_play
):

    veeco, main_window = (
        drawing_checker_veeco_play
    )

    driver = veeco.driver

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

    veeco.wait_for_page_ready()

    assert driver.current_url is not None

    # ==========================================================
    # SEARCH VALIDATION
    # ==========================================================

    veeco.search_issue("minor")

    search_box = veeco.wait.until(
        lambda d: d.find_element(
            *veeco.search_field
        )
    )

    assert (
        search_box.get_attribute("value")
        == "minor"
    ), "Search text not entered"

    veeco.clear_search()

    assert (
        search_box.get_attribute("value")
        == ""
    ), "Search field not cleared"

    # ==========================================================
    # SEVERITY FILTER VALIDATION
    # ==========================================================

    veeco.filter_by_severity(
        "Major"
    )

    severity_dropdown = veeco.wait.until(
        lambda d: d.find_element(
            *veeco.severity_dropdown
        )
    )

    assert (
        severity_dropdown.get_attribute("value")
        is not None
    )

    veeco.filter_by_severity(
        "All Severities"
    )

    # ==========================================================
    # SOURCE FILTER VALIDATION
    # ==========================================================

    veeco.filter_by_source(
        "Veeco Standards"
    )

    source_dropdown = veeco.wait.until(
        lambda d: d.find_element(
            *veeco.source_dropdown
        )
    )

    assert (
        source_dropdown.get_attribute("value")
        is not None
    )

    veeco.filter_by_source(
        "All Sources"
    )

    # ==========================================================
    # DRILLDOWN
    # ==========================================================

    veeco.click_drilldown()

    veeco.wait_for_page_ready()

    # ==========================================================
    # DOWNLOAD REPORT
    # ==========================================================

    downloaded_file = veeco.download_report(
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