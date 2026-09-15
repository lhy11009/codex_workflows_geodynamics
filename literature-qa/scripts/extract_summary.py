#!/usr/bin/env python3
"""
Extract structured information from literature summary files.

This module parses Markdown summaries generated from scientific literature.
It validates that a summary follows the expected Markdown structure and
extracts selected information for use in a compact, searchable literature
index.

Currently supported:
    - Validation of the key-takeaway structure.
    - Extraction of takeaway summaries.

Usage:
    python scripts/extract_summary.py \
        --input <summary-file> \
        --output <output-file>

Example:
    python scripts/extract_summary.py \
        --input tests/fixtures/markdown_summary/example.md \
        --output .dtemp/takeaways.md
"""

import re
import argparse
from pathlib import Path


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
        help="Path to the literature summary Markdown file.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Path to the output Markdown file.",
    )

    return parser.parse_args()


def main() -> None:
    """Extract takeaways from a literature summary."""
    args = parse_arguments()

    if not args.input.is_file():
        raise ValueError(
            f"Input Markdown file does not exist: {args.input}"
        )

    with args.input.open("r", encoding="utf-8") as file:
        markdown_text = file.read()

    validate_summary_format(markdown_text)
    takeaways = extract_takeaways(markdown_text)

    args.output.parent.mkdir(parents=True, exist_ok=True)

    with args.output.open("w", encoding="utf-8") as file:
        for i, takeaway in enumerate(takeaways, start=1):
            file.write(f"{i}. {takeaway}\n")


if __name__ == "__main__":
    main()