# -*- coding: utf-8 -*-

from psycopg2 import pool

from dbsession import DBConnection

POSTGRES_HOST = "host"
POSTGRES_PORT = "port"
POSTGRES_USER = "user"
POSTGRES_PASSWORD = "pass"
POSTGRES_DB = "db"

MINIMUM_CONNECTION = 1
MAXIMUM_CONNECTION = 50

connection_pool = pool.ThreadedConnectionPool(
    MINIMUM_CONNECTION,
    MAXIMUM_CONNECTION,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DB)


db_connection = DBConnection(connection_pool)
