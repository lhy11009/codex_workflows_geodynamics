# Insert References into LaTeX from Provided PDFs

## Purpose

Insert scientifically appropriate LaTeX citations into user-provided text using
a small collection of PDFs. Trace background claims to the original works cited
in those papers, especially in their introductions and discussions. Preserve
the user's text unless they explicitly request rewriting.

## Inputs

- Scientific PDFs supplied as files or local paths.
- LaTeX text pasted into the conversation or supplied as a `.tex` file.
- Optional bibliography files, citation style, and output path.

Ask only for required inputs that cannot be located or inferred reliably.

## Outputs

- A cited LaTeX fragment or document at the requested path. If no path is
  specified, use `temp.tex` in the working directory for pasted text and
  `<input-stem>_cited.tex` next to a supplied `.tex` file.
- Brief LaTeX comments documenting citation provenance and unresolved issues.

Keep source PDFs, input TeX files, and existing bibliographies read-only. If
the output path is already occupied, use a numbered suffix such as `_1` or `_2`.

## Workflow

### 1. Identify sources and citation conventions

Verify each supplied PDF's title, authors, year, and version from the paper
itself. Distinguish preprints, accepted manuscripts, and published versions
when the difference matters to the claim.

Follow the requested citation style if provided. Otherwise, inspect the TeX
and use the project's existing commands and citation package. For a fragment
with no discernible convention, use `\parencite{key}` and report that it
requires `biblatex`. Preserve the existing preamble and leave fragments without
a preamble unless the user requests one. If a complete document lacks a usable
citation setup, flag the dependency and preserve the preamble.

Search the user-specified bibliography files first. If none are specified,
check the bibliographies declared by the TeX project, then use the defaults in
`<workspace-root>/.local/LITERATURE_PROJECTS.md`. 

Match entries by DOI when available or by title, authors, year, and version.
Reuse the exact key and verify that it resolves in the target bibliography.
For a standalone fragment, record which bibliography supplies the key. If a
key exists only in a fallback bibliography that the project does not load,
flag that integration step in a comment. If no matching key exists, leave the
claim uncited and record the missing reference in a comment with enough
bibliographic detail to identify it.

### 2. Read every supplied PDF

Read the abstract, introduction, discussion, and conclusions where present.
Consult methods, results, figures, and captions as needed to establish what
each source supports. If extraction obscures a relevant passage or citation,
inspect the page image. Flag any material that remains unreadable.

Pay particular attention to the citations attached to descriptions of earlier
methods and assumptions, research gaps, competing mechanisms, observational
tests, and numerical approaches. Check the reference-list entry for each
candidate. Select sources based on the supporting passage and its scope.

### 3. Match claims to evidence

Assess each sentence or independently supported clause. Distinguish background
claims, reported results, interpretations, research gaps, and proposed work.
For each claim that needs support, record the supplied PDF, section, printed
page or PDF page, and figure if relevant. Record the original work cited in
the passage, the specific claim the passage supports, any qualifications, and
whether you read the supporting passage in the original work.

Prefer original studies for historical methods, experiments, observations, and
hypotheses. Cite a supplied paper directly for its own results, synthesis, or
stated limitations. Use a small number of references with a clear connection
to the claim.

When the original work is available, check the relevant passage directly
before marking the citation as verified. If the original is unavailable, use
a traced citation only when the supplied paper clearly attributes the specific
claim to that work. Record the indirect provenance in a comment. If attribution is
ambiguous, flag the claim and leave it uncited. Keep source discovery within
the supplied PDFs and the works they cite unless the user requests a broader
search.

### 4. Check research-gap and novelty claims

Check phrases such as “most studies,” “no existing model,” or “only conceptual”
against all supplied papers. Distinguish a limitation demonstrated for an
individual approach from a claim about the field as a whole. Treat the supplied
PDFs as a bounded sample when assessing broad claims. For example, a model that
identifies conditions favorable for a mechanism supports a claim about those
conditions. Claims about nucleation, dynamic rupture, or a decisive hypothesis
test require additional evidence.

Preserve overstated wording and use a nearby comment to identify the evidence
gap and, where useful, suggest a minimal correction. Leave unsupported claims
uncited. Statements of planned work generally need no citation. Cite a
methodological precedent only where it supports the method actually described.

### 5. Insert citations and provenance comments

Preserve the wording, sentence order, headings, equations, notation, labels,
and existing citations. Replace empty parentheses only when they clearly mark
a citation placeholder. Otherwise, insert citations next to the supported
clause, normally before its final punctuation. Use separate citations for
clauses with different supporting sources when needed.

Use short LaTeX comments for provenance and unresolved issues. Place them on
their own lines where they preserve surrounding LaTeX syntax and spacing.

```latex
% Traced via SuppliedAuthor (2026), Introduction, PDF p. 5.
% Original study not independently inspected. Supports the kinetic approximation.
Earlier models used a blocking-temperature approximation
\parencite{example_kinetics_2012}.
```

### 6. Validate the output

- Confirm that every supplied PDF was considered and that each added citation
  supports the adjacent claim at the level of specificity used in the text.
- Verify that each added key resolves in the intended bibliography or has a
  documented bibliography dependency.
- Compare the result with the input. Removing only the additions, including
  insertion-related whitespace, and restoring replaced placeholders should
  recover the original text and LaTeX structure.
- Confirm that unresolved or overstated claims are flagged and that input
  files were preserved.

Use the text comparison and citation-key checks for validation. A standalone
PDF build is optional.

## Final response

Give the output path. Summarize material unresolved claims, missing
bibliography entries or dependencies, and citations traced through the supplied
PDFs whose originals were not inspected. Include the full cited text only if
requested.

## Example invocation

> Apply `literature-qa/templates/insert-references.md` to these five PDFs and
> this LaTeX text. Preserve all wording, use the references cited in the
> papers' introductions and discussions, and save the result to `temp.tex`.