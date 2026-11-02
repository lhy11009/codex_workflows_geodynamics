# Workspace Structure

This repository contains the reusable code-manager workflow.

The workspace is expected to have the following structure:

<workspace-root>/
├── code-manager/
│   ├── AGENTS.md
│   ├── README.md
│   ├── skills/
│   ├── scripts/
│   └── notes/
│
└── .softwares/
    ├── <repository-1>/
    ├── <repository-2>/
    └── ...

## Path conventions

- Do not assume an absolute path such as `D:\Codex`.
- Check that the `<workspace-root>` folder contains the `code-manager`, otherwise warn me that there might be a problem
- Software repositories are located under:
  `<workspace-root>/.softwares/`

# Development workflow

## Test-driven development

For code changes:

1. Inspect the existing implementation and tests.
2. Add a test demonstrating the requested behavior.
3. Run the test and verify that it fails for the expected reason.
4. Make the smallest implementation change necessary.
5. Run the affected tests again.
6. Run the broader test suite when appropriate.

## Code changes

- Prefer small, localized changes.
- Follow existing coding conventions.
- Do not refactor unrelated code.
- Preserve backward compatibility unless explicitly requested.
- Always follow the workflow in `<workspace-root>/code-manager/templates/new-pr-workflow.md` to apply changes.
- Always first show a plan to the user. Only apply the changes after user say something like "proceed" or "apply the changes".

## Repository configuration

Before working on a software repository:

1. Check that the user's task explicitly identifies the repository to work on.

   * The repository may be identified by its configured repository name.
   * If no repository is specified, or if the repository cannot be identified unambiguously, stop and ask the user to specify the repository.
   * Do not infer the target repository from the current working directory, previous tasks, or other contextual clues.

2. Read `<workspace-root>/.local/REPOSITORIES.md`.

3. Locate the section corresponding to the requested repository.

4. Verify that the requested repository is defined in `REPOSITORIES.md`.

5. Use only the repository location, remotes, environment, build commands, test commands, and other repository-specific configuration defined there.

6. If the requested repository is not defined in `REPOSITORIES.md`, stop and ask the user for the required repository configuration.

7. Do not infer or invent repository-specific configuration.

## Local repository

* Local repository should be <workspace-root>/.softwares/<name-of-repository> if not otherwise specified.

## Python environment

* If the repository uses python, use the conda environment mentioned in `REPOSITORIES.md`.
* Before activating the conda environment, assert it exists. And after activating it, assert that the environment is properly set.
* Use pytest to run all the python tests when you need to validate your changes to the code.

## Git and GitHub workflow

A repository typically uses the following remote locations:

* There is an authoritative upstream repository (i.e. <upstream-repository>).
* There could also be my personal GitHub fork. If not explicitly mentioned in `REPOSITORIES.md`, assume this the same with the authoritative upstream repository (i.e. <personal-fork>).
* In case <upstream-repository> is different from <personal-fork>, treat <upstream-repository> as read-only, and never push to <upstream-repository>.
* <personal-fork> is the only remote you may push to.

Before making changes, verify the repository configuration with:

```bash
git remote -v
git status
git branch --show-current
```

If the remotes do not follow the convention above, stop and report the problem. Do not add, remove, rename, or modify remotes unless explicitly instructed.

### Branch workflow

Branch workflow defines how to work on different local branch with git and interact with the remote branches on github.

For a specific task, either ask the user for a desired branch workflow or follow the workflow defined in "Branch workflow" of a given md file.

### Restrictions

Unless explicitly instructed otherwise:

* Never push to `origin`.
* Never push directly to `main`.
* Never push directly to the target/integration branch.
* Never force-push.
* Never merge a pull request.
* Never create a pull request to the upstream `origin` repository.
* Never modify Git or GitHub authentication settings.
* Never expose, print, commit, or store authentication tokens or other credentials in the repository.
* Do not modify the configured Git remotes without explicit permission.
* If authentication, authorization, remote configuration, branch state, or push operations fail, stop and report the failure rather than attempting to change credentials or bypass the restriction.

The final pull request from my fork to the upstream repository will be created and submitted by me.


## CI

If GitHub CI fails:

1. Inspect the failing job.
2. Determine whether the failure is caused by the PR.
3. Reproduce the failure locally when possible.
4. Fix the underlying issue.
5. Do not disable or weaken tests simply to make CI pass.
6. Push the fix and verify CI again.


## Notebook explanation workflow

### Trigger

When the user includes the phrase `notebook explanation` in a request, activate this workflow.

- The trigger is case-insensitive and may appear anywhere in the user's request.
- Without this trigger, respond normally in the conversation unless the user explicitly requests a Jupyter notebook.

### Workflow

1. **Create a Jupyter notebook (`.ipynb`)** to explain the requested scientific, mathematical, or technical topic.

2. **Use Markdown cells for explanations and equations.**
   - Use LaTeX syntax (`$...$` and `$$...$$`) for mathematical expressions.
   - Use `aligned` or similar environments for multiline derivations.
   - Explain variables, assumptions, and intermediate steps clearly.
   - Ensure equations are compatible with Jupyter's Markdown rendering.

3. **Generate scientific sketches when helpful.**
   - Prefer Python and Matplotlib for diagrams, vector illustrations, coordinate systems, and physical processes.
   - Include clear labels, annotations, arrows, and units where appropriate.
   - Distinguish conceptual sketches from quantitative results.
   - Prefer scientifically meaningful diagrams over decorative illustrations.

4. **Include executable Python examples when appropriate.**
   - Use numerical demonstrations to illustrate mathematical or physical concepts.
   - Keep code cells self-contained and reproducible whenever possible.
   - Use the Python environment configured for the relevant repository when applicable.

5. **Validate the notebook.**
   - Execute relevant code cells when the environment permits.
   - Verify that all executed cells run successfully.
   - Check that figures render correctly and mathematical expressions use valid Jupyter-compatible LaTeX syntax.
   - Remove unnecessary debugging output and execution errors.

6. **Save and name the notebook.**
   - Save all generated notebooks under `<workspace-root>/code-manager/notes/` unless the user specifies another location.
   - Use the filename convention `YYYY-MM-DD-topic.ipynb`.
   - Use the current date for `YYYY-MM-DD`.
   - Generate a short, descriptive topic based on the explanation.
   - Use lowercase letters and underscores (`_`) to separate words in the topic.
   - Avoid spaces and special characters in filenames.
   - Examples:
     - `2026-11-02-jaumann_stress_rate.ipynb`
     - `2026-11-02-upwind_discretization.ipynb`
     - `2026-11-02-coordinate_transformations.ipynb`
   - If a notebook with the same filename already exists, append a numerical suffix (e.g., `_2`, `_3`) rather than overwriting it.
   - Do not modify or overwrite existing notebooks unless the user explicitly requests an update to a specific notebook.

7. **Summarize the results in the conversation.**
   - Provide a short summary of the explanation and its main conclusions.
   - Report the final notebook path.
   - Mention any limitations if notebook execution or validation could not be completed.

### Restrictions

- This workflow is intended for explanation and visualization, not repository code modification.
- Do not modify repository source code unless explicitly requested.
- Notebook generation does not require the repository code-change approval workflow.
- If the explanation concerns a specific repository, follow the repository identification and configuration requirements before inspecting its code.
- Do not invent repository-specific details, numerical results, or scientific assumptions.
- Prefer conceptual clarity, mathematical correctness, and reproducible figures over visual complexity.
