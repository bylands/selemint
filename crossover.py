import pandas as pd
import numpy as np
import random
from numpy.random import default_rng
import calculate_fitness

rng = default_rng()

rate = 0.02

def get_offspring(pool: dict, choices_df: pd.DataFrame, blocks, n_genes: int, multipliers: list[float]) -> dict:
    
    pool_keys = list(pool.keys())
    block_names = [block for block in blocks.keys()]
    n_people = len(pool[pool_keys[0]][0])

    offsprings = {}

    for i in range(n_genes):
        id = f'GID{i:05}'

        while True:
            key1, key2 = random.sample(pool_keys, k = 2)
            off1, off2 = pool[key1], pool[key2]

            pos = rng.integers(n_people)
            off_df1 = off1[0][:pos]
            off_df2 = off2[0][pos:]

            off_df = pd.concat([off_df1, off_df2])
            fitness = calculate_fitness.calc_fitness(choices_df, off_df, blocks, block_names, multipliers)
            if fitness > 0:
                break

        while True:
            for block in blocks:
                options = list(blocks[block].keys())
                random_value = rng.random(size=n_people)
                off_df[f'{block}'] = (np.where(random_value < rate, random.choice(options), off_df[f'{block}']))
            
            fitness = calculate_fitness.calc_fitness(choices_df, off_df, blocks, block_names, multipliers)
            if fitness > 0:
                break

        offsprings[id] = [off_df, fitness]

    return offsprings    