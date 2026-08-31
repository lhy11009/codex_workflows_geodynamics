# codex_workflows_geodynamics
This folder contains my codex workflows in geodynamics modelling.

Yes, I would make the top-level README describe the **convention**, not the current workflows by name.


## File organization

This repository contains multiple Codex workflows. Each workflow is organized in a separate top-level folder and should be largely self-contained.

### Top-level files

The repository root contains files that apply to the repository as a whole rather than to an individual workflow.

Typical top-level files include:

- `README.md` describes the overall organization and usage of the repository.
- `.gitignore` defines files and generated outputs that should not be tracked by Git.

Workflow-specific configuration and instructions should generally remain inside the corresponding workflow folder rather than being placed at the repository root.

### Workflow files

A typical workflow folder may contain:

```text
<workflow>/
├── AGENTS.md
├── README.md
├── environment.yml
├── scripts/
├── tests/
│   └── fixtures/
└── <generated-output>/
```

The files and directories have the following general purposes:

* `AGENTS.md` contains instructions that define how Codex should operate within the workflow, including its current scope and constraints.
* `README.md` contains user-facing documentation for the workflow, including its purpose, setup, and usage.
* `environment.yml` defines a Conda environment when the workflow requires its own Python dependencies.
* `scripts/` contains scripts and utilities used by the workflow.
* `tests/` contains automated tests for the workflow.
* `tests/fixtures/` contains small input datasets or files used specifically for testing.
* Generated-output directories contain files produced by the workflow. These files should normally be excluded from Git when they can be regenerated.

Not every workflow needs all of these files or directories. They should be added incrementally as required by the workflow.



## Set up

### Codex CLI setup on Linux

1. Install Codex CLI:

   ```bash
   npm install -g @openai/codex
   ````

2. Start Codex:

   ```bash
   codex
   ```

3. On first launch, select **Sign in with ChatGPT** and complete the browser authentication.

4. Verify that Codex is installed and available from Bash:

   ```bash
   which codex
   codex --version
   ```

### Codex sandbox setup

The Codex sandbox restricts Codex to a controlled set of filesystem locations, allowing it to work within the intended directories without giving it unrestricted write access to the rest of the system.

To start Codex with write access to the current directory, run the following command from the local working directory:

```bash
codex \
    --sandbox workspace-write
```

To grant Codex write access to an additional directory, use:

```bash
codex \
    --sandbox workspace-write \
    --add-dir <path-to-dir>
```

For example:

```bash
codex \
    --sandbox workspace-write \
    --add-dir "$WORLD_BUILDER_SOURCE_DIR"
```

This latter command is useful when the Codex workflow is launched from one directory but Codex also needs to modify a separate Git repository, such as ASPECT or WorldBuilder.

When starting Codex, check the terminal output for sandbox-related errors. If the sandbox fails to initialize, diagnose the sandbox configuration first (e.g. with chatgpt, could be resolved in 10 mins).



## Launch codex

### Terminal launch

Codex should normally be launched with the relevant workflow folder as its working directory:

```bash
codex -C <workflow> --sandbox workspace-write
```

Additional directories should be added to the sandbox only when required for the current task:

```bash
codex -C <workflow> --sandbox workspace-write --add-dir <additional-directory>
```
