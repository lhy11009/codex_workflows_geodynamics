import json
import subprocess
import sys
from pathlib import Path

import pytest

import scripts.extract_summary as extract_summary_module
from scripts.extract_summary import (
    build_jsonl_index,
    extract_title,
    extract_takeaways,
    find_markdown_files,
    match_pdf_file,
    validate_summary_format,
)


MARKDOWN_FIXTURE_DIR = (
    Path(__file__).parent / "fixtures" / "markdown_summary"
)
LITERATURE_FIXTURE_DIR = Path(__file__).parent / "fixtures" / "literature"

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


def test_extract_takeaways_without_figure_summaries():
    """Test that figure summaries are optional."""
    markdown_text = (
        "# A paper title\n\n"
        "## Key takeaways\n\n"
        "### Takeaway 1\n\n"
        "**Summary:** A result.\n"
    )

    assert extract_takeaways(markdown_text) == ["A result."]


def test_extract_methods():
    """Test extraction of optional method highlights."""
    markdown_text = (
        "# A paper title\n\n"
        "## Key takeaways\n\n"
        "### Takeaway 1\n\n"
        "**Summary:** A result.\n\n"
        "## Methods\n\n"
        "### Method 1\n\n"
        "**Method:** Thin-viscous-shell scaling analysis\n\n"
        "- **Setup:** Detailed setup.\n"
        "- **Purpose:** First purpose.\n\n"
        "### Method 2\n\n"
        "**Method:** Axisymmetric boundary-element modeling\n\n"
        "- **Setup:** Another setup.\n"
        "- **Purpose:** Second purpose.\n\n"
        "## Figure summaries\n"
    )

    assert extract_summary_module.extract_methods(markdown_text) == [
        "Thin-viscous-shell scaling analysis",
        "Axisymmetric boundary-element modeling",
    ]


def test_extract_methods_without_methods_section():
    """Test that a Methods section is optional."""
    markdown_text = make_summary("A paper title", ["A result."])

    assert extract_summary_module.extract_methods(markdown_text) == []


def make_summary(title: str, takeaways: list[str], front_matter: str = "") -> str:
    """Create a minimal valid literature summary."""
    takeaway_text = "\n\n".join(
        f"### Takeaway {number}\n\n**Summary:** {takeaway}"
        for number, takeaway in enumerate(takeaways, start=1)
    )
    return (
        f"{front_matter}# {title}\n\n"
        f"## Key takeaways\n\n{takeaway_text}\n\n"
        "## Figure summaries\n"
    )


def test_extract_title():
    markdown_text = make_summary("A paper title", ["A result."])

    assert extract_title(markdown_text) == "A paper title"


def test_extract_title_requires_one_level_one_heading():
    markdown_text = make_summary("A paper title", ["A result."])
    markdown_text += "\n# A second title\n"

    with pytest.raises(ValueError, match="exactly one level-one heading"):
        extract_title(markdown_text)


def test_find_markdown_files_accepts_file_and_directory(tmp_path):
    nested_directory = tmp_path / "nested"
    nested_directory.mkdir()
    first = tmp_path / "b.md"
    second = nested_directory / "a.md"
    ignored = tmp_path / "notes.txt"
    first.write_text("first", encoding="utf-8")
    second.write_text("second", encoding="utf-8")
    ignored.write_text("ignored", encoding="utf-8")

    assert find_markdown_files(first) == [first]
    assert find_markdown_files(tmp_path) == sorted([first, second])


def test_match_pdf_file_uses_front_matter(tmp_path):
    summary = tmp_path / "renamed_summary.md"
    summary.write_text(
        make_summary(
            "Paper",
            ["Result."],
            front_matter="---\npdf: original.pdf\n---\n",
        ),
        encoding="utf-8",
    )
    pdf = tmp_path / "original.pdf"
    pdf.touch()

    assert match_pdf_file(summary, [pdf]) == pdf


def test_match_pdf_file_uses_stem_and_numbered_suffix(tmp_path):
    pdf = tmp_path / "paper.pdf"
    pdf.touch()
    exact_summary = tmp_path / "paper.md"
    numbered_summary = tmp_path / "paper_2.md"
    exact_summary.touch()
    numbered_summary.touch()

    assert match_pdf_file(exact_summary, [pdf]) == pdf
    assert match_pdf_file(numbered_summary, [pdf]) == pdf


