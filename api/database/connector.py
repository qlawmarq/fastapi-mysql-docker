from fastapi import HTTPException, status
import os
import pymysql.cursors
from pymysql import converters


class DatabaseConnector:
    def __init__(self):
        self.host = os.getenv("DATABASE_HOST")
        self.user = os.getenv("DATABASE_USERNAME")
        self.password = os.getenv("DATABASE_PASSWORD")
        self.database = os.getenv("DATABASE")
        self.port = int(os.getenv("DATABASE_PORT"))
        self.conversions = converters.conversions
        self.conversions[pymysql.FIELD_TYPE.BIT] = (
            lambda x: False if x == b"\x00" else True
        )
        if not self.host:
            raise EnvironmentError("DATABASE_HOST environment variable not found")
        if not self.user:
            raise EnvironmentError("DATABASE_USERNAME environment variable not found")
        if not self.password:
            raise EnvironmentError("DATABASE_PASSWORD environment variable not found")
        if not self.database:
            raise EnvironmentError("DATABASE environment variable not found")

    def get_connection(self):
        connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor,
            conv=self.conversions,
        )
        return connection

    def query_get(self, sql, param):
        try:
            connection = self.get_connection()
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql, param)
                    return cursor.fetchall()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error: " + str(e),
            )

    def query_put(self, sql, param):
        try:
            connection = self.get_connection()
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql, param)
                    connection.commit()
                    return cursor.lastrowid
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error: " + str(e),
            )
