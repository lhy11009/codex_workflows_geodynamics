"""Integration test for indexing real Markdown and PDF fixtures."""

import json
from pathlib import Path

from scripts.extract_summary import build_jsonl_index


PROJECT_DIRECTORY = Path(__file__).parents[1]
SUMMARY_DIRECTORY = Path(__file__).parent / "fixtures" / "markdown_summary"
LITERATURE_DIRECTORY = Path(__file__).parent / "fixtures" / "literature"
TEST_OUTPUT_DIRECTORY = PROJECT_DIRECTORY / ".test"
INDEX_PATH = TEST_OUTPUT_DIRECTORY / "literature.jsonl"
UNMATCHED_PATH = TEST_OUTPUT_DIRECTORY / "unmatched.json"


def test_build_fixture_directories_jsonl_index():
    """Index complete fixture directories and report unmatched inputs."""
    build_jsonl_index(
        SUMMARY_DIRECTORY,
        LITERATURE_DIRECTORY,
        INDEX_PATH,
        unmatched_output_path=UNMATCHED_PATH,
    )

    records = [
        json.loads(line)
        for line in INDEX_PATH.read_text(encoding="utf-8").splitlines()
    ]

    assert [record["source"] for record in records] == [
        "Billen_Hirth_2005.md",
        "Hansen_2007.md",
    ]
    assert [record["pdf"] for record in records] == [
        "Billen_Hirth_2005.pdf",
        "Hansen_2007.pdf",
    ]
    assert [len(record["takeaways"]) for record in records] == [4, 5]
    assert records[0]["title"].startswith(
        "Newtonian versus non-Newtonian upper mantle viscosity"
    )
    assert records[1]["title"] == "Subduction origin on early Earth: A hypothesis"

    assert json.loads(UNMATCHED_PATH.read_text(encoding="utf-8")) == {
        "summaries_without_pdf": [
            "Clift04RG_ControlsTectAccretionSubductionErosion_1.md"
        ],
        "pdfs_without_summary": ["Hosoya_et_al_2005.pdf"],
    }
