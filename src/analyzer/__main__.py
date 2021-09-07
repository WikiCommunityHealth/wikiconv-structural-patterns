import gzip
import json
import time
from typing import Any, Dict, Generator, List

from tqdm import tqdm

from . import utils
from .metrics import MetricController, Record
from .parser import *


def process_file(
    file_path: str, input_compression: str, configs: Dict[str, Any]
) -> None:
    if not input_compression:
        with open(file_path) as file:
            process_lines((line for line in file), configs)
    elif input_compression == "gzip":
        with gzip.open(file_path, mode="rt", newline="\n") as file:
            process_lines((line for line in file), configs)


def process_lines(lines: Generator[str, None, None], configs: Dict[str, Any]) -> None:
    records: Generator[Dict[str, Any], None, None] = (
        json.loads(line.split("\t")[1], object_hook=utils.date_hook) for line in lines
    )

    target_field = configs["general"]["target_field"]
    filter_user_pages = configs["general"]["filter_user_pages"]

    controller = MetricController(configs)
    record_buffer: List[Record] = []

    previous_line_block_id = ""
    is_new_discussion_page = True

    for record in records:
        if filter_user_pages and record["pageNamespace"] == 3:
            continue

        is_new_discussion_page = previous_line_block_id != record[target_field]

        if is_new_discussion_page and previous_line_block_id != -1:
            # save result from previous discussione page to db
            controller.calculate_metrics_for_block(
                record_buffer, previous_line_block_id
            )
            record_buffer.clear()

        record_buffer.append(record)
        previous_line_block_id = record[target_field]

    # calculate metrics for the last block
    controller.calculate_metrics_for_block(record_buffer, previous_line_block_id)
    controller.flush()
    controller.close()


if __name__ == "__main__":
    args = parse_arguments()
    configs = parse_configs(args.config)
    print(configs)

    now = time.perf_counter()
    for file_path in tqdm(args.files):
        process_file(file_path, args.compression, configs)

        if "json" in configs and "reset" in configs["json"]:
            configs["json"]["reset"] = False

        if "database" in configs and "reset" in configs["database"]:
            configs["database"]["reset"] = False

    print(f"Elapsed time: {time.perf_counter() - now}")
