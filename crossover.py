import pandas as pd
import random
from numpy.random import default_rng
import calculate_fitness

rng = default_rng()

def get_offspring(pool: dict, choices_fd: pd.DataFrame, options: list[str], n_genes: int,
                  multipliers: list[float], counter: list[float]) -> dict:
    
    pool_keys = list(pool.keys())
    n_people = len(pool[pool_keys[0]][0])

    offsprings = {}

    for i in range(n_genes):
        id = f'GID{i:05}'
        key1, key2 = random.sample(pool_keys, k = 2)
        off1, off2 = pool[key1], pool[key2]

        pos = rng.integers(n_people)
        off_fd1 = off1[0][:pos]
        off_fd2 = off2[0][pos:]

        off_fd = pd.concat([off_fd1, off_fd2])
        fitness = calculate_fitness.calc_fitness(choices_fd, off_fd, options, n_people, multipliers, counter)

        offsprings[id] = [off_fd, fitness]

    return offsprings
