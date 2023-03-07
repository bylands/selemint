import pandas as pd
import random
from itertools import chain


def get_gene(blocks: list[str], n_people: int) -> pd.DataFrame:

    id_list = [f'ID{i:03}' for i in range(n_people)]

    dict = {}

    for block in blocks:
        options = list(blocks[block].keys())
        slots_per_option = list(blocks[block].values())

        option_list = list(chain(*[[o] * n for o, n in zip(options, slots_per_option)]))

        module_list = random.sample(option_list, k=n_people)

        dict[f'{block}'] = module_list

    return pd.DataFrame(dict, index=id_list)
