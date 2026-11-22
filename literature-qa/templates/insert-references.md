# Insert References into LaTeX from Provided PDFs

## Purpose

Insert scientifically appropriate LaTeX citations into user-provided text using a collection of scientific PDFs.

Identify relevant supporting evidence in the provided papers, and trace background claims to the original studies cited in those papers, particularly in their introductions and discussions. Prefer citing the original studies when the claim is supported by earlier research, and cite the provided paper when referring to its own findings.

Preserve the user's original text unless rewriting is explicitly requested.

## Inputs

- Scientific PDFs provided as files or local paths.
- LaTeX text pasted into the conversation or provided in a `.tex` file.
- Optional bibliography files, citation style, and output path. Use the project defaults when these are not specified.

Ask for clarification only when required inputs cannot be located or reliably inferred from the available files or project context.

## Outputs

- A LaTeX fragment or document with scientifically appropriate citations inserted, saved to the requested path. If no path is specified:
  - For text pasted into the conversation, use `temp.tex` in the working directory.
  - For a supplied `.tex` file, use `<input-stem>_cited.tex` in the same directory as the input file.
- Brief LaTeX comments documenting citation provenance, supporting sources, and unresolved issues.

Keep all source PDFs, input `.tex` files, and existing bibliography files read-only. Never overwrite an existing output file. If the target path is already occupied, append a numerical suffix (`_1`, `_2`, etc.) to create a unique filename.


## Workflow

### 1. Identify sources and citation conventions

Verify that the specified PDFs exist and are accessible. For each PDF, verify its title, authors, publication year, and version using information from the paper itself.

Follow the user's requested citation style, if specified. Otherwise, inspect the existing LaTeX file to identify its citation conventions:

- If an existing citation convention is identifiable, follow it and reuse the established citation commands.
- If no identifiable citation convention exists, use `\parencite{key}` and note that it requires `biblatex`.
- If a complete LaTeX document lacks a working citation setup, report the missing dependency without modifying the preamble.

Identify the bibliography files in the following order:

1. Bibliography files explicitly specified by the user.
2. Bibliography files declared in the existing LaTeX project.
3. Default bibliography files listed in `<workspace-root>/.local/LITERATURE_PROJECTS.md`.

### 2. Read every supplied PDF

Read the abstract, introduction, discussion, and conclusions of each supplied PDF, where available. Consult the methods, results, figures, and captions as needed to understand the scientific claims and identify supporting evidence.

If text extraction is incomplete or unclear, inspect the corresponding PDF page directly. Flag any relevant content that remains unreadable.

Pay particular attention to:

- Background knowledge and previous studies cited in the introduction and discussion.
- Earlier methods, assumptions, and numerical or experimental approaches.
- Research gaps, competing hypotheses, and proposed mechanisms.
- Observational evidence and tests supporting or challenging scientific interpretations.
- Results and conclusions originating from the supplied paper itself.

For each potential citation:

- Identify the specific passage and scientific claim it supports.
- Check the references cited in that passage and locate their entries in the paper's reference list.
- Distinguish between findings originating from the supplied paper and background claims attributed to earlier studies.
- Prefer the original study for background claims and the supplied paper for its own findings.
- Select references based on how directly they support the intended claim, rather than citing papers solely because they discuss a related topic.

Do not assume that a cited reference supports a claim beyond what can be established from the supplied PDF. If the original reference is not available for direct verification, treat its support as indirect and document that limitation when relevant.

### 3. Insert citations and provenance comments

Preserve the original wording, sentence order, headings, equations, notation, labels, and existing citations. Do not rewrite or reorganize the text unless explicitly requested.

When inserting citations:

- Replace empty parentheses only when they clearly represent citation placeholders.
- Insert citations immediately after the supported clause, normally before its final punctuation.
- Use the citation commands and bibliography keys identified in Step 1.
- Avoid redundant citations when an existing citation already adequately supports the claim.

For unresolved references or uncertain citation keys:

- Insert a provisional citation key using the format `author_year` (e.g., `\parencite{smith_2020}`).
- Add a brief LaTeX comment near the corresponding sentence explaining the unresolved issue, such as a missing bibliography entry, uncertain citation key, or reference that could not be independently verified.
- Clearly distinguish provisional citation keys from verified bibliography keys.
- Do not modify existing bibliography files.

Example:

```latex
Earlier models used a blocking-temperature approximation
\parencite{smith_2020}. % Unresolved: Smith et al. (2020) 
```

### 4. Validate the output

- Confirm that every supplied PDF was examined and that each newly inserted citation supports the adjacent scientific claim at the level of specificity used in the text.
- Verify that each added citation key either:
  - Resolves to an existing entry in the intended bibliography; or
  - Uses a provisional `author_year` key with a nearby LaTeX comment explaining the unresolved reference or uncertain citation key.
- Compare the output against the original input. Confirm that only the citations are modified, check the original text is preserved. 
- Confirm that unsupported, uncertain, or overstated claims are explicitly flagged rather than silently modified.
- Verify that all source PDFs, original `.tex` files, and existing bibliography files remain unchanged.
- Confirm that the output follows the citation conventions identified in Step 1.


## Final response

- Provide the path to the generated LaTeX file.
- Briefly summarize any unresolved scientific claims, missing bibliography entries, provisional citation keys, or citation dependencies.

Keep the final response concise. Detailed citation provenance and unresolved issues should be documented in LaTeX comments within the output file.

## Example invocation

> Apply `literature-qa/templates/insert-references.md` to these the default referneces
> for the MOW project and this LaTeX text. Preserve all wording, use the references cited in the
> papers' introductions and discussions, and save the result to `temp.tex`.

'''latex
\par Second, deep earthquakes are unlikely to occur through the same brittle failure mechanisms as shallow earthquakes due to the high confining pressure in the MTZ.
Instead, proposed mechanisms include thermally induced transformational faulting (), shear-induced transformational faulting (\citealp{levitas2022resolving}, todo: more), and runaway shear heating processes.
Within this scope, metastable olivine has long been proposed to play a key role in deep earthquake generation, although the exact mechanism remains under debate.
Recently, () showed that high strain rates are associated with deep earthquakes in the MTZ.
In this context, the kinetic transformation of olivine in the subducti
'''