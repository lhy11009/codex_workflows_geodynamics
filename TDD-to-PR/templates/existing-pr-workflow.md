# Branch workflow

Use this workflow when the user asks Codex to continue development on an **existing pull request** that has already been submitted to the authoritative upstream repository.

The existing pull request has a **PR/contribution branch** in the user's fork. This branch is already the source branch of the upstream pull request.

Use two levels of branches for continued development:

* The **existing PR/contribution branch**, such as `indicator_field`, is the branch already associated with the upstream pull request. Do not directly modify this branch.

* A **Codex working branch**, such as `codex/indicator_field`, is where Codex performs new work. Codex submits changes to the existing PR/contribution branch through a pull request within the user's fork.

The intended branch structure is:

```text
authoritative-upstream:main
            ↑
            │ existing upstream PR
            │
personal-fork:<PR-branch>
            ↑
            │ internal Codex PR
            │
personal-fork:codex/<PR-branch>
```

Do not work directly on `main`.

Do not directly modify the existing PR/contribution branch.

Do not create another upstream pull request.

For each task, follow these steps in order:

1. **Identify the existing pull request.**

   The user must specify the existing pull request to work on, preferably using its GitHub PR URL or PR number.

   Determine:

   * the authoritative upstream repository;
   * the upstream PR number;
   * the PR base repository and branch;
   * the PR head repository and branch;
   * whether the PR is open;
   * whether the PR head branch belongs to the configured personal fork.

   The existing PR head branch becomes the **PR/contribution branch** for this workflow.

   Do not infer the PR branch solely from the current local branch.

   If the pull request cannot be identified unambiguously, is closed or merged, or its head repository/branch conflicts with the configuration in `REPOSITORIES.md`, stop and report the problem.

2. **Verify or initialize the local repository.**

   First determine whether the repository is already present in the expected local project directory.

   If the repository is not present locally, clone the authoritative upstream repository. The authoritative upstream repository must be configured as `origin`:

   ```bash
   git clone <upstream-repository-url>
   cd <repository>
   ```

   If a separate `<personal-fork>` repository is present, add the configured personal fork remote:

   ```bash
   git remote add <personal-fork-remote> <personal-fork-url>
   ```

   If the repository already exists locally, do not clone another copy. Use the existing repository.

   Verify:

   ```bash
   git remote -v
   git status
   git branch --show-current
   ```

   Verify the remote configuration against `REPOSITORIES.md`.

   If a required remote is missing, points to an unexpected repository, or the configuration is ambiguous, stop and report the problem.

   Do not rename, replace, add, remove, or modify an existing remote unless explicitly instructed.

3. **Check for existing local changes.**

   Inspect:

   ```bash
   git status
   ```

   Determine whether there are existing modified, staged, or untracked files.

   Do not discard, reset, clean, overwrite, or silently stash existing user changes.

   If existing changes could interfere with the requested work or branch switching, stop and report their state.

4. **Fetch the required remotes.**

   Fetch the authoritative upstream repository:

   ```bash
   git fetch origin
   ```

   If a separate personal fork is configured, fetch it as well:

   ```bash
   git fetch <personal-fork-remote>
   ```

   Verify that all required fetch operations succeed before proceeding.

5. **Verify the existing PR/contribution branch.**

   Confirm that the branch identified from the existing pull request exists on the configured personal fork.

   For example:

   ```text
   <personal-fork-remote>/indicator_field
   ```

   Verify that this remote branch corresponds to the head branch of the existing upstream pull request.

   Do not recreate, reset, overwrite, rebase, delete, or force-push the PR/contribution branch.

   If the branch cannot be found or does not correspond to the existing pull request, stop and report the problem.

6. **Prepare the local PR/contribution branch.**

   If the PR/contribution branch does not exist locally, create a local tracking branch from the personal fork:

   ```bash
   git switch -c <PR-branch> --track <personal-fork-remote>/<PR-branch>
   ```

   If it already exists locally, verify that it corresponds to the expected remote branch.

   Do not reset or overwrite the local branch merely to make it match the remote.

   If the local and remote states differ unexpectedly, stop and report the divergence.

   Do not make requested code modifications on this branch.

7. **Create the Codex working branch.**

   Create a Codex working branch from the current PR/contribution branch:

   ```bash
   git switch -c codex/<PR-branch> <PR-branch>
   ```

   All requested code modifications and commits must be made on this branch.

   If `codex/<PR-branch>` already exists locally or remotely, do not automatically reset, delete, overwrite, or force-push it.

   Stop and report its state unless the task explicitly instructs you to continue using that branch.

8. **Inspect the existing pull request.**

   Before modifying code, understand the current state of the upstream pull request.

   Inspect, when available:

   * the PR title and description;
   * the complete diff relative to its upstream base branch;
   * existing commits;
   * review status;
   * reviewer comments;
   * unresolved review conversations;
   * requested changes;
   * automated CI/status checks.

   Distinguish between:

   * issues already addressed by the existing PR;
   * unresolved reviewer requests;
   * new work requested by the user;
   * unrelated observations.

   Do not modify code merely because Codex notices an unrelated improvement.

