import random

def get_mating_pool(genes:dict, frac_elite: float, frac_lucky: float) -> dict:

    n_genes = len(genes)

    genes_ids_sorted = list(dict(sorted(genes.items(), key=lambda item: item[1][1], reverse=True)).keys())

    elite_ids = genes_ids_sorted[:int(frac_elite * n_genes)]
    pool = {id: genes[id] for id in elite_ids}

    lucky_ids = random.sample(genes_ids_sorted[int(frac_elite * n_genes):], k=int(frac_lucky * n_genes))
    pool.update({id: genes[id] for id in lucky_ids})

    return pool

def get_best(genes:dict, n):
    return list(dict(sorted(genes.items(), key=lambda item: item[1][1], reverse=True)))[:n]