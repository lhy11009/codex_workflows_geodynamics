# Literature Question Workflow

## Purpose

Use a small collection of scientific papers to answer a research question.

## Inputs

The user provides:

1. A set of PDF papers.
2. A research question about those papers.

All provided PDFs must be considered when answering the question.
The user may provide the PDFs first. In that case, first identify and read the PDFs, then wait for questions.

## Workflow

### 1. Identify the papers

List the provided PDF files.

For each PDF:

* identify the paper title,
* identify the authors,
* identify the publication year,
* verify that the file is a scientific paper relevant to the requested analysis.

Do not infer bibliographic information from the filename when it can be obtained from the paper itself.

### 2. Read the papers

Read each provided PDF at minimum, inspect:

* Abstract
* Introduction
* Methods
* Results
* Discussion
* Conclusions
* Relevant figures and figure captions

Do not answer the question based only on abstracts.

When the question concerns a specific result, mechanism, method, or interpretation, inspect the relevant sections and figures in detail.

### 3. Analyze the question

Determine what information is required to answer the user's question.

For each paper, identify:

* information directly relevant to the question,
* relevant results,
* relevant figures,
* interpretations made by the authors,
* limitations or qualifications relevant to the answer.

Distinguish between:

* results reported by the paper,
* interpretations made by the paper's authors,
* conclusions obtained by comparing multiple papers.

Do not attribute a conclusion to a paper unless that paper actually supports it.

### 4. Compare the papers

When multiple papers address the same issue, compare them.

Identify:

* agreements,
* differences,
* potentially conflicting results,
* differences in methods or model assumptions that may explain different conclusions.

Do not force agreement between papers.

If the available papers do not provide enough evidence to answer part of the question, state that explicitly.

### 5. Answer the question

Answer the user's research question directly.

Base the answer mainly on information supported by the provided papers.

General knowledge may be added when needed to connect the logic, provide necessary context, or explain relationships between results from different papers.

Do not use general knowledge to replace evidence that should come from the provided papers.

#### Annotation of supporting material

For each statement, add the reference to its supporting material in parentheses `()` after the statement.

If a statement is supported by one of the provided papers, identify the supporting paper and include at least one of the following when available:

* relevant section,
* figure number,
* page number.

Prefer specific references such as:

`(Smith et al., 2020, Fig. 4)`

or:

`(Smith et al., 2020, Discussion, p. 12)`

If multiple papers support the same statement, include the relevant references together, separate them by `;`.

If a statement is based on general knowledge rather than the provided papers, explicitly mark it as:

`(GK)`

Clearly distinguish statements supported by the provided papers from statements added using general knowledge.



## Rules

* Read all provided PDFs before giving the final answer.
* Do not use external literature unless the user explicitly requests it.
* Do not invent citations, page numbers, figure numbers, or results.
* Do not rely only on abstracts.
* Prefer results and figures over broad statements in introductions.
* Separate reported results from author interpretation.
* Separate cross-paper synthesis from claims made by individual papers.
* Explicitly identify uncertainty or disagreement between papers.
* If the papers are insufficient to answer the question, explain what information is missing.


## Test PDF Workflow

### Test papers

Read and analyze the following five PDF files:

* `Ledeczi_etal_2026.pdf`
* `Perez-Gussinye_etal_2023_nree.pdf`
* `Raghuram_etal_2023_geology.pdf`
* `Mezri_etal_2024_epsl.pdf`
* `Yang_etal_2025_epsl.pdf`

From the folder
`/home/lochy/Documents/papers`

The question is:
* In general, what are the different types of continental rifting?

### Test procedure

1. Locate all five PDF files.
2. Verify that all five files exist and can be read. If not, stop and report the issue.
3. Read all five papers following the Literature Question Workflow above.