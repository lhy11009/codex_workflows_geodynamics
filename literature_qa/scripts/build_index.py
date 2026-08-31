#!/usr/bin/env python3

"""Build a local index from a collection of PDF literature."""

import argparse
import pymupdf
from pathlib import Path


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Build a local index from a directory of PDF literature."
    )

    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Directory containing the PDF literature.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Path to the output literature index.",
    )

    return parser.parse_args()


def find_pdf_files(input_directory: Path) -> list[Path]:
    """Find all PDF files recursively under the input directory."""
    if not input_directory.is_dir():
        raise ValueError(
            f"Input literature directory does not exist: {input_directory}"
        )

    return sorted(input_directory.rglob("*.pdf"))


def extract_pdf_metadata(pdf_path: Path) -> dict:
    """Extract metadata from a PDF file."""
    with pymupdf.open(pdf_path) as document:
        metadata = document.metadata

        return {
            "filename": pdf_path.name,
            "path": pdf_path,
            "title": metadata.get("title", ""),
            "author": metadata.get("author", ""),
            "subject": metadata.get("subject", ""),
            "keywords": metadata.get("keywords", ""),
            "page_count": document.page_count,
        }


def main() -> None:
    """Build the literature index."""
    args = parse_arguments()

    pdf_files = find_pdf_files(args.input)

    print(f"Literature directory: {args.input}")
    print(f"Output index: {args.output}")
    print(f"Number of PDF files: {len(pdf_files)}")

    for pdf_file in pdf_files:
        metadata = extract_pdf_metadata(pdf_file)

        print()
        print(f"File: {metadata['filename']}")
        print(f"Title: {metadata['title']}")
        print(f"Author: {metadata['author']}")
        print(f"Subject: {metadata['subject']}")
        print(f"Keywords: {metadata['keywords']}")
        print(f"Pages: {metadata['page_count']}")


if __name__ == "__main__":
    main()