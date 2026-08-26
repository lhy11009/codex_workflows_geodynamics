# Branch workflow

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

   If a separate <personal-fork> repository presents, add my fork as the `lhy11009` remote:

   ```bash
   git remote add lhy11009 <personal-fork-url>
   ```

   If the repository already exists locally, do not clone another copy. Use the existing repository.

   Verify the remote configuration:

   ```bash
   git remote -v
   ```

   The required convention is:

   ```text
   origin    -> authoritative upstream repository
   lhy11009  -> my GitHub fork, in case there is a separate <personal-fork>
   ```

   If either remote is missing, points to an unexpected repository, or the remote configuration is otherwise ambiguous, stop and report the problem. Do not rename, replace, or modify an existing remote without explicit permission.

2. **Fetch both remotes.**

   ```bash
   git fetch origin
   git fetch lhy11009  # in case there is a separate <personal-fork>
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

# Verification workflow

This serve to verifiy the workflow defined here.

Don't execute this unless specifically asked for workflow verification

Follow the Git branch workflow.
Execute the workflow strictly in the order specified there. Do not skip, reorder, or substitute steps.

For each step:
	1. State briefly what you are about to verify or do.
	2. Perform the required Git/GitHub operation.
	3. Verify that the operation succeeded before proceeding to the next step.
	4. Report the successful result briefly.

New test branches:
	Name the two new branch tdd_to_pr_workflow_verification and codex/tdd_to_pr_workflow_verification;
  When creating these branches, if you find existing local branches with the same name, delete them.
  If remote repository with the same name already exists, do forced push.

Test feature to implement:
	Add a codex_message.txt directory below the repository root with this contents: "This verifies the TDD-to-PR workflow"

If any step fails, produces an unexpected result, or conflicts with the repository state:
	• Stop immediately.
	• Do not attempt subsequent steps.
	• Do not change Git remotes, credentials, authentication settings, or repository configuration in an attempt to fix the problem.
	• Report which step failed, the command or operation that failed, and the relevant error/output.
	• Wait for my instructions before continuing.
In particular, verify the configured remotes and branch state before creating or pushing any branches.
Follow all restrictions in AGENTS.md, including the rules governing origin, lhy11009, target/contribution branches, codex/ working branches, pushes, pull requests, and merges.
