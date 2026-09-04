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
<workspace-root>/Softwares/HaMaGeoLib

Upstream:
https://github.com/lhy11009/HaMaGeoLib

Fork:
same as upstream

## Git remotes

origin:
authoritative upstream, read-only

lhy11009:
personal fork, push allowed

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

## Development environment

None

## Tests

None



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

## Indentation

Code indentation can be applied using:

```bash
make indent
```

## Tests

For every new test, there must be a reference-data directory with the same name under the test folder.

At a minimum, the reference-data directory must contain a `screen-output` file.

Tests are built using:

```bash
make setup_tests
```
