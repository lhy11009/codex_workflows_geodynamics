Follow the Git branch workflow defined in AGENTS.md.
Execute the workflow strictly in the order specified there. Do not skip, reorder, or substitute steps.
For each step:
	1. State briefly what you are about to verify or do.
	2. Perform the required Git/GitHub operation.
	3. Verify that the operation succeeded before proceeding to the next step.
	4. Report the successful result briefly.
New test branches:
	Name the two new branch tdd_to_pr_workflow_verification and codex/tdd_to_pr_workflow_verification;
Test feature to implement:
	Add a codex_message.txt directory below the repository root with this contents: "This verifies the code-manager workflow"
If any step fails, produces an unexpected result, or conflicts with the repository state:
	• Stop immediately.
	• Do not attempt subsequent steps.
	• Do not change Git remotes, credentials, authentication settings, or repository configuration in an attempt to fix the problem.
	• Report which step failed, the command or operation that failed, and the relevant error/output.
	• Wait for my instructions before continuing.
In particular, verify the configured remotes and branch state before creating or pushing any branches.
Follow all restrictions in AGENTS.md, including the rules governing origin, lhy11009, target/contribution branches, codex/ working branches, pushes, pull requests, and merges.
