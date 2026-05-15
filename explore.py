import marimo

__generated_with = "0.23.5"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import polars as pl
    import pyarrow as pa
    import sedona.db
    import ggsql

    return pl, sedona


@app.cell
def _(sedona):
    sd = sedona.db.connect()
    sd.options.interactive = True
    sd.options.memory_limit = "6gb"
    sd.options.memory_pool_type = "fair"
    sd.options.unspillable_reserve_ratio = 0.4
    sd.options.temp_dir = "/tmp/sedona-spill"
    return (sd,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Read Spatial Parquet and Store in View

    We have to go through the Extract, Transform, and Load (ETL) process to get our data into the correct format to use with SedonaDB and Polars.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Starting with Sedona
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Extract Data

    The `sd` context we created has a `.read_parquet()` method that allows us to read in parquet files from the web. These three files are from Github.
    """)
    return


@app.cell
def _(sd):
    cities = sd.read_parquet(
        "https://raw.githubusercontent.com/geoarrow/geoarrow-data/v0.2.0/natural-earth/files/natural-earth_cities_geo.parquet")
    countries = sd.read_parquet(
        "https://raw.githubusercontent.com/geoarrow/geoarrow-data/v0.2.0/natural-earth/files/natural-earth_countries_geo.parquet"
    )
    return cities, countries


@app.cell
def _(cities, countries):
    countries.to_view("countries", overwrite=True)
    cities.to_view("cities", overwrite=True)
    return


@app.cell
def _(cities):
    print(cities.count())
    cities.show()
    return


@app.cell
def _(countries):
    print(countries.count())
    countries.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Transform Data

    Now we need to perform some minor transformations to ensure;
    - the two tables will not have duplicate column names after our join. Also, our columns have descriptive names to provide context.
    - we have the right columns for data handling in Polars. Polars can't currently handle geometry-type columns well. [`ST_AsText()`](https://sedona.apache.org/sedonadb/latest/reference/sql/st_astext/) returns the Well-Known Text string representation of a geometry or geography. [`ST_X()`](https://sedona.apache.org/sedonadb/latest/reference/sql/st_x/) returns the X coordinate of the point, or NULL if not available and `ST_Y()` does the same for the y coordinate.

    _Note 1: I can't figure out a cleaner way to method-chain these processes. I am agitated that I can't do `sql` methods on the object in Python._
    _Note 2: The [SedonaDB SQL methods](https://sedona.apache.org/sedonadb/latest/reference/sql/) cover most of the use cases I have always wanted access to for spatial data._
    """)
    return


@app.cell
def _(sd):
    cities_new_names = sd.sql("""
    SELECT name as city_name, 
        geometry as city_geometry,
        ST_AsText(geometry) AS city_wkt_geometry,
        ST_X(geometry) AS city_x,
        ST_Y(geometry) AS city_y
    FROM cities
    """)
    countries_new_names = sd.sql("""
    SELECT name as country_name,
        geometry as country_geometry,
        ST_AsText(geometry) AS country_wkt_geometry
    FROM countries
    """)
    return cities_new_names, countries_new_names


@app.cell
def _(cities_new_names):
    cities_new_names.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Load Data
    """)
    return


@app.cell
def _(cities_new_names, countries_new_names):
    cities_new_names.to_view("cities", overwrite=True)
    countries_new_names.to_view("countries", overwrite=True)
    return


@app.cell
def _(sd):
    # join the cities and countries tables
    dat_joined = sd.sql("""
    select * from cities
    join countries
    where ST_Intersects(cities.city_geometry, countries.country_geometry)
    """)
    dat_joined.to_view('dat_joined')
    dat_joined.show()
    return (dat_joined,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### SedonaDB to Polars

    SedonaDB doesn't have a `.to_polars()` method. However, we can use `.to_arrow_table()` and then use polar's `pl.from_arrow()` function to get the data into polars.

    - _Note 1: Notice in an above chunk the `ST_AsText(geometry)` funtion in the SQL code. This get's the spatial values in a format that polars can handle. The geometry typed columns are not currently handled by polars. Also the next code chunk will show a warning `sys:1: UserWarning: Extension type 'geoarrow.wkb' is not registered; loading as its storage type.` that can be ignored._
    """)
    return


@app.cell
def _(dat_joined, pl):
    dat_arrow = dat_joined.to_arrow_table()
    dat_polars = pl.from_arrow(dat_arrow)
    return (dat_polars,)


@app.cell
def _(dat_polars):
    dat_polars.limit(5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Polars to SedonaDB

    SedonaDB can handled a polars DataFrame for ther `sd.create_data_frame()` function.

    _Note 1: Notice that the binary columns in Polars render correctly in in the SedonaDB DataFrame._
    _Note 2:
    """)
    return


@app.cell
def _(dat_polars, sd):
    df_from_polars = sd.create_data_frame(dat_polars)
    df_from_polars.schema
    return (df_from_polars,)


@app.cell
def _(df_from_polars):
    df_from_polars.to_view('dat_joined_polars')
    return


@app.cell
def _(sd):
    sd.sql('SELECT * FROM dat_joined_polars').show()
    return


@app.cell
def _(df_from_polars):
    df_from_polars.to_parquet(path="joined_df.parquet")
    return


@app.cell
def _(sd):
    joined_df = sd.read_parquet(
        "joined_df.parquet"
    )
    return (joined_df,)


@app.cell
def _(joined_df):
    joined_df.limit(10).show()
    return


if __name__ == "__main__":
    app.run()