9. **Investigate the requested change.**

   Before modifying code:

   * identify the affected subsystem;
   * inspect relevant implementation and declarations;
   * inspect relevant tests;
   * inspect important callers when necessary;
   * inspect similar existing implementations when useful;
   * relate the requested work to relevant reviewer comments when applicable.

   For design-sensitive reviewer comments, explain the issue and possible implementation choices to the user before making a substantial architectural change when the correct solution is not clear.

10. **Make the requested changes.**

Make changes only on the `codex/<PR-branch>` working branch.

Follow the development and test-driven-development rules in `AGENTS.md`.

Keep changes scoped to the requested task or reviewer feedback.

Do not modify the existing PR/contribution branch directly.

11. **Run tests and checks.**

Run relevant focused tests first.

Run broader tests and checks when appropriate.

Fix failures caused by the changes when appropriate.

If a required test cannot be run or a failure cannot safely be resolved, report it rather than bypassing the test.

12. **Review the changes.**

Before committing, inspect:

```bash
git status
git diff
```

Also inspect the relationship to the existing PR branch:

```bash
git diff <PR-branch>...HEAD
```

Verify that:

* only intended files were changed;
* changes address the requested task or reviewer feedback;
* unrelated changes were not introduced;
* no credentials or secrets were introduced.

13. **Commit the changes.**

Commit the completed and tested changes to the Codex working branch.

Use a concise commit message describing the change.

14. **Push the Codex working branch.**

Push only the Codex working branch to the configured personal fork:

```bash
git push -u <personal-fork-remote> codex/<PR-branch>
```

Never push the Codex working branch to `origin`.

Do not push directly to the existing PR/contribution branch.

15. **Create a pull request within the personal fork.**

Create an internal pull request:

```text
personal-fork:codex/<PR-branch>
              ↓
personal-fork:<PR-branch>
```

This pull request represents Codex's proposed update to the existing upstream PR.

Do not create the pull request against `main`.

Do not create another pull request against the authoritative upstream repository.

16. **Check the internal pull request.**

Check the pull request is created with a valid PR number and and a github link

17. **Stop for user review.**

Stop after the internal pull request has been prepared and checked.

Do not merge the pull request.

Report:

```text
Upstream PR:
PR/contribution branch:
Codex working branch:
Internal pull request:
Local tests:
Internal CI status:
Existing upstream CI status:
Reviewer requests addressed:
Outstanding issues:
```

I will review and merge the Codex pull request into the existing PR/contribution branch myself.

Once I merge it, the existing upstream pull request will automatically receive the new commits.

Do not merge either pull request.

Do not create a new upstream pull request.

# Review workflow

Use this workflow when the requested task involves addressing reviewer feedback on the existing pull request.

Do not execute it unless the user specifically asks to inspect, respond to, or address review feedback.

For each reviewer comment or requested change:

1. **Identify the review request.**

   Determine exactly what the reviewer is asking.

   Preserve the relationship between the comment and the code or discussion to which it refers.

2. **Investigate before changing code.**

   Inspect the relevant implementation, interfaces, tests, and surrounding architecture.

   Determine whether the reviewer is:

   * requesting a clear implementation change;
   * asking a question;
   * suggesting an alternative design;
   * identifying a bug;
   * requesting clarification;
   * raising a broader architectural issue.

3. **Do not automatically implement ambiguous design suggestions.**

   If there are multiple reasonable solutions or the request affects architecture/API design, report:

   * the reviewer's concern;
   * the relevant existing design;
   * possible solutions;
   * trade-offs;
   * the recommended approach.

   Stop for user input before implementing a substantial design decision when the intended solution is ambiguous.

4. **Implement agreed changes.**

   Make modifications only on the Codex working branch.

   Follow the TDD and testing requirements in `AGENTS.md`.

5. **Verify the change.**

   Run relevant tests and inspect the diff.

6. **Do not submit reviewer replies automatically.**

   Codex may draft a proposed response to a reviewer when requested.

   Do not post review replies, resolve review conversations, dismiss reviews, or otherwise act on reviewer discussions unless explicitly instructed.

# Verification workflow

This serves to verify the workflow defined here.

Do not execute this unless specifically asked for existing-PR workflow verification.

The user must provide a suitable existing test pull request and explicitly authorize its use for verification.

Follow the existing-PR branch workflow strictly in the order specified above.

Do not use a real scientific or production pull request merely to test this workflow unless explicitly instructed.

For each step:

1. State briefly what you are about to verify or do.
2. Perform the required Git/GitHub operation.
3. Verify that the operation succeeded before proceeding.
4. Report the successful result briefly.

Use a temporary Codex working branch named:

```text
codex/existing_pr_workflow_verification
```

The verification change should be harmless and clearly identifiable as workflow testing.

If any step fails, produces an unexpected result, or conflicts with the repository state:

* Stop immediately.
* Do not attempt subsequent steps.
* Do not change Git remotes, credentials, authentication settings, or repository configuration in an attempt to fix the problem.
* Report which step failed, the command or operation that failed, and the relevant error/output.
* Wait for my instructions before continuing.

Do not force-push, reset, overwrite, or delete the existing PR/contribution branch as part of workflow verification.

Follow all restrictions in `AGENTS.md`.
