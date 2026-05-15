# Learning about SedonaDB, GGSQL, and a little UV

Testing out two of the latest additions to the data science space


## Getting Started

You should be able to clone this repository or [download](https://github.com/quickskilling/sedonadb_polars_python/archive/refs/heads/main.zip) the zip file and run the example script to get started in Marimo with the right packages.

1. Install [uv](https://github.com/astral-sh/uv#installation).
2. Once you are in the folder in Terminal with uv installed run the command `uv run marimo edit explore.py`.
3. You should see a list of Python packages being installed then your browser should pop open with a marimo script running.


## Some notes on how we set up the repository

### UV to start

[uv](https://docs.astral.sh/uv/) continues to be my favorite way to control python and create common experiences for learners and developers. Plus it is screaming fast. This repository is built to leverage a virtual Python environment using uv.

#### Commands to get it set up

_These have already been done in this repo._

1. Created the repo on Github and then clones
2. `uv init .` in the base folder
3. Then add `package = false` under `[tool.uv]` in the `pyproject.toml` as this will not be a package.
4. No run the following two uv commands in terminal
  ```bash
  uv add \
  "apache-sedona[db]>=1.9.0" \
  "marimo[edit,recommended]>=0.23.5" \
  "nbformat>=5.10.4" \
  "python-lsp-server>=1.14.0" \
  "ruff>=0.15.12" \
  "sedona>=1.0.4" \
  "vl-convert-python>=1.9.0.post1"
  ```

  ```bash
  uv add --group dev "jupyter>=1.1.1" "pyyaml>=6.0.3"
  ```

### Marimo for scripting

[marimo](https://marimo.io/) is a next generation Python notebook that has my interest lately. Once you have this repo cloned you can start marimo with the terminal command `uv run marimo edit explore.py`


### SedonaDB with Polars for data wrangling

- [SQL - Apache Sedona](https://sedona.apache.org/sedonadb/latest/reference/sql/)
- [GeoArrow has spatial parquet data](https://github.com/geoarrow/geoarrow-data) that we can use.

