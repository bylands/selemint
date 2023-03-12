import numpy as np
import pandas as pd

# calculate fitness

def calc_fitness(choices_df:pd.DataFrame, gene_df: pd.DataFrame, blocks, block_names, multipliers: list[float]) -> float:

    counter = [0, 0, 0]
    fitness = 0

    for block in block_names:

        counts = pd.DataFrame(gene_df[block].value_counts().sort_index())
        max_counts = pd.DataFrame({block: blocks[block].values()}, index=blocks[block].keys()).sort_index()

        if (counts[block] > max_counts[block]).any():
            return 0


        for i, level in enumerate(['first', 'seconds', 'thirds']):
            filter_col = [col for col in choices_df if col.startswith(f'{block}_{level}')]

            counter[i] = (choices_df[filter_col].isin(gene_df[block]).any(axis=1) 
                          * choices_df['total_score']).sum()

        fitness += np.array([c * m for c, m in zip(counter, multipliers)]).sum()

    return fitness
