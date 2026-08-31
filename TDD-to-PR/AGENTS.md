# Workspace Structure

This repository contains the reusable TDD-to-PR workflow.

The workspace is expected to have the following structure:

<workspace-root>/
├── TDD-to-PR/
│   ├── AGENTS.md
│   ├── README.md
│   ├── skills/
│   ├── scripts/
│   └── notes/
│
└── Softwares/
    ├── <repository-1>/
    ├── <repository-2>/
    └── ...

## Path conventions

- Do not assume an absolute path such as `D:\Codex`.
- Check that the `<workspace-root>` folder contains the `TDD-to-PR`, otherwise warn me that there might be a problem
- Software repositories are located under:
  `<workspace-root>/Softwares/`

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

## Repository configuration

Before working on a software repository:

1. Check that the user's task explicitly identifies the repository to work on.

   * The repository may be identified by its configured repository name.
   * If no repository is specified, or if the repository cannot be identified unambiguously, stop and ask the user to specify the repository.
   * Do not infer the target repository from the current working directory, previous tasks, or other contextual clues.

2. Read `REPOSITORIES.md`.

3. Locate the section corresponding to the requested repository.

4. Verify that the requested repository is defined in `REPOSITORIES.md`.

5. Use only the repository location, remotes, environment, build commands, test commands, and other repository-specific configuration defined there.

6. If the requested repository is not defined in `REPOSITORIES.md`, stop and ask the user for the required repository configuration.

7. Do not infer or invent repository-specific configuration.

## Local repository

* Local repository should be <workspace-root>/Softwares/<name-of-repository> if not otherwise specified.

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