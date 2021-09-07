import argparse
import toml


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", help="dataset file to analyze", nargs="+", type=str)
    parser.add_argument("config", help="toml config file", type=str)
    parser.add_argument(
        "-c",
        "--compression",
        help="compression used for input files",
        type=str,
        choices=[None, "gzip"],
    )

    return parser.parse_args()


def parse_configs(config_path: str):
    config = None

    try:
        with open(config_path, "r") as file:
            toml_data = "\n".join(file.readlines())
            config = toml.loads(toml_data)
    except Exception:
        print("Error config file")
    
    return config
