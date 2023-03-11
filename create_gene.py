import pandas as pd
import random
from itertools import chain


def get_gene(blocks: list[str], n_people: int) -> pd.DataFrame:

    dict = {}

    for block in blocks:

        option_list = list(chain(*[[o] * n for o, n in blocks[block].items()]))

        module_list = random.sample(option_list, k=n_people)

        dict[f'{block}'] = module_list

    return pd.DataFrame(dict)
