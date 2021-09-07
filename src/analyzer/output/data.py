import datetime

from dataclasses import dataclass


@dataclass
class MetricOutput:
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
class ChainOutput:
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