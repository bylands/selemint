import pandas as pd
from numpy.random import default_rng
import random

rng = default_rng()

def get_choices(options: list[str], n_people: int) -> pd.DataFrame:

    n_options = len(options)
    weights = [3, 2, 1]

    id_list = [f'ID{i:03}' for i in range(n_people)]
    first_list = []
    second_list = []
    third_list = []
    score_list = []

    for i in range(n_people):
        n2 = rng.integers(n_options)
        n3 = rng.integers(n_options)

        first = random.choice(options)
        seconds = random.sample(options, k=n2)
        thirds = random.sample(options, k=n3)

        if first in seconds:
            seconds.remove(first)

        first_seconds = set(seconds).union([first])
        for item in first_seconds:
            if item in thirds:
                thirds.remove(item)

        first_list.append(first)
        second_list.append(seconds)
        third_list.append(thirds)

        score_list.append(weights[0] * int(first != 0) + weights[1] * len(seconds) + weights[2] * len(thirds))

    dict = {'first_choice': first_list, 'second_choices': second_list, 'third_choices': third_list, 'score': score_list}
    return pd.DataFrame(dict, index=id_list)