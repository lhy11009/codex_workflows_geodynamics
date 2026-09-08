# Summarize Literature Workflow

## Purpose

Use this workflow to read and summarize a single scientific paper provided by
the user.

The summary must be based only on information contained in the specified PDF.

## Input

The user must specify the PDF to summarize.

If the PDF cannot be identified unambiguously, stop and ask the user to
specify it.

## Source restrictions

Use only information contained in the specified PDF.

Do not use:

- web searches;
- external literature;
- general knowledge as supporting evidence; or
- information from other PDFs in the literature collection.

If the requested information is not provided by the paper, state that it is
not provided rather than filling the gap using outside knowledge.

## Workflow

1. Locate the specified PDF.

2. Read enough of the paper to understand its overall structure, motivation,
   methods, results, discussion, and conclusions.

3. Identify the main scientific claims and the PDF pages that support them.


## Output

Summary into a `<filename>.md` file under the foler `literature_qa/dtemp` 

If a file with the same name already exists, do not overwrite it. Append a numerical suffix `_1`, `_2`, etc. to create a new filename.

For example:

    <filename>.md
    <filename>_1.md
    <filename>_2.md

### Key takeaways

1. Provide 3--5 points summarizing the most important scientific contributions of the paper.

   For each takeaway, use subpoints to explain how the conclusion is developed and supported in the paper:

   - If it builds on background knowledge mentioned in the paper introduction, summarize the relevant background and include the cited references.
   - If it contains result of the current study, use the relevant figures and key results to explain how the conclusion is developed.
   - If it is related arguments made in the discussion, summarize the relevant arguments and include the cited references.

    These categories are not mutually exclusive. Apply all that are relevant to each takeaway, and, when possible, connect the background knowledge in the introduction, results and figures from the current study, and discussion arguments to show how they collectively support the takeaway.

2. Summarize the figure contents. For each figure, provide one sentence describing its main content.

3. Provide a forward summary.

   Organize the summary in the following order:

   - Start with the background knowledge and previous studies. Exclusively include all the background points identified in Section 1. For each point, provide one sentence explaining why it is important for understanding the main takeaways of the paper.

   - Then summarize the results of the current study, following the order in which the figures are presented. For each figure, start with the one-sentence summary provided in Section 2. Then incorporate the relevant points identified in Section 1 and explain how the figure supports or illustrates the key takeaways. If a figure is important for multiple takeaways, discuss each connection as a separate point.

   - Finally, summarize the arguments and interpretations developed in the discussion. Exclusively include all the discussion points identified in Section 1. For each point, explain how it relates to the background knowledge listed earlier and how the argument is developed or supported by the results and figures of the current study.

## Output format requirements

Follow the Markdown structure defined in this workflow exactly.

The generated Markdown files will be parsed programmatically. Therefore:

- Do not rename section headings.
- Do not change heading levels.
- Do not reorder required sections.
- Use the exact field labels specified by the template.
- Number takeaways and figures sequentially.
- Do not replace the specified structure with an alternative Markdown format.

Below is the specified structure:

```text
# <Paper title>

## Key takeaways

### Takeaway 1

**Summary:** <one-sentence summary of the takeaway>

- **Background:** <background information relevant to this takeaway, including references where applicable>
- **Result:** <results from this paper supporting the takeaway, including relevant figure numbers>
- **Discussion:** <arguments or interpretations from the discussion supporting the takeaway>

### Takeaway 2

**Summary:** <one-sentence summary of the takeaway>

- **Background:** <...>
- **Result:** <...>
- **Discussion:** <...>

## Figure summaries

### Figure 1

**Summary:** <one-sentence description of the figure>

### Figure 2

**Summary:** <one-sentence description of the figure>

## Forward summary

### Background and previous studies

<summary>

### Current study and results in figure order

#### Figure 1

<summary and connection to relevant takeaways>

#### Figure 2

<summary and connection to relevant takeaways>

### Discussion and interpretation

<summary>
```