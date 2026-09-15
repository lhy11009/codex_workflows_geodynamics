# Literature Q&A Development Instructions

## Purpose

This project develops a local literature retrieval system for scientific PDF
collections.

The long-term goal is to allow questions to be answered using only evidence
contained in a user-provided literature corpus.

Development must proceed incrementally. Do not implement later indexing,
retrieval, or question-answering features unless explicitly requested.

## Source literature

Original PDF files are source data.

Do not modify, rename, move, or delete PDF files.

Generated indexes and databases are disposable derived data and must be
rebuildable from the original PDFs.

## Python environment

Use the python environment literature-qa to run python scripts and tests.

First check this environment exists.


## Current development scope

The current development target is:

    scripts/build_index.py

At the current stage, `build_index.py` is responsible only for:

1. accepting an input literature directory;
2. accepting an output index path;
3. validating the input literature directory;
4. recursively discovering PDF files in the input directory; and
5. reporting the discovered PDF files.

Do not implement PDF text extraction, metadata extraction, database creation,
search, embeddings, or question answering unless explicitly requested.

## Testing

Tests for `build_index.py` belong in:

    tests/test_build_index.py

Use the small literature collection under:

    tests/fixtures/literature/

for testing during development. Do not use the full literature collection unless explicitly requested.

Before running tests, activate the project's Conda environment:

    conda activate literature-qa

Run the tests from the root directory of this project using:

    python -m pytest tests/test_build_index.py -v

The testing workflow is:

1. Activate the `literature-qa` Conda environment.
2. Run the relevant pytest tests.
3. If a test fails, inspect the failure and provide suggestions for how the implementation could be modified to address it.