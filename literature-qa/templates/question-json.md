# Literature Selection from Summaries Workflow

## Purpose

Use a collection of structured scientific-paper summaries to identify the papers that are most relevant to a research question.

This workflow is primarily a literature-selection workflow rather than a literature-question-answering workflow.

The summaries serve as a retrieval and filtering layer. The original PDF papers are not read during this workflow.

The workflow should:

* analyze the user's research question,
* inspect the summarized evidence for all available papers,
* identify evidence relevant to the question,
* select a user-specified number of the most relevant papers,
* explain why each selected paper is relevant.

The selected papers may subsequently be passed to a PDF-based literature workflow for detailed analysis of the original papers.

## Default Inputs

Read `<workspace-root>/.local/LITERATURE_PROJECTS.md` to locate the reference summaries file (JSONL), then read the summaries from that path.

The JSONL entry may contain information such as:

- Paper title
- Authors
- Publication year
- Key takeaways
- Methods
- Figure summaries

Use only the information available in each entry.
Do not assume that a field exists if it is not present.

## Inputs

The user provides:

1. A research question.
2. The number of papers to select, excluding any project default references.
3. An optional project name.


## Workflow

### 1. Load and validate the summary collection

Read the provided JSON file.

Identify all papers represented in the file.

For each paper, determine what summarized information is available.

Verify that the JSON can be read and contains sufficient information to perform literature selection.

If the JSON cannot be read or does not contain recognizable paper summaries, stop and report the issue.

Do not read the original PDF papers during this workflow.

### 2. Optionally read the project description

If the user specifies a project name, read its description in `<workspace-root>/.local/LITERATURE_PROJECTS.md`.

Identify the project's default references and include them in addition to the requested number of references.
For example, if the user requests 5 references and the project has 3 default references, provide 8 references in total: list the 5 newly found references first, followed by the 3 default references.

Avoid duplicates between the two lists.
If a default reference is also found during the search, retain it in the default-reference list and find another reference to satisfy the requested count.

### 3. Analyze the research question

Determine what information would make a paper relevant to the research question.

Identify the main concepts in the question, including where applicable:

* geological or physical processes,
* mechanisms,
* observations,
* model results,
* experimental results,
* methods,
* parameters,
* spatial or temporal relationships,
* interpretations,
* competing hypotheses,
* terminology and closely related concepts.

Do not rely only on exact keyword matches.

Consider conceptually related terminology and evidence that may address the question using different language.

### 4. Inspect all paper summaries

Consider every paper represented in the JSON before selecting the most relevant papers.

For each paper, inspect the summarized information for evidence related to the research question.

Relevant evidence may occur in:

* key takeaways,
* figure summaries,
* methods,

Do not determine relevance from the paper title alone.

Do not select papers solely because the title or abstract contains keywords from the research question.

### 5. Identify relevant summarized evidence

For each potentially relevant paper, identify the specific summarized evidence that connects the paper to the research question.

Distinguish between different kinds of relevance.

Give consideration to the following aspects to address the research question.

* background information directly related to the question,
* key takeaways addresses the question or part of it
* quantitative relationships relevant to the question,
* figures showing the relevant behavior.
* discussion in relation to the question


### 6. Compare relevance across papers

Compare the relevant evidence identified for all papers.

Do not create arbitrary numerical relevance scores.

Do not force papers into an artificial ranking when their relevance is effectively similar.

The purpose of the comparison is to identify the requested number of papers with the strongest and most useful summarized evidence.

### 7. Select the literature and output

Select the number of papers requested by the user.

Selection must be based on the evidence contained in the provided summaries.

For each selected paper, provide:

* name of the original pdf file,
* why the paper is relevant,
* the specific summarized evidence supporting its selection,

At the end, provide:

* names of all the selected pdf files, separated by ",", in one line.


## Evidence boundaries

This workflow operates on paper summaries rather than the original papers.

Therefore:

* Do not claim to have verified information against the original PDF.
* Do not invent information that is absent from the summaries.
* Do not invent figure numbers, page numbers, sections, results, or bibliographic information.
* Treat figure, page, and section references as information inherited from the summary.
* Do not assume that a summary contains every relevant result from the original paper.
* Absence of information from a summary does not necessarily mean that the original paper does not discuss it.

## Potential extensions

* This workflow could be extended to support writing. This typically requires writing based on the literature found. When including references, consult the citation file in the Literature project. Unless otherwise specified, write in LaTeX format and save the output to a new file in `<workspace>/.dtemp`.

## Rules

* Do not use any external literature 
* Do not determine relevance from titles alone.
* Do not rely only on keyword matching.
* Do not invent information missing from the summaries.
* Select the number of papers requested by the user.
* Explain the evidence supporting each selection.
* Preserve uncertainty when the available summaries do not provide enough information to determine relevance confidently.
* Never imply that the original PDF has been inspected when only its summary has been read.

# Test Literature Selection Workflow

## Test input

Follow the workflow defined in:

`literature-qa/templates/literature-question.md`

Use the literature summaries contained in:

`/home/lochy/Documents/papers/markdown_summary/summary.jsonl`

## Research question

**In general, what are the different types of continental rifting?**

## Number of literature to select

Select **10 relevant papers**.

## Test procedure

Follow the workflow in this file with the entries above.
