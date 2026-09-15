"""Tests for scripts/build_index.py."""

from pathlib import Path

import pytest

from scripts.build_index import find_pdf_files, extract_pdf_metadata


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "literature"


def test_find_pdf_files():
    """Test that PDF files are discovered recursively."""
    pdf_files = find_pdf_files(FIXTURE_DIR)

    assert len(pdf_files) > 0

    for pdf_file in pdf_files:
        assert pdf_file.is_file()
        assert pdf_file.suffix == ".pdf"

    pdf_names = [pdf_file.name for pdf_file in pdf_files]

    assert "Billen_Hirth_2005.pdf" in pdf_names
    assert "Hansen_2007.pdf" in pdf_names
    assert "Hosoya_et_al_2005.pdf" in pdf_names

    assert FIXTURE_DIR / "Billen_Hirth_2005.pdf" in pdf_files
    assert FIXTURE_DIR / "Hansen_2007.pdf" in pdf_files
    assert FIXTURE_DIR / "Hosoya_et_al_2005.pdf" in pdf_files


def test_find_pdf_files_invalid_directory():
    """Test that an invalid input directory raises an error."""
    invalid_directory = FIXTURE_DIR / "directory_that_does_not_exist"

    with pytest.raises(ValueError):
        find_pdf_files(invalid_directory)


def test_extract_pdf_metadata():
    """Test that metadata is extracted from a PDF file."""
    pdf_path = FIXTURE_DIR / "Billen_Hirth_2005.pdf"

    metadata = extract_pdf_metadata(pdf_path)

    assert metadata["title"] == (
        "Newtonian versus non&hyphen;Newtonian upper mantle viscosity: "
        "Implications for subduction initiation"
    )
    assert metadata["author"] == "Magali I. Billen, Greg Hirth"
    assert metadata["subject"] == (
        "Tectonophysics: Dynamics of lithosphere and mantle: general; "
        "Tectonophysics: Plate boundary: general; "
        "Tectonophysics: Rheology: mantle; "
        "Tectonophysics: Subduction zone processes"
    )
    assert metadata["keywords"] == (
        "http://dx.doi.org/10.1029/2005GL023457, "
        "doi:10.1029/2005GL023457"
    )