#!/usr/bin/env python3
"""
Extract structured information from literature summary files.

This module parses Markdown summaries generated from scientific literature.
It validates that a summary follows the expected Markdown structure and
extracts selected information for use in a compact, searchable literature
index.

Currently supported:
    - Validation of the key-takeaway structure.
    - Extraction of paper titles and takeaway summaries.
    - Matching summaries to their source PDF files.
    - Creation of a JSON Lines literature index.

Usage:
    python scripts/extract_summary.py \
        --input <summary-file-or-directory> \
        --literature <pdf-directory> \
        --output <output.jsonl>

Example:
    python scripts/extract_summary.py \
        --input tests/fixtures/markdown_summary \
        --literature tests/fixtures/literature \
        --output .dtemp/literature.jsonl
"""

import argparse
import json
import re
from pathlib import Path

if __package__:
    from scripts.build_index import extract_pdf_metadata, find_pdf_files
else:
    from build_index import extract_pdf_metadata, find_pdf_files


def extract_title(markdown_text: str) -> str:
    """Extract the single level-one paper title from a summary."""
    titles = re.findall(r"^#\s+(.+?)\s*$", markdown_text, flags=re.MULTILINE)

    if len(titles) != 1:
        raise ValueError(
            "Invalid summary format: expected exactly one level-one heading "
            "containing the paper title."
        )

    return titles[0].strip()


def find_markdown_files(input_path: Path) -> list[Path]:
    """Find Markdown summaries from a file or recursively from a directory."""
    if input_path.is_file():
        if input_path.suffix.lower() != ".md":
            raise ValueError(f"Input summary is not a Markdown file: {input_path}")
        return [input_path]

    if input_path.is_dir():
        return sorted(
            path
            for path in input_path.rglob("*")
            if path.is_file() and path.suffix.lower() == ".md"
        )

    raise ValueError(f"Input summary path does not exist: {input_path}")


def _extract_front_matter(markdown_text: str) -> dict[str, str]:
    """Extract simple key-value fields from leading YAML front matter."""
    lines = markdown_text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    fields = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip("'\"")

    return {}


def match_pdf_file(summary_path: Path, pdf_files: list[Path]) -> Path:
    """Match a Markdown summary to exactly one source PDF."""
    markdown_text = summary_path.read_text(encoding="utf-8")
    front_matter = _extract_front_matter(markdown_text)
    declared_pdf = front_matter.get("pdf", "")

    if declared_pdf:
        normalized_pdf = declared_pdf.replace("\\", "/")
        candidates = [
            path
            for path in pdf_files
            if path.name == Path(normalized_pdf).name
            and path.as_posix().endswith(normalized_pdf)
        ]

        zotero_key = front_matter.get("zotero_key", "")
        if zotero_key:
            candidates = [
                path for path in candidates if path.parent.name == zotero_key
            ]
    else:
        candidates = [
            path for path in pdf_files if path.stem == summary_path.stem
        ]

        if not candidates:
            base_stem = re.sub(r"_\d+$", "", summary_path.stem)
            candidates = [path for path in pdf_files if path.stem == base_stem]

    if not candidates:
        raise ValueError(f"No PDF match found for summary: {summary_path}")

    if len(candidates) > 1:
        matches = ", ".join(str(path) for path in candidates)
        raise ValueError(
            f"Ambiguous PDF match for summary {summary_path}: {matches}"
        )

    return candidates[0]


def build_jsonl_index(
    summary_input: Path,
    literature_directory: Path,
    output_path: Path,
) -> list[dict]:
    """Build a JSON Lines index from Markdown summaries and source PDFs."""
    summary_files = find_markdown_files(summary_input)
    pdf_files = find_pdf_files(literature_directory)
    summary_root = summary_input if summary_input.is_dir() else summary_input.parent

    records = []
    for summary_file in summary_files:
        markdown_text = summary_file.read_text(encoding="utf-8")
        pdf_file = match_pdf_file(summary_file, pdf_files)

        # Opening the PDF verifies that the indexed source remains accessible.
        extract_pdf_metadata(pdf_file)

        records.append(
            {
                "title": extract_title(markdown_text),
                "source": summary_file.relative_to(summary_root).as_posix(),
                "pdf": pdf_file.relative_to(literature_directory).as_posix(),
                "takeaways": extract_takeaways(markdown_text),
            }
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as output_file:
        for record in records:
            output_file.write(json.dumps(record, ensure_ascii=False) + "\n")

    return records


def validate_summary_format(markdown_text: str) -> None:
    """Validate the required structure of a literature summary."""

    if "## Key takeaways" not in markdown_text:
        raise ValueError(
            "Invalid summary format: missing '## Key takeaways' section."
        )

    if "## Figure summaries" not in markdown_text:
        raise ValueError(
            "Invalid summary format: missing '## Figure summaries' section."
        )

    key_takeaways_text = markdown_text.split(
        "## Key takeaways", 1
    )[1].split(
        "## Figure summaries", 1
    )[0]

    takeaway_headings = re.findall(
        r"^### Takeaway (\d+)\s*$",
        key_takeaways_text,
        flags=re.MULTILINE,
    )

    if not takeaway_headings:
        raise ValueError(
            "Invalid summary format: no takeaways found."
        )

    expected_numbers = [
        str(i) for i in range(1, len(takeaway_headings) + 1)
    ]

    if takeaway_headings != expected_numbers:
        raise ValueError(
            "Invalid summary format: takeaways must be numbered "
            "sequentially starting from 1."
        )

    takeaway_sections = re.split(
        r"^### Takeaway \d+\s*$",
        key_takeaways_text,
        flags=re.MULTILINE,
    )[1:]

    for number, section in enumerate(takeaway_sections, start=1):
        summary_matches = re.findall(
            r"^\*\*Summary:\*\*\s+(.+)$",
            section,
            flags=re.MULTILINE,
        )

        if len(summary_matches) != 1:
            raise ValueError(
                f"Invalid summary format: Takeaway {number} must contain "
                "exactly one '**Summary:**' field."
            )


def extract_takeaways(markdown_text: str) -> list[str]:
    """Extract takeaway summaries from a literature summary."""

    validate_summary_format(markdown_text)

    key_takeaways_text = markdown_text.split(
        "## Key takeaways", 1
    )[1].split(
        "## Figure summaries", 1
    )[0]

    takeaway_sections = re.split(
        r"^### Takeaway \d+\s*$",
        key_takeaways_text,
        flags=re.MULTILINE,
    )[1:]

    takeaways = []

    for section in takeaway_sections:
        match = re.search(
            r"^\*\*Summary:\*\*\s+(.+)$",
            section,
            flags=re.MULTILINE,
        )
        takeaways.append(match.group(1).strip())

    return takeaways


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Extract information from a literature summary."
    )

    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to a summary Markdown file or directory of summaries.",
    )

    parser.add_argument(
        "--literature",
        type=Path,
        required=True,
        help="Directory containing the original PDF literature.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Path to the output JSON Lines index.",
    )

    return parser.parse_args()


def main() -> None:
    """Build a JSON Lines index from literature summaries."""
    args = parse_arguments()
    build_jsonl_index(args.input, args.literature, args.output)


if __name__ == "__main__":
    main()
