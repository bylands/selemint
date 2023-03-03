import numpy as np
import pandas as pd

# calculate fitness

def calc_fitness(choices_fd:pd.DataFrame, gene_fd: pd.DataFrame, options: list[str], n_people: int,
                 multipliers: list[float], counters: list[float]) -> float:

    # n_options = len(options)

    # opt_slots = {option: 1.5 * n_people//n_options for option in options if gene_fd['module'].eq(option).any()}
    # if any([gene_fd.value_counts()[option] > opt_slots[option] for option in options]):
    #     return 0


    multipliers = [10, 2, 1]

    counter = [0, 0, 0]

    counter[0] = ((choices_fd['first_choice'] == gene_fd['module']) * choices_fd['score']).sum()

    for c, g, s in zip(choices_fd['second_choices'], gene_fd['module'], choices_fd['score']):
        if g in c:
            counter[1] += s

    for c, g, s in zip(choices_fd['third_choices'], gene_fd['module'], choices_fd['score']):
        if g in c:
            counter[2] += s

    return np.sum(np.array(multipliers) * np.array(counter))
