import psycopg2

from typing import List
from .data import MetricOutput, ChainOutput
from .device import Device


class Database(Device):
    """Class to manage database access"""

    def __init__(
        self,
        dbname: str,
        table: str,
        user: str,
        password: str,
        host: str = "localhost",
        port: int = 5432,
        reset: bool = False
    ) -> None:
        self.table_metrics = table
        self.table_chains = f"{table}_chains"

        try:
            self.conn = psycopg2.connect(
                dbname=dbname, user=user, password=password, host=host, port=port
            )
            self.cur = self.conn.cursor()
        except Exception:
            print("Error connecting to the database")

        if reset:
            self.__delete_table_metrics()
            self.__delete_table_chains()
            
        self.__create_table_metrics()
        self.__create_table_chains()

    def __create_table_metrics(self):
        query = f"""CREATE TABLE IF NOT EXISTS {self.table_metrics} (
            block_id text,
            metric_name text,
            year_month text,
            abs_actual_value real,
            rel_actual_value real,
            abs_cumulative_value real,
            rel_cumulative_value real,
            PRIMARY KEY (block_id, metric_name, year_month)
        )"""
        self.cur.execute(query)
        self.conn.commit()
    
    def __create_table_chains(self):
        query = f"""CREATE TABLE IF NOT EXISTS {self.table_chains} (
            id SERIAL PRIMARY KEY,
            first Text,
            second Text,
            year_month Text,
            timestamp_begin TIMESTAMP,
            timestamp_end TIMESTAMP,
            duration_sec bigint,
            length bigint
        )"""
        self.cur.execute(query)
        self.conn.commit()

    def __delete_table_metrics(self):
        query = f"""
            DROP TABLE IF EXISTS {self.table_metrics};
        """
        self.cur.execute(query)
        self.conn.commit()

    def __delete_table_chains(self):
        query = f"""
            DROP TABLE IF EXISTS {self.table_chains};
        """
        self.cur.execute(query)
        self.conn.commit()

    def send_metric_data(self, data: List[MetricOutput]):
        try:
            self.cur.executemany(
                f"INSERT INTO {self.table_metrics} VALUES (%s, %s, %s, %s, %s, %s, %s)",
                map(MetricOutput.unpack, data),
            )
            self.conn.commit()
        except Exception:
            print("Error saving metric data to the database")

    def send_chain_data(self, data: List[ChainOutput]):
        try:
            self.cur.executemany(
                f"INSERT INTO {self.table_chains} VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s)",
                map(ChainOutput.unpack, data),
            )
            self.conn.commit()
        except Exception:
            print("Error saving chain data to the database")

    def close(self):
        self.conn.close()
