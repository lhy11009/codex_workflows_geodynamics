# Local Projects

This file defines the locations of local projects used by the geodynamics workflows.

Paths in this file are machine-specific.

`local` refers to my workstation. The SSH alias for `local` is always `ucd`.

For example, when connecting to `local` from another machine (e.g., a laptop), use:

```bash
ssh ucd
```

## MOW

### Local

Project directory:

`/mnt/lochy/ASPECT_DATA/MOW`

ASPECT branch:

`master_TwoD_rebase`

ASPECT build:

`/home/lochy/Softwares/aspect/build_master_TwoD_rebase`

### Build and test

- Tests on this branch has to run in release mode.
- Tests started with name of `TwoDSubduction_` and `MOW_` are tests specifically designed for this project.
- When creating new test for this project, make sure the test name starts with `MOW_`.

Below is an example of bash script.

```bash
/home/lochy/ASPECT_PROJECT/HaMaGeoLib/scripts/bash_scripts/build_aspect.sh master_TwoD_rebase --mode release -j 2
cd /home/lochy/Softwares/aspect/build_master_TwoD_rebase
make setup_tests
ctest --output-on-failure -j2 -R '^TwoDSubduction_'
```

### Stampede3 (remote)

Project directory:

`/scratch/06806/hyli/MOW`

## Collision

### Local

Project directory:

`/mnt/lochy/ASPECT_DATA/Collision0`

ASPECT branch:

`main_collision`

ASPECT build:

`/home/lochy/Softwares/aspect/build_main_collision`

HaMaGeoLib main notebook:

`notebooks/research/haoyuan_collision/Collision.ipynb`

HaMaGeoLib tests:

`tests/research/haoyuan_collision`

### Hive (remote)

Project directory:

`/quobyte/billengrp/lochy/Collision0`

### Stampede3 (remote)

Project directory:

`/scratch/06806/hyli/Collision0`

### Project-specific Workflow

None

### Stampede3 (remote)

Project directory:

`/scratch/06806/hyli/MOW`


## Prescribe velocity

### Local

Project directory:

`/mnt/lochy/ASPECT_DATA/prescribe_velocity`

ASPECT branch:

`world_builder_prescribed_solution`

ASPECT build:

`/home/lochy/Softwares/aspect/build_world_builder_prescribed_solution`

HaMaGeoLib main notebook:

`notebooks/research/prescribe_velocity/PrescribeVelocity.ipynb`

HaMaGeoLib tests:

`tests/research/prescribe_velocity`

### Hive (remote)

Project directory:

`/quobyte/billengrp/lochy/prescribe_velocity`

### Stampede3 (remote)

Project directory:

`/scratch/06806/hyli/prescribe_velocity`

### Project-specific Workflow

None


## Literature

### Local

literature directory:

`/home/lochy/Documents/papers`

markdown directory:

`/home/lochy/Documents/papers/markdown_summary`

json path for extracting summaries:

`/home/lochy/Documents/papers/markdown_summary/summary.jsonl`

unmatched output path for extracting summaries:

`/home/lochy/Documents/papers/markdown_summary/match_report.json`

bibliography files:

`/home/lochy/Documents/papers/bib/codex.bib`

and

`/home/lochy/Documents/papers/bib/myref1.bib`
