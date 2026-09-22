"""Tests for bash_scripts/summarize_batch.sh."""

import os
import subprocess
import time
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).parents[1]
SCRIPT = PROJECT_ROOT / "bash_scripts" / "summarize_batch.sh"


def create_mock_codex(mock_bin_dir: Path, log_file: Path) -> None:
    """Create a mock Codex executable that records one entry per invocation."""
    codex_path = mock_bin_dir / "codex"

    codex_path.write_text(
        f"""#!/usr/bin/env bash
printf '%s\\n' "$*" | tr '\\n' ' ' >> "{log_file}"
printf '\\n' >> "{log_file}"
""",
        encoding="utf-8",
    )

    codex_path.chmod(0o755)


@pytest.mark.parametrize("arguments", [["-h"], ["--help"], ["unused", "--help"]])
def test_help_option(arguments):
    """Show usage and exit successfully without requiring other arguments."""
    result = subprocess.run(
        [SCRIPT, *arguments],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Usage:" in result.stdout
    assert "<literature-dir> <output-dir> <number-of-papers>" in result.stdout
    assert "--exclude-subdirectory" in result.stdout
    assert "-z, --zotero-storage" in result.stdout
    assert result.stderr == ""


def test_unknown_option_is_rejected():
    """Report unsupported options instead of treating them as paths."""
    result = subprocess.run(
        [SCRIPT, "--unknown"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "Error: unknown option: --unknown" in result.stderr


@pytest.mark.parametrize(
    ("zotero_option", "option_position"),
    [
        ("--zotero-storage", 0),
        ("--zotero-storage", 1),
        ("-z", 2),
        ("--zotero-storage", 3),
    ],
)
def test_zotero_storage_adds_front_matter_instructions(
    tmp_path, zotero_option, option_position
):
    """Pass Zotero metadata and the flat output directory to Codex."""
    literature_dir = tmp_path / "storage"
    output_dir = tmp_path / "output"
    mock_bin_dir = tmp_path / "bin"
    log_file = tmp_path / "codex.log"
    zotero_item_dir = literature_dir / "ABCD1234"

    zotero_item_dir.mkdir(parents=True)
    output_dir.mkdir()
    mock_bin_dir.mkdir()
    (zotero_item_dir / "my_old_filename.pdf").touch()

    create_mock_codex(mock_bin_dir, log_file)
    env = os.environ.copy()
    env["PATH"] = f"{mock_bin_dir}:{env['PATH']}"

    arguments = [str(literature_dir), str(output_dir), "1"]
    arguments.insert(option_position, zotero_option)

    result = subprocess.run(
        [SCRIPT, *arguments],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    call = log_file.read_text(encoding="utf-8")
    assert f"Write the resulting Markdown summary directly under:  {output_dir}" in call
    assert "zotero_key: ABCD1234" in call
    assert "doi: <DOI from the PDF>" in call
    assert "pdf: my_old_filename.pdf" in call
    assert "If the DOI cannot be verified, use an empty value" in call
    assert not (output_dir / "ABCD1234").exists()


def test_zotero_storage_skips_existing_zotero_key(tmp_path):
    """Skip an item whose Zotero key is already present in a flat summary folder."""
    literature_dir = tmp_path / "storage"
    output_dir = tmp_path / "output"
    mock_bin_dir = tmp_path / "bin"
    log_file = tmp_path / "codex.log"

    (literature_dir / "ABCD1234").mkdir(parents=True)
    (literature_dir / "WXYZ5678").mkdir()
    output_dir.mkdir()
    mock_bin_dir.mkdir()
    (literature_dir / "ABCD1234" / "same_name.pdf").touch()
    (literature_dir / "WXYZ5678" / "same_name.pdf").touch()
    (output_dir / "existing_summary.md").write_text(
        "---\nzotero_key: ABCD1234\ndoi: \npdf: same_name.pdf\n---\n",
        encoding="utf-8",
    )

    create_mock_codex(mock_bin_dir, log_file)
    env = os.environ.copy()
    env["PATH"] = f"{mock_bin_dir}:{env['PATH']}"

    result = subprocess.run(
        [
            SCRIPT,
            "--zotero-storage",
            str(literature_dir),
            str(output_dir),
            "2",
        ],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    calls = log_file.read_text(encoding="utf-8").splitlines()
    assert len(calls) == 1
    assert "WXYZ5678" in calls[0]
    assert "ABCD1234" not in calls[0]
    assert "Skipping existing Zotero item: same_name.pdf (ABCD1234)" in result.stdout


@pytest.mark.parametrize(
    ("newest_option", "option_position"),
    [
        ("--newest-first", 0),
        ("--newest-first", 1),
        ("-n", 2),
        ("--newest-first", 3),
    ],
)
def test_newest_first_orders_pdfs_by_creation_time(
    tmp_path, newest_option, option_position
):
    """Select a newer PDF before an alphabetically earlier, older PDF."""
    literature_dir = tmp_path / "literature"
    output_dir = tmp_path / "output"
    mock_bin_dir = tmp_path / "bin"
    log_file = tmp_path / "codex.log"

    literature_dir.mkdir()
    output_dir.mkdir()
    mock_bin_dir.mkdir()

    (literature_dir / "z_older.pdf").touch()
    time.sleep(0.02)
    (literature_dir / "a_newer.pdf").touch()

    create_mock_codex(mock_bin_dir, log_file)
    env = os.environ.copy()
    env["PATH"] = f"{mock_bin_dir}:{env['PATH']}"

    arguments = [str(literature_dir), str(output_dir), "1"]
    arguments.insert(option_position, newest_option)

    result = subprocess.run(
        [SCRIPT, *arguments],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    calls = log_file.read_text(encoding="utf-8").splitlines()
    assert len(calls) == 1
    assert "a_newer.pdf" in calls[0]


def test_exclude_subdirectory_skips_pdfs_by_exact_directory_name(tmp_path):
    """Skip PDFs below each named literature subdirectory."""
    literature_dir = tmp_path / "literature"
    output_dir = tmp_path / "output"
    mock_bin_dir = tmp_path / "bin"
    log_file = tmp_path / "codex.log"

    (literature_dir / "included").mkdir(parents=True)
    (literature_dir / "archive").mkdir()
    (literature_dir / "topic" / "private").mkdir(parents=True)
    (literature_dir / "archive-copy").mkdir()
    output_dir.mkdir()
    mock_bin_dir.mkdir()

    (literature_dir / "included" / "included.pdf").touch()
    (literature_dir / "archive" / "archived.pdf").touch()
    (literature_dir / "topic" / "private" / "private.pdf").touch()
    (literature_dir / "archive-copy" / "similar_name.pdf").touch()

    create_mock_codex(mock_bin_dir, log_file)
    env = os.environ.copy()
    env["PATH"] = f"{mock_bin_dir}:{env['PATH']}"

    result = subprocess.run(
        [
            SCRIPT,
            "--exclude-subdirectory",
            "archive",
            str(literature_dir),
            "--exclude-subdirectory",
            "private",
            str(output_dir),
            "4",
        ],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    calls = log_file.read_text(encoding="utf-8")
    assert "included.pdf" in calls
    assert "similar_name.pdf" in calls
    assert "archived.pdf" not in calls
    assert "private.pdf" not in calls
    assert "PDF files discovered: 2" in result.stdout
    assert (
        "Skipping excluded subdirectory PDF: archived.pdf (archive)"
        in result.stdout
    )
    assert (
        "Skipping excluded subdirectory PDF: private.pdf (private)"
        in result.stdout
    )


def test_batch_size_and_skip_existing(tmp_path):
    """Test batch size and skipping papers with existing summaries."""
    literature_dir = tmp_path / "literature"
    output_dir = tmp_path / "output"
    mock_bin_dir = tmp_path / "bin"
    log_file = tmp_path / "codex.log"

    literature_dir.mkdir()
    output_dir.mkdir()
    mock_bin_dir.mkdir()

    # Create four test PDFs.
    (literature_dir / "paper_1.pdf").touch()
    (literature_dir / "paper_2.pdf").touch()
    (literature_dir / "paper_3.pdf").touch()
    (literature_dir / "paper_4.pdf").touch()

    # paper_2 has already been summarized and should be skipped.
    (output_dir / "paper_2.md").touch()

    # Create a mock Codex executable so the test does not invoke
    # the real Codex CLI or consume quota.
    create_mock_codex(mock_bin_dir, log_file)

    # Put the mock Codex executable before the real Codex executable
    # on PATH.
    env = os.environ.copy()
    env["PATH"] = f"{mock_bin_dir}:{env['PATH']}"

    result = subprocess.run(
        [
            SCRIPT,
            str(literature_dir),
            str(output_dir),
            "2",
        ],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0

    selection_message = "PDF files selected for batch: 2"
    assert selection_message in result.stdout
    assert result.stdout.index(selection_message) < result.stdout.index("Starting Codex")

    calls = log_file.read_text(encoding="utf-8").splitlines()

    # Exactly two papers should be processed.
    assert len(calls) == 2

    # paper_1 should be processed first.
    assert "paper_1.pdf" in calls[0]

    # paper_2 should be skipped, so paper_3 should be processed next.
    assert "paper_3.pdf" in calls[1]

    all_calls = "\n".join(calls)

    # paper_2 should not be processed because its summary already exists.
    assert "paper_2.pdf" not in all_calls

    # paper_4 should not be processed because the batch limit
    # has already been reached.
    assert "paper_4.pdf" not in all_calls
