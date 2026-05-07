# Learning about SedonaDB, GGSQL, and a little UV

Testing out two of the latest additions to the data science space


## UV to start

[uv](https://docs.astral.sh/uv/) continues to be my favorite way to control python and create common experiences for learners and developers. Plus it is screaming fast. This repository is built to leverage a virtual Python environment using uv.

### Commands to get it set up

_These have already been done in this repo._

1. Created the repo on Github and then clones
2. `uv init .` in the base folder
3. Then add `package = false` under `[tool.uv]` in the `pyproject.toml` as this will not be a package.
4. `uv add 'marimo[edit]' "apache-sedona[db]" ggsql` to get the tools needed.

## Marimo for scripting

[marimo](https://marimo.io/) is a next generation Python notebook that has my interest lately. Once you have this repo cloned you can start marimo with the terminal command `uv run marimo edit explore.py`

## ggsql for visualization

1. `uv tool install ggsql-jupyter`
2. 


## SedonaDB with Polars for data wrangling

[SQL - Apache Sedona](https://sedona.apache.org/sedonadb/latest/reference/sql/)

[GeoArrow has spatial parquet data](https://github.com/geoarrow/geoarrow-data) that we can use.

