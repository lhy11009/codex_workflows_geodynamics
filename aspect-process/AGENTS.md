# ASPECT Processing Agent

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

# Repository discovery

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

## Repository permissions

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

The branch should be the developed branch:

`haoyuan_main`

The HaHaGeoLib package depends on this exact branch of gdmate

---

## HaMaGeoLib

**Permission: READ/WRITE**

HaMaGeoLib is the primary repository in which reusable post-processing functionality may be developed.

The agent may:

* inspect any files in the repository
* modify any files in the repository
* run scripts in the repository
* import python utilities defined in the repository

Modifications are permitted and must follow the workflow defined in the <workspace-root>/code-manager/templates/new-pr-workflow.md. If this markdown file is missing, report a problem before doing any modification to the repository.
Modifications must always use the local main branch.

If not specifically mentioned, start with the local main branch when modify the code.

# Project discovery

Project directory refers to a location on local or remote systems that keeps copies of simulation cases.

Project locations and project-specific configurations must not be hard-coded.

When a task requires access to a modeling project, first locate:

```text
<workspace-root>/.local/PROJECTS.md
```

Read `PROJECTS.md` and identify the project requested by the user.

For example, a project entry may define different configurations for:

* Local
* Stampede3 (remote)
* other machines or remote systems

A project configuration may include:

* project directory,
* ASPECT branch,
* ASPECT build,
* HaMaGeoLib main notebook or processing scripts,
* HaMaGeoLib tests,
* machine or remote system,
* other project-specific paths or settings.

When the user refers to a project by name:

1. Locate `<workspace-root>/.local/PROJECTS.md`.
2. Find the corresponding project entry.
3. Determine which machine/configuration applies to the current task.
4. Retrieve the project directory and any other configuration required for the task.
5. Use the paths exactly as defined in `PROJECTS.md`.

Do not guess project locations or project-specific ASPECT branches, builds, notebooks, scripts, or tests.

If `PROJECTS.md` cannot be found, report the issue before performing any project-specific operation.

If the requested project is not defined in `PROJECTS.md`, report that the project is not configured and ask the user to add or provide the project configuration.

If the requested machine or remote configuration is not defined for that project, report the missing configuration rather than assuming a path.

## Project processing workflow

If `PROJECTS.md` defines a main notebook, main processing script, or other processing entry point for a project, use these files as the primary reference for understanding that project's post-processing workflow.

Paths identified as HaMaGeoLib notebooks, scripts, or tests are relative to the HaMaGeoLib repository unless `PROJECTS.md` explicitly states otherwise.

Before designing, implementing, or running project-specific post-processing:

1. Read the project's configuration from `PROJECTS.md`.
2. Identify any configured main notebook, processing scripts, and tests.
3. Locate these files relative to the HaMaGeoLib repository defined in `REPOSITORIES.md`.
4. Inspect the main notebook or processing scripts to understand the existing processing workflow.
5. Follow the existing workflow, conventions, data structures, function calls, file organization, and processing sequence when applicable.
6. Inspect the configured tests when implementation details or expected behavior need to be understood.
7. Prefer using or extending the existing project workflow rather than creating a separate or duplicate processing workflow.

The main notebook or processing scripts define the starting point for understanding how the project is currently processed. They do not override the global repository permissions or operating-mode rules.

Do not assume that a generic HaMaGeoLib or gdmate workflow applies to a project without first checking the project's configured main notebook or processing scripts.

If a configured notebook, script, or test path does not exist, report the issue rather than silently substituting another file.

## Project directory permissions

A project directory is distinct from the ASPECT, gdmate, and HaMaGeoLib software repositories.

The agent may inspect files in a configured project directory as required for processing and analysis.

The agent is also allowed to create new files in a configured project directory.

Original ASPECT simulation outputs are READ ONLY unless the user explicitly states otherwise.

The agent must not overwrite, modify, move, rename, or delete existing simulation outputs.

## Project-specific ASPECT branches and builds

If a project configuration defines an ASPECT branch or build, use that branch and build when determining which ASPECT source code, version, or executable is associated with the project.

### Inspecting ASPECT source code

If a task requires inspecting or inquiring about ASPECT source code for a specific project:

1. Read the project's configuration from `PROJECTS.md`.
2. Identify the ASPECT branch associated with the project.
3. Go to the ASPECT repository defined in `REPOSITORIES.md`.
4. Check the current Git status before changing branches.
5. Check out the project-specific ASPECT branch before inspecting the source code.
6. Verify that the expected branch is checked out.
7. Perform the requested source-code inspection on that branch.

Do not inspect another branch and assume that its implementation applies to the project.

If the project-specific ASPECT branch is not defined, report the issue rather than guessing which branch should be used.

If switching branches could overwrite, remove, or otherwise interfere with uncommitted changes in the ASPECT repository, stop and report the issue. Do not stash, discard, commit, or modify those changes.

Checking out an existing project-specific branch for read-only inspection is permitted. This does not grant permission to modify files in the ASPECT repository.

### ASPECT builds

If a project configuration defines an ASPECT build, use that build when determining which ASPECT version or executable is associated with the project.

The presence of an ASPECT build in `PROJECTS.md` does not grant permission to build or run ASPECT.

The global ASPECT permissions still apply.

If a task requires running ASPECT:

1. Prepare the case and parameter files as needed.
2. Verify the case configuration as far as possible without running ASPECT.
3. Identify the appropriate ASPECT branch and build from `PROJECTS.md`.
4. Verify that the case is intended for that branch/build.
5. Provide the exact command required to run the case.
6. Stop and let the user run ASPECT.
7. Continue processing or analysis after the user reports that the run has completed.

---


# ASPECT simulation outputs

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

## Large ASPECT outputs

ASPECT output can be very large.

Avoid unnecessarily reading entire datasets into memory.

Before processing large `vtu/pvtu` time series:

* warn the user if the file for one time step is too large before proceeding (i.e. > 100 MB).


# Destructive operations

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

# General working principle

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