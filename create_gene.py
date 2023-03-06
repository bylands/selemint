import pandas as pd
import random

def get_gene(options: list[str], n_people: int) -> pd.DataFrame:

    n_options = len(options)

    factor = int(n_people / n_options * 1.2)
    option_list = options * factor

    id_list = [f'ID{i:03}' for i in range(n_people)]

    module_list = random.sample(option_list, k=n_people)

    return pd.DataFrame({'module': module_list}, index=id_list)
