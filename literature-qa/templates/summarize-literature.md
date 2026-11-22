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

Use only information contained in the specified PDF and its associated supplementary files, if available.

Do not use:

- web searches;
- external literature;
- general knowledge as supporting evidence; or
- information from other PDFs in the literature collection, except for supplementary files identified by the rules below.

If the requested information is not provided by the paper or its supplementary files, state that it is not provided rather than filling the gap using outside knowledge.

## Workflow

1. Locate the specified PDF.

2. **Locate associated supplementary files.**
   - After locating the main PDF, search the same directory for PDF files with the same base filename followed by one of these suffixes:
     - `_sup`
     - `_supplementary`
     - `_appendix`
   - For example, if the main file is `paper.pdf`, look for:
     - `paper_sup.pdf`
     - `paper_supplementary.pdf`
     - `paper_appendix.pdf`
   - If one or more matching files exist, treat them as extensions of the main paper.
   - Read and use these files alongside the main PDF when identifying methods, results, figures, and scientific claims.
   - When citing information from supplementary files, distinguish supplementary figures, tables, and PDF page numbers from those in the main paper.
   - If no matching files exist, proceed using only the main PDF.
   - Do not include unrelated PDFs or files with different base filenames.

3. Read enough of the main paper and associated supplementary files to understand their overall structure, motivation, methods, results, discussion, and conclusions.

4. Identify the main scientific claims and the PDF pages that support them.


## Output

Summary into a `<filename>.md` file under the foler `literature-qa/.dtemp` 

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

3. Summarize the methods used in the current study.

   - Identify the main methods, models, experiments, observations, datasets, or analytical approaches used in the paper.

   - For each method, use 1--4 sentences to briefly summarize the important model or experimental setup, assumptions, parameters, initial or boundary conditions, and analysis procedures.

   - Then, for each method, use 1--2 sentences to briefly explain its purpose and how it is used to obtain the results that support the key takeaways.

   - Focus on methodological information that is relevant to the key takeaways rather than reproducing every technical detail provided in the paper.

4. Provide a forward summary.

   Organize the summary in the following order:

   - Start with the background knowledge and previous studies. Exclusively include all the background points identified in Section 1. For each point, provide one sentence explaining why it is important for understanding the main takeaways of the paper.

   - Then summarize the results of the current study, following the order in which the figures are presented in the main text, including figures from associated supplementary files.

     - For each figure, start with a one-sentence summary of its main result. Then incorporate the relevant points identified in Section 1 and explain how the figure supports or illustrates the key takeaways. If a figure is important for multiple takeaways, discuss each connection as a separate point.

     - Include supplementary figures from associated supplementary files in the forward summary. Label them using their original supplementary figure numbers (e.g., `Figure S1`, `Figure S2`).

     - **Insert supplementary figures according to the order in which they are first mentioned in the main text**, rather than placing all supplementary figures at the end.

     - For example, if `Figure S1` is first mentioned in the main text between the discussions of `Figure 1` and `Figure 2`, organize the forward summary as:
       - `#### Figure 1`
       - `#### Figure S1`
       - `#### Figure 2`

     - If multiple supplementary figures are mentioned between two main figures, preserve their order of first mention in the main text.

     - If a supplementary figure is not mentioned in the main text, place it after all figures referenced in the main text, maintaining its original supplementary figure numbering.

     - Use information from the supplementary files to explain the supplementary figures, but maintain the scientific narrative established by the main paper.

   - Finally, summarize the arguments and interpretations developed in the discussion. Exclusively include all the discussion points identified in Section 1. For each point, explain how it relates to the background knowledge listed earlier and how the argument is developed or supported by the results and figures of the current study, including supplementary figures where relevant.

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

## Methods

### Method 1

**Method:** <name or brief description of the method>

- **Setup:** <1--4 sentences summarizing the important model or experimental setup, assumptions, parameters, initial or boundary conditions, and analysis procedures>
- **Purpose:** <1--2 sentences explaining the purpose of the method and how it is used to obtain the results that support the key takeaways>

### Method 2

**Method:** <...>

- **Setup:** <...>
- **Purpose:** <...>

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