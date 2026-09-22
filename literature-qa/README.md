## Batch literature summarization

The script:

    bash_scripts/summarize_batch.sh

uses Codex to summarize multiple PDF files using the workflow defined in:

    templates/summarize-literature.md

For each run, the script:

1. Finds PDF files recursively under the literature directory.
2. Skips PDFs that already have a corresponding Markdown summary in the output directory.
3. Selects the requested number of unsummarized papers.
4. Runs Codex once for each selected paper.
5. Writes the generated Markdown summaries to the specified output directory.
6. Records batch information in `summarize_batch.log` in the output directory.

### Usage

Run:

    ./bash_scripts/summarize_batch.sh [options] <literature-dir> <output-dir> <number-of-papers>

For example:

    ./bash_scripts/summarize_batch.sh \
        /home/lochy/Documents/papers \
        /home/lochy/Documents/papers/markdown_summary \
        10

The literature and output directories may be absolute paths or paths relative to the `literature-qa` directory.

Use:

    -n
    --newest-first

to process newer PDFs first. If PDF creation time is unavailable, modification time is used instead.

For example:

    ./bash_scripts/summarize_batch.sh \
        /home/lochy/Documents/papers \
        /home/lochy/Documents/papers/markdown_summary \
        10 \
        -n

Use:

    -z
    --zotero-storage

when the literature directory is a Zotero storage directory whose immediate
subdirectories are item keys. Summaries remain directly under the output
directory. Each generated summary starts with Zotero metadata such as:

    ---
    zotero_key: ABCD1234
    doi: 10.1016/j.tecto.2020.xxxxx
    pdf: my_old_filename.pdf
    ---

The item key is taken from the PDF's parent directory and the PDF filename is
preserved in the metadata. Codex reads the DOI from the PDF; the `doi` value is
left empty if it cannot be verified. Existing summaries with the same
`zotero_key` are skipped.

For example:

    ./bash_scripts/summarize_batch.sh \
        /home/lochy/Zotero/storage \
        /home/lochy/Documents/papers/markdown_summary \
        10 \
        --zotero-storage \
        --newest-first

Use:

    ./bash_scripts/summarize_batch.sh --help

to display the command-line options.

### Scheduling with cron

The batch script can be run periodically with `cron`. This is useful for processing a large literature collection gradually rather than consuming a large amount of Codex usage in one session.

First verify that the command runs successfully from the terminal.

Then edit the user crontab:

    crontab -e

For example, the following configuration runs a batch of 10 papers at 00:00, 05:00, 10:00, 15:00, and 20:00 each day:

    SHELL=/bin/bash
    PATH=/usr/local/bin:/usr/bin:/bin

    0 */5 * * * /home/lochy/Desktop/codex_workflows_geodynamics/literature-qa/bash_scripts/summarize_batch.sh /home/lochy/Documents/papers /home/lochy/Documents/papers/markdown_summary 10 -n >> /home/lochy/Documents/papers/markdown_summary/cron.log 2>&1

The script writes its own batch log to:

    <output-dir>/summarize_batch.log

The cron entry additionally redirects the complete stdout and stderr of the scheduled execution to:

    <output-dir>/cron.log

This is useful for diagnosing failures that occur before or outside the script's normal logging.

Check the installed cron configuration with:

    crontab -l

Monitor cron output with:

    tail -f /home/lochy/Documents/papers/markdown_summary/cron.log

Note that `0 */5 * * *` means execution at hours divisible by five rather than a strictly continuous five-hour interval. In particular, the daily sequence is:

    00:00
    05:00
    10:00
    15:00
    20:00

followed by 00:00 the next day.

## Build a summary index

Use `scripts/extract_summary.py` to assemble generated Markdown summaries and
their original PDF files into a JSON Lines index:

```bash
python scripts/extract_summary.py \
    --input /path/to/markdown_summary \
    --literature /path/to/papers \
    --output /path/to/literature.jsonl \
    --report-output /path/to/match_report.json
```

The input can be one Markdown summary or a directory, which is searched
recursively. Each output line contains the paper title, the author metadata
from the PDF, the relative Markdown and PDF paths, and the extracted
key-takeaway summaries. When the Markdown contains a `## Methods` section, the
output also contains the text from each `**Method:**` field:

```json
{"title": "Paper A", "author": "Author One, Author Two", "source": "paper_a.md", "pdf": "paper_a.pdf", "takeaways": ["Result 1", "Result 2"], "methods": ["Thin-viscous-shell scaling analysis"]}
```

The Methods section is optional. Records produced from summaries without it do
not contain a `methods` field.

When a summary has YAML front matter, its `pdf` field identifies the original
PDF. Otherwise, the script matches the Markdown and PDF filename stems. A
terminal summary suffix such as `_1` or `_2` is ignored only when an exact
stem match is unavailable. Summaries without PDFs are omitted from the JSONL
index, while PDFs without summaries are also identified. Both categories are
written to `match_report.json` beside the index by default, or to the path
given with `--report-output`. When multiple PDFs match one summary, the first
PDF in the sorted literature-file list is indexed and the selected PDF and all
candidates are recorded under `ambiguous_pdf_matches` in the report.
