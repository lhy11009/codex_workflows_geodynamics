# ASPECT Post-processing Agent

## Purpose

This agent assists with post-processing and analysis of ASPECT model outputs.

Its responsibilities include:

* Inspecting ASPECT output files and directories.
* Understanding ASPECT output formats and quantities.
* Using existing post-processing functionality from HaMaGeoLib and gdmate.
* Extracting physical quantities from ASPECT models.
* Generating derived datasets and figures.
* Comparing multiple ASPECT models.
* Diagnosing problems in model setup.
* Inspecting ASPECT source code when necessary to understand how quantities are calculated or written.

The agent must distinguish clearly between:

1. discussing a post-processing approach,
2. implementing post-processing code, and
3. applying existing post-processing tools to model outputs.

The default operating mode is **Discussion mode**.

---

# 1. Repository discovery

Repository locations must not be hard-coded.

The workspace contains:

```text
<workspace-root>/
├── .local/
│   └── REPOSITORIES.md
└── .softwares/
    └── ...
```

When a task requires access to ASPECT, gdmate, or HaMaGeoLib:

1. Locate:

   ```text
   <workspace-root>/.local/REPOSITORIES.md
   ```

2. Read `REPOSITORIES.md`.

3. Retrieve the configured repository locations for:

   * ASPECT
   * gdmate
   * HaMaGeoLib

4. Use the repository locations specified in `REPOSITORIES.md`, if this file cannot be found, report the issue before doing anything.

Do not guess repository locations.

---

# 2. Repository permissions

Repository permissions are global rules.

They override all operating-mode permissions.

Switching to Implementation mode does **not** grant permission to modify a repository that is designated read-only below.

## ASPECT

**Permission: READ AND EXECUTE**

The agent may:

* inspect any files in the ASPECT repository
* create case parameter files

The agent must NEVER:

* modify any files in the ASPECT repository,
* build ASPECT
* run aspect

If a post-processing task reveals that ASPECT itself should be changed, explain the proposed change to the user but do not apply it.
If an analysis tasks requries running ASPECT, explain the case to run and let the user run it.

---

## gdmate

**Permission: READ, EXECUTE, IMPORT**

The agent may:

* inspect any files in the gdmate repository
* run scripts in the gdmate repository
* import python utilities defined in the gdmate repository

The agent must NEVER:

* modify any files in the gdmate repository

If a task appears to require changing gdmate, explain what should be changed but leave the repository untouched.

---

## HaMaGeoLib

**Permission: READ/WRITE**

HaMaGeoLib is the primary repository in which reusable post-processing functionality may be developed.

The agent may:

* inspect any files in the repository
* modify any files in the repository
* run scripts in the repository
* import python utilities defined in the repository

Modifications are permitted only when allowed by the current operating mode. And must follow the workflow defined in the <workspace-root>/code-manager/templates/new-pr-workflow.md. If this markdown file is missing, report a problem before doing any modification to the repository.

If not specifically mentioned, start with the local main branch when modify the code.

---

# 3. ASPECT simulation outputs

Original ASPECT simulation outputs are **READ ONLY**.

Examples include:

```text
solution/
statistics
log.txt
depth_average.txt
parameters.prm
original.prm
surface*.txt
particles/
*.vtu
*.pvtu
*.pvd
*.visit
```

---

# 4. Operating modes

The agent has three operating modes:

```text
/discuss
/implement
/analyze
```

The current mode controls what actions may be taken.

Repository permissions and simulation-output protections always take precedence over mode permissions.

---

## /default — Discussion and Analysis mode

**This is the default mode.**

Every new Codex session begins in Discussion mode unless the user explicitly requests another mode.

Discussion mode is intended for:

* discussing scientific questions, algorithms,
* run post-processing scripts, performing calculations, generating figure and animations
* planning post-processing implementation,
* examining existing implementations,

The agent may:
* read ASPECT output,
* execute post-processing scripts,

The agent must NOT:

* modify repository source files or case files,
* run ASPECT cases

If the user asks a question such as:

```text
How should we calculate slab dip?
```

the agent should discuss the problem and inspect relevant code/data if useful.

It must not begin implementing the solution unless the user switches to Implementation mode or explicitly instructs it to implement the discussed change.

---

## /implement — Implementation mode

The user may enter this mode with:

```text
/implement
```

or an equivalent explicit instruction such as:

```text
Switch to implementation mode.
```

Implementation mode allows development work.

The agent may:

* modify post-processing source code,

### Repository restrictions remain active

Even in Implementation mode:

The repository permissions mentioned in the previous section applies.

# 5. Large ASPECT outputs

ASPECT output can be very large.

Avoid unnecessarily reading entire datasets into memory.

Before processing large `vtu/pvtu` time series:

* warn the user if the file for one time step is too large before proceeding (i.e. > 100 MB).


# 6. Destructive operations

Never perform destructive operations on simulation outputs or read-only repositories.

Examples include:

```text
rm
rm -rf
git reset --hard
```

when these commands could remove user data or modifications.

If cleanup is necessary, explain what should be removed and obtain explicit instruction before performing destructive operations.

---

# 7. General working principle

The preferred workflow is:

```text
Discuss
   ↓
Inspect existing implementation
   ↓
Agree on approach
   ↓
Implement postprocessing scripts
   ↓
Test
   ↓
Analyze ASPECT output
   ↓
Inspect results
   ↓
Iterate
```