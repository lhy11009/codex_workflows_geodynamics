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

## Local repository

* Local repository should be <workspace root>/Softwares/gdmate

## Python environment

* Use conda environment py-gdmate to execute commands with the gdmate package.
* Before activating the conda environment, assert it exists. And after activating it, assert that the environment is properly set.
* Use pytest to run all the python tests when you need to validate your changes to the code.

## Git and GitHub workflow

This repository uses the following remote naming convention:

* `origin` refers to the authoritative upstream repository https://github.com/gdmate/gdmate.
* `lhy11009` refers to my personal GitHub fork at https://github.com/lhy11009/gdmate
* Treat `origin` as read-only. Never push to `origin`.
* `lhy11009` is the only remote you may push to.

Before making changes, verify the repository configuration with:

```bash
git remote -v
git status
git branch --show-current
```

If the remotes do not follow the convention above, stop and report the problem. Do not add, remove, rename, or modify remotes unless explicitly instructed.

### Branch workflow

Use two levels of branches for development:

* A **target/contribution branch**, such as `fix-parser`, represents the complete change that may later be submitted to the upstream repository. This branch is based on `origin/main` and pushed to `lhy11009`.
* A **Codex working branch**, such as `codex/fix-parser`, is where Codex performs its work. Codex submits changes to the target/contribution branch through a pull request.

Do not work directly on `main` or directly modify the target/contribution branch.

For each task, follow these steps in order:

1. **Verify or initialize the local repository.**

   First determine whether the repository is already present in the expected local project directory.

   If the repository is not present locally, clone the authoritative upstream repository. The upstream repository must be configured as `origin`:

   ```bash
   git clone <upstream-repository-url>
   cd <repository>
   ```

   Then add my fork as the `lhy11009` remote:

   ```bash
   git remote add lhy11009 https://github.com/lhy11009/<repository>.git
   ```

   If the repository already exists locally, do not clone another copy. Use the existing repository.

   Verify the remote configuration:

   ```bash
   git remote -v
   ```

   The required convention is:

   ```text
   origin    -> authoritative upstream repository
   lhy11009  -> my GitHub fork
   ```

   If either remote is missing, points to an unexpected repository, or the remote configuration is otherwise ambiguous, stop and report the problem. Do not rename, replace, or modify an existing remote without explicit permission.

2. **Fetch both remotes.**

   ```bash
   git fetch origin
   git fetch lhy11009
   ```

   Verify that both fetch operations succeed before proceeding.

3. **Identify the target/contribution branch.**

   Identify the user-specified target branch, for example `fix-parser`.

   If no target branch has been specified, figure out the name youself from the tasks it involves.

4. **Create the target/contribution branch.**

   The target/contribution branch must start from the current upstream `origin/main`.

   For example:

   ```bash
   git switch -c fix-parser origin/main
   ```

   Push the new target branch to my fork:

   ```bash
   git push -u lhy11009 fix-parser
   ```

   The target/contribution branch is an integration branch. Do not make the requested code changes directly on this branch.

   If the target branch already exists locally or on `lhy11009`, do not recreate, reset, overwrite, or force-push it. Stop and report its current state unless the task explicitly instructs you to continue work on that existing target branch.

5. **Create the Codex working branch.**

   Create a separate working branch from the target/contribution branch. Use a descriptive `codex/` branch name.

   For example:

   ```bash
   git switch -c codex/fix-parser fix-parser
   ```

   All requested code modifications and commits must be made on this branch.

6. **Make the requested changes.**

   Make changes only on the `codex/` working branch. Do not modify `main` or the target/contribution branch directly.

7. **Run tests and checks.**

   Run the relevant tests and checks before submitting the work.

   Fix failures caused by the changes when appropriate. If a required test cannot be run or a failure cannot be resolved safely, report it rather than bypassing the test.

8. **Commit the changes.**

   Commit the completed and tested changes to the Codex working branch.

9. **Push the Codex working branch.**

   Push only the Codex working branch to my fork:

   ```bash
   git push -u lhy11009 codex/fix-parser
   ```

   Never push this branch to `origin`.

10. **Create a pull request within my fork.**

Create the pull request:

```text
lhy11009:codex/fix-parser
          ↓
lhy11009:fix-parser
```

Do not create the pull request against `main`.

Do not create a pull request against the upstream `origin` repository.

11. **Check the pull request.**

Check the pull request's automated tests/status checks when available.

Report whether they pass and describe any failures.

12. **Stop for user review.**

Stop after the pull request has been prepared and checked.

Do not merge the pull request.

I will review and merge the Codex pull request into the target/contribution branch myself. When the complete contribution is ready, I will create the final pull request from the target branch in my fork (for example, `lhy11009:fix-parser`) to the upstream repository's `main` branch.



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