import os
import pytest


@pytest.mark.regression
def test_tariff_analysis_play(
    tariff_analysis_play
):

    tariff = tariff_analysis_play

    # ==========================================================
    # DOWNLOAD DIRECTORY
    # ==========================================================

    download_dir = os.path.abspath("downloads")

    os.makedirs(download_dir, exist_ok=True)

    # ==========================================================
    # PAGE VALIDATION
    # ==========================================================

    tariff.wait_for_page_ready()

    assert tariff.driver.current_url is not None

    # ==========================================================
    # EXPORT BOM
    # ==========================================================

    bom_file = tariff.export_bom(download_dir)

    # Validate file path returned
    assert bom_file is not None, (
        "BOM export did not return file path"
    )

    # Validate file exists
    assert os.path.exists(bom_file), (
        f"BOM file not found: {bom_file}"
    )

    # Validate extension
    assert bom_file.endswith(".xlsx"), (
        "BOM export is not XLSX"
    )

    # Validate file size
    assert os.path.getsize(bom_file) > 0, (
        "BOM file is empty"
    )

    print(f"BOM Downloaded: {bom_file}")

    # ==========================================================
    # APPROVE BOM
    # ==========================================================

    tariff.approve_bom()

    tariff.wait_for_loader()

    # ==========================================================
    # COMPLETE HTS WIZARD
    # ==========================================================

    tariff.complete_hts_wizard()

    tariff.wait_for_processing_complete()

    # ==========================================================
    # EXPORT TARIFF
    # ==========================================================

    tariff_file = tariff.export_tariff(
        download_dir
    )

    # Validate file path returned
    assert tariff_file is not None, (
        "Tariff export did not return file path"
    )

    # Validate file exists
    assert os.path.exists(tariff_file), (
        f"Tariff file not found: {tariff_file}"
    )

    # Validate extension
    assert tariff_file.endswith(".xlsx"), (
        "Tariff export is not XLSX"
    )

    # Validate filename contains tariff
    assert "tariff" in os.path.basename(
        tariff_file
    ).lower(), (
        "Downloaded file is not tariff report"
    )

    # Validate file size
    assert os.path.getsize(tariff_file) > 0, (
        "Tariff file is empty"
    )

    print(f"Tariff Downloaded: {tariff_file}")

    # ==========================================================
    # BACK NAVIGATION
    # ==========================================================

    tariff.go_back()

    tariff.wait_for_page_ready()

    # ==========================================================
    # FINAL VALIDATION
    # ==========================================================

    assert tariff.driver.current_url is not None