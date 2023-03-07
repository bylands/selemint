import numpy as np
import pandas as pd

# calculate fitness

def calc_fitness(choices_df:pd.DataFrame, gene_df: pd.DataFrame, block_names, multipliers: list[float]) -> float:

    counter = [0, 0, 0]

    for block in block_names:
        counter[0] = ((choices_df[f'{block}_first_choice'] == gene_df[f'{block}']) * choices_df['total_score']).sum()

        for c, g, s in zip(choices_df[f'{block}_second_choices'], gene_df[f'{block}'], choices_df['total_score']):
            if g in c:
                counter[1] += s

        for c, g, s in zip(choices_df[f'{block}_third_choices'], gene_df[f'{block}'], choices_df['total_score']):
            if g in c:
                counter[2] += s

    return np.array([c * m for c, m in zip(counter, multipliers)]).sum()
