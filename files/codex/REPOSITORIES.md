# gdmate

## Repository

Local directory:
/home/lochy/ASPECT_PROJECT/gdmate

Upstream:
https://github.com/gdmate/gdmate

Fork:
https://github.com/lhy11009/gdmate

## Git remotes

origin:
authoritative upstream, read-only

lhy11009:
personal fork, push allowed

## Development environment

Conda environment:
py-gdmate

Verify with:

conda env list
python -c "import sys; print(sys.executable)"

## Tests

Run focused tests with pytest.

Run the complete test suite with:

pytest



# HaMaGeoLib

## Repository

Local directory:
/home/lochy/ASPECT_PROJECT/HaMaGeoLib

Upstream:
https://github.com/lhy11009/HaMaGeoLib

Fork:
same as upstream

## Git remotes

origin:
authoritative upstream, push allowed

## Development environment

Conda environment:
hmgeolib

Verify with:

conda env list
python -c "import sys; print(sys.executable)"

## Tests

Run focused tests with pytest.

Run the complete test suite with:

pytest

## Special Requirements

### Workflow for Generating ParaView Plotting Scripts

- **Base utilities:** Common utilities are maintained in `scripts/paraview_scripts/base.py`.
- **Script separation:** New plotting scripts should be created as separate files and reuse utilities defined in `base.py`, rather than duplicating existing functionality.
- **Script combination:** The contents of `base.py` and the new plotting scripts will be combined at a later stage through a user-initiated operation. **Do not combine these files during script generation.**
- **Code organization:**
  - Place reusable functions and general-purpose utilities in `base.py`.
  - Place case-specific plotting workflows, configurations, and execution logic in the new plotting scripts.
  - When developing new functionality, consider whether it should be implemented as a reusable utility in `base.py` or as part of the plotting workflow in the new script.
- **Compatibility:** Ensure that newly generated scripts remain compatible with the existing utilities and can be combined with `base.py` without naming conflicts or duplicated definitions.
- **Placeholder options:** Words written entirely in capital letters (e.g., `TOP`) represent placeholders that will be substituted through a later user-initiated operation. **Do not substitute these placeholders during script generation.** When instructed to add configurable options, consider introducing similar uppercase placeholders to support later substitution.



# WorldBuilder

## Repository

Local directory:
<workspace-root>/Softwares/WorldBuilder

Upstream:
https://github.com/GeodynamicWorldBuilder/WorldBuilder

Fork:
https://github.com/lhy11009/WorldBuilder

## Repository type

C++ project using CMake.

## Git remotes

origin:
authoritative upstream, read-only

lhy11009:
personal fork, push allowed

## Important directories

- `source/` — implementation
- `include/` — public/internal headers
- `tests/` — tests
- `cmake/` — CMake configuration
- `doc/` — documentation

## Explain the structures

- `source/world_builder` - files in this folder are upper-level files (e.g. main workflow, utilities)
- `source/world_builder/features` - each file in this folder is a feature (e.g. oceanic plate as oceanic_plate.cc) and each feature as their own models as seperate sub-folders (e.g. oceanic_plate_models)

## Special requriements

- After making change to this repository, before commit, execute `make indent` in the build directory.



# ASPECT

## Repository

Local directory:
/home/lochy/Softwares/aspect

Upstream:
https://github.com/geodynamics/aspect

Fork:
https://github.com/lhy11009/aspect

Local stable deal.ii repository:
/home/lochy/Softwares/Deal.ii-9.7.0-Native-32bits-candi-gcc-12.4.0-openmpi-4.1.6

## Repository type

C++ project using CMake.

## Git remotes

origin:
authoritative upstream, read-only

lhy11009:
personal fork, push allowed

## Important directories

- `source/` — implementation
- `include/` — public/internal headers
- `tests/` — tests
- `cmake/` — CMake configuration
- `doc/` — documentation

## Explain the structures

- `source/` - files in this folder are upper-level files (e.g. main workflow, utilities)
- `source/<sub-folder>` - each subfolder is a plugin system (e.g. material model). They have their respective interface and instance of plugins.

## Development environment

None

## Indentation & Parameters

Code indentation can be applied using:

```bash
make indent
```

Code parameters can be updated by:`

```bash
make parameters
```

## Tests

For every new test, there must be a reference-data directory with the same name under the test folder.

At a minimum, the reference-data directory must contain a `screen-output` file.

Tests are enabled using this in the build directory:

```bash
make setup_tests
```

To generate standard output of a test, use this command in the build directory:

```bash
ASPECT_GENERATE_REFERENCE_OUTPUT=1 ctest -R <test_name>
```

# codex_workflows_geodynamics

## Repository

Local directory:
/home/lochy/Desktop/codex_workflows_geodynamics

Upstream:
https://github.com/lhy11009/codex_workflows_geodynamics

Fork:
None; just use the upstream

## Git remotes

origin:
authoritative upstream, as well as personal fork, push allowed

## Development environment

Conda environment:
Sub-folders have different conda environment. Check their README files.

## Tests

Look into the tests defined in the sub-folders.

# fastscape

## Repository

Local directory:
/home/lochy/Softwares/fastscape/fastscapelib-fortran

Upstream:
https://github.com/Djneu/fastscapelib-fortran

Fork:
https://github.com/lhy11009/fastscapelib-fortran


## Repository type

fortran project using CMake.

## Git remotes

origin:
authoritative upstream, read-only

lhy11009:
personal fork, push allowed