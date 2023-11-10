from dagster import resource, Field
from sqlalchemy import create_engine


@resource({
    "username": Field(str, is_required=True, description="The username for the Cloud SQL database."),
    "password": Field(str, is_required=True, description="The password for the Cloud SQL database."),
    "database": Field(str, is_required=True, description="The name of the database to connect to."),
    "instance_connection_name": Field(str, is_required=True,
                                      description="The connection name of the Cloud SQL instance."),
})
def cloud_sql_resource(context):
    db_user = context.resource_config["username"]
    db_pass = context.resource_config["password"]
    db_name = context.resource_config["database"]
    instance_name = context.resource_config["instance_connection_name"]

    # For Cloud SQL, use the dbapi connection string format provided by GCP documentation
    # Example: "postgresql+pg8000://<db_user>:<db_pass>@/<db_name>?unix_sock=/cloudsql/<instance_connection_name>/.s.PGSQL.5432"
    db_connection_string = f"postgresql+pg8000://{db_user}:{db_pass}@/{db_name}?unix_sock=/cloudsql/{instance_name}/.s.PGSQL.5432"

    engine = create_engine(db_connection_string)
    return engine
