# codex_workflows_geodynamics
This folder contains my codex workflows in geodynamics modelling.

# Set up

## Codex CLI setup on Linux

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

## Codex sandbox setup

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
