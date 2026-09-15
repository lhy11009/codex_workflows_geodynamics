# Remote Monitoring Verification Workflow

This workflow verifies that Codex can access a configured remote server
through SSH, execute the user's `sq` command on that server, and return
the command output to the user.

This is a read-only verification workflow.

Do not execute this workflow unless the user explicitly asks for remote
monitoring verification.

# Purpose

Verify the following chain:

```text
Codex
  ↓
~/.ssh/config
  ↓
SSH
  ↓
remote server
  ↓
sq
  ↓
return command output
```

This workflow must not submit, cancel, restart, or otherwise modify jobs.

# Workflow

Follow these steps in order.

## 1. Identify the remote server

Determine the SSH host alias specified by the user.

Use:

```text
~/.ssh/config
```

as the authoritative source for SSH connection information.

Confirm that the requested host alias exists in the SSH configuration.

Do not modify the SSH configuration.

If the server cannot be identified unambiguously, stop and ask the user
which SSH host alias to use.

## 2. Verify SSH access

Test remote access using a simple non-destructive command.

For example:

```bash
ssh <server> 'hostname'
```

Verify that:

- SSH successfully connects;
- authentication succeeds;
- the remote command executes;
- a hostname is returned.

Report:

```text
SSH access: PASS
Server alias: <server>
Remote hostname: <hostname>
```

If SSH access fails, stop immediately.

Report the SSH error and do not attempt to modify SSH keys,
authentication settings, `~/.ssh/config`, or `known_hosts`.

## 3. Execute `sq`

Use the user's existing `sq` command to inspect Slurm jobs.

First try:

```bash
ssh <server> 'sq'
```

Do not substitute another Slurm command for `sq` during this verification.

Capture the complete screen output of the command.

If the command succeeds, continue to the reporting step.

## 4. Handle an unavailable `sq` alias

The user's `sq` command may be defined as a shell alias or shell
function on the remote system.

A non-interactive SSH command may not load the shell initialization file
that defines the alias.

If:

```bash
ssh <server> 'sq'
```

fails because `sq` is not found, try invoking it through the user's
interactive Bash environment:

```bash
ssh <server> 'bash -ic "sq"'
```

Use this only to invoke the existing user-defined `sq` command.

Do not modify remote shell initialization files.

Do not create a replacement alias.

Do not replace `sq` with `squeue` or another Slurm command merely to
make the verification pass.

If `sq` still cannot be executed, stop and report:

```text
SSH access: PASS
sq command: FAIL
Reason: <error>
```

## 5. Return the `sq` output

Return the complete screen output produced by `sq` to the user.

Do not interpret, summarize, reformat, or otherwise modify the `sq`
output.

Report:

```text
Remote monitoring verification

Server alias: <server>
Remote hostname: <hostname>

SSH access: PASS
sq command: PASS

sq output:

<complete screen output from sq>
```

If `sq` executes successfully but produces no output, report that the
command succeeded and returned no output.

# Safety

This verification workflow is read-only.

Do not:

- submit jobs;
- cancel jobs;
- restart jobs;
- resubmit jobs;
- hold or release jobs;
- modify job priorities;
- modify remote files;
- modify Slurm scripts;
- modify shell configuration;
- modify SSH configuration;
- modify authentication;
- install software.

Do not execute modifying Slurm commands such as:

```text
sbatch
scancel
srun
```

Do not execute filesystem-modifying commands such as:

```text
rm
mv
```

# Failure handling

If any required step fails:

1. Stop the verification workflow.
2. Identify the failed step.
3. Report the command that failed.
4. Report the relevant error output.
5. Do not attempt to repair configuration automatically.
6. Wait for user instructions.

Use the following format:

```text
Remote monitoring verification: FAIL

Failed step:
Command:
Error:
Likely cause:
Recommended next action:
```

# Successful completion

The workflow passes when:

1. the requested SSH host is resolved through `~/.ssh/config`;
2. SSH authentication succeeds;
3. a remote command can be executed;
4. the user's `sq` command executes successfully;
5. the screen output from `sq` is returned to the user.

Report:

```text
Remote monitoring verification: PASS

SSH access: PASS
sq command: PASS

sq output:

<complete screen output>
```

Do not perform any additional remote operations after successful
verification unless the user explicitly requests them.