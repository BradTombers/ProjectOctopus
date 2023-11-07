from dagster import asset
from dagster_duckdb import DuckDBResource
from datetime import datetime, timedelta
from . import constants
from ..partitions import weekly_partition

import pandas as pd
import plotly.express as px
import plotly.io as pio
import geopandas as gpd


@asset(deps=["taxi_trips", "taxi_zones"])
def manhattan_stats(database: DuckDBResource):
    query = """
        SELECT
            zones.zone,
            zones.borough,
            zones.geometry,
            count(1) as num_trips,
        FROM trips
        LEFT JOIN zones 
            ON trips.pickup_zone_id = zones.zone_id
        WHERE borough = 'Manhattan' AND geometry IS NOT null
        GROUP BY zone, borough, geometry
    """

    with database.get_connection() as conn:
        trips_by_zone = conn.execute(query).fetch_df()

    trips_by_zone["geometry"] = gpd.GeoSeries.from_wkt(trips_by_zone["geometry"])
    trips_by_zone = gpd.GeoDataFrame(trips_by_zone)

    with open(constants.MANHATTAN_STATS_FILE_PATH, "w") as output_file:
        output_file.write(trips_by_zone.to_json())


@asset(
    deps=["manhattan_stats"],
)
def manhattan_map():
    trips_by_zone = gpd.read_file(constants.MANHATTAN_STATS_FILE_PATH)

    fig = px.choropleth_mapbox(
        trips_by_zone,
        geojson=trips_by_zone.geometry.__geo_interface__,
        locations=trips_by_zone.index,
        color="num_trips",
        color_continuous_scale="Plasma",
        mapbox_style="carto-positron",
        center={"lat": 40.758, "lon": -73.985},
        zoom=11,
        opacity=0.7,
        labels={"num_trips": "Number of Trips"},
    )

    pio.write_image(fig, constants.MANHATTAN_MAP_FILE_PATH)


@asset(deps=["taxi_trips"], partitions_def=weekly_partition)
def trips_by_week(context, database: DuckDBResource):
    partition_date_str = context.asset_partition_key_for_output()
    context.log.info(f"partition_date_str: {partition_date_str}")
    # current_date = datetime.strptime(partition_date_str, constants.DATE_FORMAT)
    # end_date =  current_date += timedelta(days=7)

    query = f"""
        SELECT
            vendor_id, total_amount, trip_distance, passenger_count
        FROM trips
        WHERE pickup_datetime >= '{partition_date_str}'
            AND pickup_datetime < '{partition_date_str}'::DATE + interval '1 week'
    """

    with database.get_connection() as conn:
        data_for_week = conn.execute(query).fetch_df()

    result = (
        data_for_week.agg(
            {
                "vendor_id": "count",
                "total_amount": "sum",
                "trip_distance": "sum",
                "passenger_count": "sum",
            }
        )
        .rename({"vendor_id": "num_trips"})
        .to_frame()
        .T
    )  # type: ignore

    result["period"] = partition_date_str

    # clean up the formatting of the dataframe
    result["num_trips"] = result["num_trips"].astype(int)
    result["passenger_count"] = result["passenger_count"].astype(int)
    result["total_amount"] = result["total_amount"].round(2).astype(float)
    result["trip_distance"] = result["trip_distance"].round(2).astype(float)
    result = result[
        ["period", "num_trips", "total_amount", "trip_distance", "passenger_count"]
    ]

    try:
        # If the file already exists, append to it, but replace the existing month's data
        existing = pd.read_csv(constants.TRIPS_BY_WEEK_FILE_PATH)
        existing = existing[existing["period"] != partition_date_str]
        existing = pd.concat([existing, result]).sort_values(by="period")
        existing.to_csv(constants.TRIPS_BY_WEEK_FILE_PATH, index=False)
    except FileNotFoundError:
        result.to_csv(constants.TRIPS_BY_WEEK_FILE_PATH, index=False)
