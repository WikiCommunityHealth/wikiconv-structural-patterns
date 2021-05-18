from dataclasses import dataclass
from typing import List

import psycopg2


@dataclass
class MetricDB:
    """Class for keeping track of a metric in the database"""

    block_id: str
    metric_name: str
    year_month: str
    abs_actual_value: float
    rel_actual_value: float
    abs_cumulative_value: float
    rel_cumulative_value: float

    def unpack(self):
        return (
            self.block_id,
            self.metric_name,
            self.year_month,
            self.abs_actual_value,
            self.rel_actual_value,
            self.abs_cumulative_value,
            self.rel_cumulative_value,
        )


class Database:
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
        self.table = table

        try:
            self.conn = psycopg2.connect(
                dbname=dbname, user=user, password=password, host=host, port=port
            )
            self.cur = self.conn.cursor()
        except Exception:
            print("Error connecting to the database")

        if reset:
            self.__delete_table()
            
        self.__create_table()

    def __create_table(self):
        query = f"""CREATE TABLE IF NOT EXISTS {self.table} (
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

    def __delete_table(self):
        query = f"""
            DROP TABLE IF EXISTS {self.table};
        """
        self.cur.execute(query)
        self.conn.commit()

    def send_data(self, data: List[MetricDB]):
        try:
            self.cur.executemany(
                f"INSERT INTO {self.table} VALUES (%s, %s, %s, %s, %s, %s, %s)",
                map(MetricDB.unpack, data),
            )
            self.conn.commit()
        except Exception:
            print("Error saving data to the database")

    def close(self):
        self.conn.close()


class BufferMetricDB:
    def __init__(self, max_size: int, database: Database) -> None:
        self.buffer: List[MetricDB] = []
        self.max_size = max_size
        self.database = database

    def __len__(self):
        return len(self.buffer)

    def clean(self):
        self.buffer.clear()

    def extend(self, metrics: List[MetricDB]):
        self.buffer.extend(metrics)

        if len(self.buffer) > self.max_size:
            self.flush()

    def flush(self):
        self.database.send_data(self.buffer)
        self.clean()
