# LaTeX Manuscript Polishing Workflow

## Purpose

Use this workflow to compile and polish the English in a LaTeX manuscript while preserving its scientific meaning, approximate sentence lengths, citations, equations, figures, and LaTeX structure.

The expected input directory contains:

- one main `.tex` manuscript;
- one or more bibliography files;
- figures referenced by the manuscript; and
- any supplementary LaTeX inputs required for compilation.

## Required outputs

For a main file named `<name>.tex`, produce:

- `00/<name>.tex`: an exact, immutable copy of the original;
- `<name>_new.tex`: the polished manuscript;
- `<name>_new.pdf`: the compiled polished manuscript; and
- `<name>_changes.diff`: an inline, line-numbered record of every textual change.

Do not overwrite or edit the archived original.

## 1. Inspect the manuscript directory

List the files and identify the main TeX document, bibliography, figures, and included files.

Inspect the preamble to determine:

- the TeX engine;
- whether the bibliography uses `bibtex` or `biber`;
- required LaTeX packages and backends
- whether the document relies on relative paths.

Verify the required programs before editing. For a `biblatex` document using `backend=biber`, for example:


## 2. Test the original manuscript

Compile in a temporary build directory so diagnostic files do not alter the source directory.

Resolve fatal compilation errors before editing. Record nonfatal pre-existing warnings separately from errors introduced by the revision.

## 3. Archive the original

Create the archive directory and copy the original manuscript into it:

```bash
mkdir -p 00
cp -p <name>.tex 00/<name>.tex
cmp -s <name>.tex 00/<name>.tex
sha256sum <name>.tex 00/<name>.tex
```

The checksums must match. Copy the original to `<name>_new.tex` and perform all editing only in the `_new` file.

Do not modify, rename, or delete figures, bibliography files, or other source material. Keep the root copy of the original unless the user explicitly asks for it to be moved.

## 4. Polish the manuscript sentence by sentence

Review all author-written prose, including:

- abstract;
- main sections and subsections;
- figure and table captions;
- acknowledgements, data statements, and conclusions; and
- prose embedded in table notes.

Normally leave comments, equations, labels, citation keys, file paths, commands, and tabular numerical data unchanged.

For every sentence:

1. Preserve the scientific meaning and degree of certainty.
2. Preserve approximately the original sentence length unless grammar requires restructuring.
3. Correct grammar, spelling, punctuation, articles, prepositions, agreement, and tense.
4. Improve clarity and scholarly tone without adding new claims.
5. Preserve technical terminology and symbols.
6. Preserve all citations and keep them attached to the claims they support.
7. Preserve LaTeX commands, cross-references, labels, units, and mathematical notation.
8. Do not alter numerical values or scientific conclusions unless correcting an unmistakable typographical error.
9. Avoid changing text merely to impose a personal stylistic preference.
10. Do not combine or split sentences unnecessarily.


## 5. Generate an inline change record

Create a zero-context word diff between the archived original and revised source:

```bash
git diff --no-index \
  --word-diff=plain \
  --word-diff-regex='[^[:space:]]+' \
  --unified=0 \
  -- 00/<name>.tex <name>_new.tex \
  > <name>_changes.diff
```

`git diff --no-index` returns exit status `1` when differences exist; this is expected and is not a workflow failure.

The resulting markers mean:

- `[-deleted text-]`: text removed from the original;
- `{+added text+}`: text added to the revision.

Each `@@` hunk header records the original and revised line numbers. Keep zero lines of surrounding context so the record focuses on edited sentences rather than displaying separate complete before-and-after blocks.

Verify that the log is nonempty and count its edit hunks:

```bash
grep -c '^@@' <name>_changes.diff
```

## 6. Compile the revised manuscript

Compile `<name>_new.tex` through the complete bibliography cycle in a fresh temporary directory. Run the TeX engine enough times to resolve bibliography entries and cross-references.


## 7. Validate the deliverables

Confirm all of the following:

- the archived original matches the input checksum;
- the revised file has the `_new.tex` suffix;
- the revised PDF opens and has a plausible page count;
- no fatal LaTeX errors occurred;
- no citations or references remain unresolved;
- all figures are present;
- the change record contains every source edit;
- the change record uses inline deletion/addition markers; and
- each change hunk includes original and revised line numbers.


## 8. Final report

Report concise links or paths to:

- the archived original;
- the revised TeX source;
- the inline change record; and
- the compiled revised PDF.

Also report:

- the number of change hunks;
- the PDF page count;
- whether unresolved citations or references remain; and
- whether any source files other than the requested outputs were modified.

If compilation fails, retain the revised source and change record, report the first actionable error, and do not claim completion.
