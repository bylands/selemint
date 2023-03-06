import numpy as np
import pandas as pd

# calculate fitness

def calc_fitness(choices_df:pd.DataFrame, gene_df: pd.DataFrame, multipliers: list[float]) -> float:

    # n_options = len(options)

    # opt_slots = {option: 1.5 * n_people//n_options for option in options if gene_fd['module'].eq(option).any()}
    # if any([gene_fd.value_counts()[option] > opt_slots[option] for option in options]):
    #     return 0

    counter = [0, 0, 0]

    counter[0] = ((choices_df['first_choice'] == gene_df['module']) * choices_df['score']).sum()

    for c, g, s in zip(choices_df['second_choices'], gene_df['module'], choices_df['score']):
        if g in c:
            counter[1] += s

    for c, g, s in zip(choices_df['third_choices'], gene_df['module'], choices_df['score']):
        if g in c:
            counter[2] += s

    return np.array([c * m for c, m in zip(counter, multipliers)]).sum()
