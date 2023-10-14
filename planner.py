from copy import deepcopy
from random import choice, random


def get_try(block: dict, block_nr: int, students: dict, fac1=100, fac2=50, fac3=20):

    try_block = deepcopy(block)
    block_key = 'block'+str(block_nr)

    students = sorted(students, 
                        key=lambda x: x[block_key]['weight']+random(), 
                        reverse=True)

    for student in students:
        block_data = student[block_key]
        prio1 = block_data['prio1']
        prio2 = block_data['prio2']
        prio3 = block_data['prio3']
        options = []
        for mod_key, mod_value in try_block.items():
            if mod_value['slots'] != 0:
                opt_factor = mod_value['factor']
                if mod_key in prio1:
                    opt_factor *= fac1
                elif mod_key in prio2:
                    opt_factor *= fac2
                elif mod_key in prio3:
                    opt_factor *= fac3
            
                options += [mod_key] * opt_factor

        c = choice(options)
        block_data['choice'] = c
        try_block[c]['slots'] -= 1
        try_block[c]['IDs'].append(student['ID'])

    return try_block