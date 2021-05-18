import datetime

from .metrics import Record


# this hook is also executed in nested json objects
def date_hook(json_dict: Record) -> Record:
    if "timestamp" in json_dict:
        try:
            json_dict["timestamp"] = datetime.datetime.strptime(
                str(json_dict["timestamp"]), "%Y-%m-%dT%H:%M:%SZ"
            )
            json_dict["year_month"] = get_year_month_from_timestamp(
                json_dict["timestamp"]
            )
        except Exception:
            print("Error parsing datetime in input file")

    if "indentation" in json_dict:
        json_dict["indentation"] = int(json_dict["indentation"])

    json_dict["username"] = get_username(json_dict)

    return json_dict


def get_year_month_from_timestamp(timestamp: datetime.datetime) -> str:
    return f"{timestamp.year}-{str(timestamp.month).rjust(2, '0')}"


def get_username(record: Record) -> str:
    username: str = ""
    if "user" in record and "text" in record["user"]:
        username = record["user"]["text"]
    elif "user" in record and "ip" in record["user"]:
        username = record["user"]["ip"]
    else:
        username = "??unknown??"

    return username