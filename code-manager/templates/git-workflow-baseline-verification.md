Goal:
Verify that this Codex environment can perform the complete local Git → GitHub → pull-request workflow for a repository I specify.

General rules:
- Perform the following stages strictly in order.
- Do not skip a stage.
- After each stage, report PASS or FAIL and the evidence used to determine the result.
- If any required check fails, STOP immediately.
- Do not attempt subsequent stages after a failure.
- Tell me exactly which command/action failed, the relevant error message, and what I need to do to resolve it.
- Do not change Git configuration, credentials, authentication settings, or system settings without my explicit approval.
- Do not modify the default branch directly.
- Do not force-push, reset, clean, delete branches, or overwrite existing work.

Repository:
https://github.com/lhy11009/HaMaGeoLib

## Stage 1 — Verify local Git

Verify that Git is available to the Codex shell environment.

Check:
1. `git --version`
2. Locate the Git executable.
3. Report the current working directory.
4. Report the Git version and executable path.

PASS if Codex can successfully execute Git commands.

If this stage fails, STOP.

## Stage 2 — Verify remote repository access and clone

Verify that Codex can access the repository I provided.

Before cloning:
1. Use `git ls-remote <REPOSITORY-URL> HEAD` to verify remote read access.
2. Determine the appropriate local repository location according to this project's workspace rules.
3. Make sure the target directory does not already contain an unrelated repository.

Then clone the repository.

After cloning, verify:
1. `git remote -v`
2. Current branch.
3. `git status`
4. The remote repository corresponds to the repository I specified.

Do not modify any repository files yet.

PASS if Codex can read the remote repository and successfully create a valid local clone.

If this stage fails, STOP.

## Stage 3 — Verify authenticated GitHub write access

Verify that the current environment is authenticated with GitHub and has permission to write to my fork/repository.

Do NOT modify the default branch.

First inspect:
1. Existing Git remotes.
2. Git user configuration relevant to commits.
3. Available GitHub authentication, such as Git credentials or GitHub CLI authentication.

Create a temporary verification branch from the current default branch.

Make only a harmless verification change, such as adding a temporary file specifically identified as an access test.

Commit the change on the temporary branch and push that branch to my repository.

Do NOT merge it.

PASS if:
- a local commit can be created, and
- the temporary branch can be successfully pushed to my GitHub repository.

If authentication or write permission fails, STOP and report whether the problem appears to be Git identity, GitHub authentication, repository permission, remote configuration, or another issue.

## Stage 4 — Verify pull-request capability

Using the temporary branch from Stage 3:

1. Determine whether GitHub CLI (`gh`) or another available mechanism can create a pull request.
2. Verify authentication for that mechanism.
3. Create a PR from the temporary verification branch to the repository's default branch.
4. Clearly identify the PR as a temporary workflow verification PR.
5. Do NOT merge the PR.
6. Report the PR URL and current CI/check status, if available.

PASS if the pull request is successfully created and Codex can inspect its status/checks.

Do not merge, close, or otherwise modify the PR after creating it unless I explicitly ask.

## Final report

If all four stages pass, report:

Stage 1 — Local Git: PASS
Stage 2 — Remote access and clone: PASS
Stage 3 — Authenticated write access: PASS
Stage 4 — Pull-request capability: PASS

Also report:
- Git version
- local repository path
- origin URL
- current/default branch
- GitHub authentication method detected
- whether `gh` is available
- temporary branch name
- commit created
- PR URL
- CI/check status

If any stage fails, report:

Stage <N> — <name>: FAIL

Then provide:
- the exact operation that failed
- relevant error output
- likely cause
- recommended action for me

Do not continue to later stages.