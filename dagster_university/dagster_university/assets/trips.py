import requests

from dagster_duckdb import DuckDBResource
from . import constants
from ..partitions import monthly_partition
from dagster import asset


@asset(partitions_def=monthly_partition)
def taxi_trips_file(context):
    """
    The raw parquet files for the taxi trips dataset. Sourced from the NYC Open Data portal.
    """

    partition_date_str = context.asset_partition_key_for_output()
    month_to_fetch = partition_date_str[:-3]

    raw_trips = requests.get(
        f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{month_to_fetch}.parquet"
    )

    with open(
        constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(month_to_fetch), "wb"
    ) as output_file:
        output_file.write(raw_trips.content)


@asset
def taxi_zones_file():
    """
    The raw parquet files for the taxi zones dataset. Sourced from the NYC Open Data portal.
    """
    month_to_fetch = "2023-03"
    raw_taxi_zones = requests.get(
        f"https://data.cityofnewyork.us/api/views/755u-8jsi/rows.csv?accessType=DOWNLOAD"
    )

    with open(constants.TAXI_ZONES_FILE_PATH, "wb") as output_file:
        output_file.write(raw_taxi_zones.content)


@asset(deps=["taxi_trips_file"], partitions_def=monthly_partition)
def taxi_trips(context, database: DuckDBResource):
    """
    The raw taxi trips dataset, loaded into a DuckDB database
    """

    partition_date_str = context.asset_partition_key_for_output()
    month_to_fetch = partition_date_str[:-3]
    context.log.info(f"month_to_fetch: {month_to_fetch}")

    create_table_query = """
            CREATE TABLE IF NOT EXISTS
                trips (
                    vendor_id integer,
                    pickup_zone_id integer,
                    dropoff_zone_id integer,
                    rate_code_id double,
                    payment_type integer,
                    dropoff_datetime timestamp,
                    pickup_datetime timestamp,
                    trip_distance double,
                    passenger_count double,
                    total_amount double,
                    partition_date varchar
                );
        """

    delete_partition_query = f"""
        DELETE FROM trips
        WHERE partition_date = '{month_to_fetch}';
    """

    insert_partition_query = f"""
        INSERT INTO trips
        SELECT
            VendorID AS vendor_id,
            PULocationID AS pickup_zone_id,
            DOLocationID AS dropoff_zone_id,
            RatecodeID AS rate_code_id,
            payment_type AS payment_type,
            tpep_dropoff_datetime AS dropoff_datetime,
            tpep_pickup_datetime AS pickup_datetime,
            trip_distance AS trip_distance,
            passenger_count AS passenger_count,
            total_amount AS total_amount,
            '{month_to_fetch}' AS partition_date
        FROM '{constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(month_to_fetch)}';
    """

    with database.get_connection() as conn:
        conn.execute(create_table_query)
        conn.execute(delete_partition_query)
        conn.execute(insert_partition_query)


@asset(deps=["taxi_zones_file"])
def taxi_zones(database: DuckDBResource):
    """
    The raw taxi zones dataset, loaded into a DuckDB database
    """
    sql_query = f"""
        CREATE OR REPLACE TABLE zones AS (
            SELECT
                LocationId AS zone_id,
                zone,
                borough,
                the_geom AS geometry
            FROM '{constants.TAXI_ZONES_FILE_PATH}'
        );
    """

    with database.get_connection() as conn:
        conn.execute(sql_query)
