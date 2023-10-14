import json


def get_data(fn: str) -> dict:
    with open(fn) as f:
        d = json.load(f)

    return d