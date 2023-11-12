import json


def get_data(fn: str) -> dict:
    """
    import data from json file and return dictionary
    """

    with open(fn) as f:
        d = json.load(f)

    return d