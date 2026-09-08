from pathlib import Path

from scripts.extract_summary import (
    extract_takeaways,
    validate_summary_format,
)


MARKDOWN_FIXTURE_DIR = (
    Path(__file__).parent / "fixtures" / "markdown_summary"
)

SUMMARY_FILE = (
    MARKDOWN_FIXTURE_DIR
    / "Clift04RG_ControlsTectAccretionSubductionErosion_1.md"
)


def test_validate_summary_format():
    """Test that a correctly formatted literature summary is accepted."""
    with SUMMARY_FILE.open("r", encoding="utf-8") as file:
        markdown_text = file.read()

    validate_summary_format(markdown_text)


def test_extract_takeaways():
    """Test extraction of takeaway summaries."""
    with SUMMARY_FILE.open("r", encoding="utf-8") as file:
        markdown_text = file.read()

    takeaways = extract_takeaways(markdown_text)

    assert len(takeaways) == 5

    assert takeaways[0] == (
        "Whether a convergent margin is accretionary or erosive is controlled "
        "primarily by convergence rate and trench-sediment thickness."
    )

    assert takeaways[1] == (
        "Sediment accretion is inefficient, so both accretionary and erosive "
        "margins transfer large volumes of crustal material beneath the forearc."
    )

    assert takeaways[2] == (
        "Long-term forearc erosion has no simple steady first-order control; "
        "episodic collision of major oceanic ridges is the strongest identified "
        "accelerator."
    )

    assert takeaways[3] == (
        "Arc magmatism, distributed mainly according to convergence rate, must "
        "balance large tectonic losses and dominates the creation of new crust "
        "at active margins."
    )

    assert takeaways[4] == (
        "The global budget implies rapid continental-crust recycling and "
        "requires oceanic-arc accretion to offset loss at erosive continental "
        "margins."
    )