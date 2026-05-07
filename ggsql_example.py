import marimo

__generated_with = "0.23.5"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo

    return


@app.cell
def _():
    import polars as pl
    import pyarrow as pa
    import ggsql

    return ggsql, pa


@app.cell
def _(ggsql, pa):
    # Create a table
    table = pa.table({
        "x": [1, 2, 3, 4, 5],
        "y": [10, 20, 15, 30, 25],
        "category": ["A", "B", "A", "B", "A"]
    })

    # Render to Altair chart
    chart = ggsql.render_altair(table, "VISUALISE x, y DRAW point")

    # Display or save
    chart.display()  # In Jupyter
    return


if __name__ == "__main__":
    app.run()
