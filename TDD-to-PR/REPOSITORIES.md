# gdmate

## Repository

Local directory:
<workspace-root>/Softwares/gdmate

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