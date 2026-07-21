import time

import click
import pandas as pd
from sqlalchemy import create_engine


@click.command()
@click.option("--pg-user", default="root", help="PostgreSQL user")
@click.option("--pg-pass", default="root", help="PostgreSQL password")
@click.option("--pg-host", default="localhost", help="PostgreSQL host")
@click.option("--pg-port", default=5432, type=int, help="PostgreSQL port")
@click.option("--pg-db", default="ny_taxi", help="PostgreSQL database name")
@click.option(
    "--target-table",
    default="yellow_taxi_data",
    help="Target table name",
)
@click.option("--year", default=2021, type=int, help="Taxi-data year")
@click.option("--month", default=1, type=int, help="Taxi-data month")
def run(
    pg_user,
    pg_pass,
    pg_host,
    pg_port,
    pg_db,
    target_table,
    year,
    month,
):
    """Download Yellow Taxi data and load it into PostgreSQL."""

    chunk_size = 100_000

    prefix = (
        "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/"
    )
    url = f"{prefix}yellow_tripdata_{year}-{month:02d}.csv.gz"

    dtype = {
        "VendorID": "Int64",
        "passenger_count": "Int64",
        "trip_distance": "float64",
        "RatecodeID": "Int64",
        "store_and_fwd_flag": "string",
        "PULocationID": "Int64",
        "DOLocationID": "Int64",
        "payment_type": "Int64",
        "fare_amount": "float64",
        "extra": "float64",
        "mta_tax": "float64",
        "tip_amount": "float64",
        "tolls_amount": "float64",
        "improvement_surcharge": "float64",
        "total_amount": "float64",
        "congestion_surcharge": "float64",
    }

    parse_dates = [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
    ]

    engine = create_engine(
        f"postgresql+psycopg://{pg_user}:{pg_pass}@"
        f"{pg_host}:{pg_port}/{pg_db}"
    )

    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunk_size,
    )

    start_time = time.time()

    for chunk_number, df_chunk in enumerate(df_iter, start=1):
        write_mode = "replace" if chunk_number == 1 else "append"

        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists=write_mode,
            index=False,
        )

        print(
            f"Chunk {chunk_number} inserted: {len(df_chunk):,} rows "
            f"({time.time() - start_time:.1f} seconds elapsed)"
        )

    print("Finished loading data into PostgreSQL.")


if __name__ == "__main__":
    run()