def test_match_pdf_file_selects_first_ambiguous_filename(tmp_path):
    summary = tmp_path / "paper.md"
    summary.touch()
    first_pdf = tmp_path / "first" / "paper.pdf"
    second_pdf = tmp_path / "second" / "paper.pdf"
    first_pdf.parent.mkdir()
    second_pdf.parent.mkdir()
    first_pdf.touch()
    second_pdf.touch()

    assert match_pdf_file(summary, [first_pdf, second_pdf]) == first_pdf


def test_match_pdf_file_rejects_missing_pdf(tmp_path):
    summary = tmp_path / "missing.md"
    summary.touch()

    with pytest.raises(ValueError, match="No PDF match found"):
        match_pdf_file(summary, [])


def test_build_jsonl_index(tmp_path, monkeypatch):
    summary_directory = tmp_path / "summaries"
    literature_directory = tmp_path / "literature"
    summary_directory.mkdir()
    literature_directory.mkdir()

    (summary_directory / "paper_b.md").write_text(
        make_summary("Paper B", ["Result B1.", "Result B2."]),
        encoding="utf-8",
    )
    (summary_directory / "paper_a.md").write_text(
        make_summary("Päper A", ["Résult A1."]),
        encoding="utf-8",
    )
    first_pdf = literature_directory / "paper_a.pdf"
    second_pdf = literature_directory / "paper_b.pdf"
    first_pdf.touch()
    second_pdf.touch()

    accessed_pdfs = []

    def record_pdf_access(pdf_path):
        accessed_pdfs.append(pdf_path)
        return {
            "filename": pdf_path.name,
            "author": f"Author of {pdf_path.stem}",
        }

    monkeypatch.setattr(
        extract_summary_module,
        "extract_pdf_metadata",
        record_pdf_access,
    )

    output_path = tmp_path / "index.jsonl"
    build_jsonl_index(
        summary_directory,
        literature_directory,
        output_path,
    )

    records = [
        json.loads(line)
        for line in output_path.read_text(encoding="utf-8").splitlines()
    ]

    assert records == [
        {
            "title": "Päper A",
            "author": "Author of paper_a",
            "source": "paper_a.md",
            "pdf": "paper_a.pdf",
            "takeaways": ["Résult A1."],
        },
        {
            "title": "Paper B",
            "author": "Author of paper_b",
            "source": "paper_b.md",
            "pdf": "paper_b.pdf",
            "takeaways": ["Result B1.", "Result B2."],
        },
    ]
    assert accessed_pdfs == [first_pdf, second_pdf]
    assert "Päper A" in output_path.read_text(encoding="utf-8")
    assert json.loads(
        (tmp_path / "match_report.json").read_text(encoding="utf-8")
    ) == {
        "summaries_without_pdf": [],
        "pdfs_without_summary": [],
        "ambiguous_pdf_matches": [],
    }


def test_direct_cli_help_runs():
    script_path = Path(__file__).parents[1] / "scripts" / "extract_summary.py"

    result = subprocess.run(
        [sys.executable, str(script_path), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "--literature" in result.stdout
    assert "--report-output" in result.stdout
    assert "--unmatched-output" not in result.stdout


def test_direct_cli_builds_index(tmp_path):
    script_path = Path(__file__).parents[1] / "scripts" / "extract_summary.py"
    summary_path = tmp_path / "Billen_Hirth_2005.md"
    output_path = tmp_path / "index.jsonl"
    summary_path.write_text(
        make_summary("Billen and Hirth", ["A result."]),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--input",
            str(summary_path),
            "--literature",
            str(LITERATURE_FIXTURE_DIR),
            "--output",
            str(output_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert json.loads(output_path.read_text(encoding="utf-8")) == {
        "title": "Billen and Hirth",
        "author": "Magali I. Billen, Greg Hirth",
        "source": "Billen_Hirth_2005.md",
        "pdf": "Billen_Hirth_2005.pdf",
        "takeaways": ["A result."],
    }
