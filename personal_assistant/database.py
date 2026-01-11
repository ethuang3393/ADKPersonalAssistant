# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Database connection and schema for the Checkmate agent."""

import os
import sqlalchemy
from google.cloud.sql.connector import Connector
from sqlalchemy import (
    create_engine,
    Table,
    Column,
    String,
    MetaData,
    Boolean,
    ForeignKey,
)

def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL for PostgreSQL instance.

    Uses the Cloud SQL Python Connector package.
    """
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager to help keep secrets safe.
    instance_connection_name = os.environ["DB_INSTANCE_CONNECTION_NAME"]
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]

    connector = Connector()

    def getconn() -> sqlalchemy.engine.base.Connection:
        conn = connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
        )
        return conn

    engine = create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )
    inspector = sqlalchemy.inspect(engine)
    if not inspector.has_table("users"):
        create_tables(engine)
    return engine


metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("user_id", String, primary_key=True),
    Column("user_name", String),
)

todolists = Table(
    "todolists",
    metadata,
    Column("list_id", String, primary_key=True),
    Column("user_id", String, ForeignKey("users.user_id")),
    Column("list_name", String),
)

tasks = Table(
    "tasks",
    metadata,
    Column("task_id", String, primary_key=True),
    Column("list_id", String, ForeignKey("todolists.list_id")),
    Column("task_description", String),
    Column("is_completed", Boolean),
)

stashed_urls = Table(
    "stashed_urls",
    metadata,
    Column("url_id", String, primary_key=True),
    Column("user_id", String, ForeignKey("users.user_id")),
    Column("url", String),
    Column("summary", String),
    Column("tags", String),
)

def create_tables(engine: sqlalchemy.engine.base.Engine):
    metadata.create_all(engine)
