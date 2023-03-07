import pandas as pd
from numpy.random import default_rng
import random

rng = default_rng()

def get_choices(blocks: list[str], n_people: int) -> pd.DataFrame:
    weights = [3, 2, 1]
    id_list = [f'ID{i:03}' for i in range(n_people)]

    dict = {}

    for block in blocks:
        options = list(blocks[block].keys())
        n_options = len(options)

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

        dict[f'{block}_first_choice'] = first_list
        dict[f'{block}_second_choices'] = second_list
        dict[f'{block}_third_choices'] = third_list
        dict[f'{block}_score'] = score_list

    total_score = [0] * n_people

    for block in blocks:
        for i, score in enumerate(dict[f'{block}_score']):
            total_score[i] += score

    dict['total_score'] = total_score

    return pd.DataFrame(dict, index=id_list)