from dagster import asset, Config
from dagster_duckdb import DuckDBResource

from ..fakerapi import get_faker_data
from . import constants

import pandas as pd


@asset
def faker_companies_file():
    raw_companies_data = get_faker_data(resource="companies", quantity=100)
    df = pd.DataFrame.from_dict(raw_companies_data, orient="columns")
    df.to_csv(constants.FAKER_COMPANY_RAW_FILE_PATH)


@asset(deps=["faker_companies_file"])
def faker_companies(database: DuckDBResource):
    create_table_query = """
        CREATE TABLE IF NOT EXISTS
            faker_companies (
                id integer,
                name varchar,
                email varchar,
                vat BIGINT,
                phone varchar,
                country varchar,
                addresses varchar,
                website varchar,
                image varchar,
                contact varchar
            );
    """

    insert_query = f"""
        INSERT INTO faker_companies
        SELECT 
            id,
            name,
            email,
            vat,
            phone,
            country,
            addresses,
            website,
            image,
            contact        
        FROM '{constants.FAKER_COMPANY_RAW_FILE_PATH}';
    """

    with database.get_connection() as conn:
        conn.execute(create_table_query)
        conn.execute(insert_query)
