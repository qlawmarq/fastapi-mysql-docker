import os
import pymysql.cursors
from pymysql import converters


conversions = converters.conversions
conversions[pymysql.FIELD_TYPE.BIT] = lambda x: False if x == b"\x00" else True


def init_connection():
    host = os.getenv("DATABASE_HOST")
    user = os.getenv("DATABASE_USERNAME")
    password = os.getenv("DATABASE_PASSWORD")
    database = os.getenv("DATABASE")
    if not host:
        raise EnvironmentError("DATABASE_HOST environment variable not found")
    if not user:
        raise EnvironmentError("DATABASE_USERNAME environment variable not found")
    if not password:
        raise EnvironmentError("DATABASE_PASSWORD environment variable not found")
    if not database:
        raise EnvironmentError("DATABASE environment variable not found")
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=database,
        cursorclass=pymysql.cursors.DictCursor,
        conv=conversions,
    )
    return connection


def query_get(sql, param):
    connection = init_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, param)
            return cursor.fetchall()


def query_put(sql, param):
    connection = init_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, param)
            connection.commit()
            return cursor.lastrowid


def query_update(sql, param):
    connection = init_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, param)
            connection.commit()
            return True
