from dataclasses import dataclass
from typing import List
import datetime

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

@dataclass
class ChainDB:
    """Class for keeping track of a metric in the database"""

    first: str
    second: str
    year_month: str
    timestamp_begin: datetime.datetime
    timestamp_end: datetime.datetime
    duration_sec: int
    length: int

    def unpack(self):
        return (
            self.first,
            self.second,
            self.year_month,
            self.timestamp_begin,
            self.timestamp_end,
            self.duration_sec,
            self.length,
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

    def send_metric_data(self, data: List[MetricDB]):
        try:
            self.cur.executemany(
                f"INSERT INTO {self.table_metrics} VALUES (%s, %s, %s, %s, %s, %s, %s)",
                map(MetricDB.unpack, data),
            )
            self.conn.commit()
        except Exception:
            print("Error saving metric data to the database")

    def send_chain_data(self, data: List[ChainDB]):
        try:
            self.cur.executemany(
                f"INSERT INTO {self.table_chains} VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s)",
                map(ChainDB.unpack, data),
            )
            self.conn.commit()
        except Exception:
            print("Error saving chain data to the database")

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
        self.database.send_metric_data(self.buffer)
        self.clean()


class BufferChainDB:
    def __init__(self, max_size: int, database: Database) -> None:
        self.buffer: List[ChainDB] = []
        self.max_size = max_size
        self.database = database

    def __len__(self):
        return len(self.buffer)

    def clean(self):
        self.buffer.clear()

    def extend(self, chains: List[ChainDB]):
        self.buffer.extend(chains)

        if len(self.buffer) > self.max_size:
            self.flush()

    def flush(self):
        self.database.send_chain_data(self.buffer)
        self.clean()
