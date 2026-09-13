# Review Literature

## Purpose

Review a scientific paper using both the original PDF and my existing
Markdown summary.

The Markdown file contains my own notes and interpretation of the paper.
Treat these notes as the starting point for the review.

The PDF is the authoritative source and should be used to verify the notes,
identify missing information, and provide additional context.

## Inputs

For each paper, there should be:

- The original paper as a PDF file.
- My existing summary as a Markdown (`.md`) file.

The PDF and Markdown file should correspond to the same paper.

## Instructions

1. Do not modify, overwrite, rename, move, or delete my existing Markdown
   summary file. Treat it as read-only.

2. Read the Markdown summary first.

3. Check that the Markdown summary contains all of the following sections:
   - `Key takeaways`
   - `Figure summaries`
   - `Forward summary`

   If any of these sections are missing, report which sections are missing
   and stop the review.

4. Read the corresponding PDF.

5. Compare the Markdown summary with the PDF only to verify that they refer
   to the same literature. Do not evaluate the accuracy, completeness, or
   quality of the summary at this step.

   If they do not refer to the same literature, report the mismatch and stop
   the review.

## Review Format

Create a separate review copy of the Markdown summary before adding any
review content.

Use the following file naming convention:

- Original summary: `<paper>.md`
- Review copy: `<paper>.review.md`

Copy the complete contents of the original Markdown summary into the review
copy. Do not modify the original Markdown summary.

Perform all subsequent review work only in the review copy.

Add review comments directly below the corresponding content in the review
copy so that the review can be read alongside my existing notes.

Use Markdown blockquotes for review comments. For example:

> **REVIEW**
> Review comments go here.

Preserve the original structure, headings, text, and ordering from the
Markdown summary. Do not rewrite or reorganize my original content in the
review copy.

With every item, use review labels only to identify contents that has a problem or requires
attention. If the existing item is accurate and does not require attention according to the rules of review, 
do not add a review label or comment.

When inspecting an item, first inspect the original PDF contents that are related, do not rely entired on the markdown file.
Try to be critical.

When a review comment applies to an item, place the comment below that item.

When a review comment applies to an entire section, place the comment at the
end of that section.

When adding a review, add a page and line number inside the PDF, that this review mostly related to.

## Rules of Review

### Reviewing `Key takeaways`

Review the existing content in the `Key takeaways` section against the PDF.

For the `Result` in each takeaway, check that the stated results are well
supported by the paper, with particular attention to whether they are supported
by the figures referenced or presented in the paper.

Use the following review labels when a problem is identified:

- `REVIEW — Ambiguous figure`: Use when the stated result may be supported by
  the figure, but the figure does not clearly or uniquely support the
  interpretation given in the takeaway.

- `REVIEW — Problematic result`: Use when the stated result is not supported
  by the paper, conflicts with the figure or other evidence, contains an
  incorrect quantitative statement, or materially misrepresents the result.

For the `Discussion` in each takeaway, when the discussion is derived from the
reported results:

1. Check whether the reasoning from the results to the discussion is logically
   supported.

   - `REVIEW — Logic needs clarification`: Use when the reasoning is plausible,
     but the connection between the results and the discussion is unclear,
     incomplete, or requires additional justification.

   - `REVIEW — Logic problem`: Use when the discussion does not logically
     follow from the results or makes a conclusion that the presented evidence
     cannot support.

2. Check whether the reasoning depends on assumptions that are not explicitly
   stated in the takeaway.

   - `REVIEW — Assumption needs clarification`: Use when the reasoning depends
     on an implicit assumption that is reasonable but should be stated or
     clarified.

   - `REVIEW — Problematic assumption`: Use when the reasoning depends on an
     assumption that is unsupported, questionable, or inconsistent with the
     evidence presented in the paper.

Review the `Background` in each takeaway only after reviewing the `Result` and
`Discussion`.

Check whether information in the `Background` provides necessary context or
support for the `Result` and `Discussion`.

- `REVIEW — Missing background link`: Use when relevant information is present
  in the `Background`, but an important connection between that information and
  the `Result` or `Discussion` is missing or unclear.

- `REVIEW — Background conflict`: Use when information in the `Background`
  conflicts with the `Result`, `Discussion`, or the interpretation developed
  in the takeaway.

### Reviewing `Figure summaries`

For each figure, check whether the figure summary matches the actual content
shown in the figure and its caption.

For figures containing multiple subfigures or panels, check each subfigure
individually and verify that its summary matches the corresponding subfigure
and the description provided in the figure caption.

- `REVIEW — Figure caption problem`: Use when a figure or subfigure summary
  does not accurately match the content shown in the figure or the description
  provided in the figure caption.

For each figure, check that the figure is referred to at least once in the main
text of the PDF.

- `REVIEW — Figure not referenced`: Use when a figure is not referred to
  anywhere in the main text of the PDF.

For each reference to the figure in the main text, check whether the local text
surrounding the reference is consistent with the content shown in the figure.

- `REVIEW — Figure reference problem`: Use when the local text associated with
  a figure reference does not accurately match, is not supported by, or
  conflicts with the content shown in the figure.

For each reference to the figure in the main text, also check whether the
interpretation drawn from the figure is reasonable and adequately supported by
what the figure shows.

- `REVIEW — Figure interpretation problem`: Use when the figure itself is
  consistent with the local text, but the interpretation or conclusion drawn
  from the figure is not adequately supported, overstates what the figure
  demonstrates, or requires additional assumptions that are not justified.

After reviewing all individual figures, review the `Figure summaries` section
as a whole against the `Key takeaways` section.

Check whether additional figures from the PDF contain results that would
provide important visual evidence or substantially better support for points
made in the `Key takeaways` section but are not currently included in the
`Figure summaries`.

- `REVIEW — Additional figure recommended`: Use when an additional figure from
  the PDF would provide important evidence or substantially strengthen the
  support for a specific point in the `Key takeaways` section. Identify the
  recommended figure and the specific takeaway or statement it would support.

Do not recommend additional figures solely for completeness. Add this review
label only when the additional figure would materially improve the support for
a point made in the `Key takeaways`.

Do not add review labels when the corresponding content passes the checks
above.