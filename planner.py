from copy import deepcopy
from random import choice, random

from blocks import get_block_stat


def get_try(block: dict, block_nr: int, students: dict, specials,
            fac1=100, fac2=50, fac3=20):

    ks_classes = ('3p', '3q')
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
        ks = student['class'] in ks_classes
        c = None

        if (c:=set(prio1).intersection(set(specials['fixed_p1']))):
            c = list(c)[0]

        else:
            options = []
            for mod_key, mod_value in try_block.items():
                if not (ks and mod_value['mng_only']):
                    if mod_value['slots'] != 0:
                        opt_factor = mod_value['factor']
                        if mod_key in prio1:
                            opt_factor *= fac1
                        elif mod_key in prio2:
                            opt_factor *= fac2
                        elif mod_key in prio3:
                            opt_factor *= fac3
                        elif (mod_key in specials['no_p0']) or ks:
                            opt_factor = 0
                    
                        options += [mod_key] * opt_factor
            if options:
                c = choice(options)

        if c:
            block_data['choice'] = c
            try_block[c]['slots'] -= 1
            try_block[c]['IDs'].append(student['ID'])
        else:
            block_data['choice'] = None

    return try_block


def list_results(blocks: dict, block_nr: int, students: list, details=False) -> None:
    block = blocks[block_nr-1]

    stat = get_block_stat(block, block_nr, students)
    stat_tot = stat['total']
    p1 = stat_tot['totp1']
    p2 = stat_tot['totp2']
    p3 = stat_tot['totp3']
    p0 = stat_tot['totp0']
    tot = len(students)

    print(f'block {block_nr}: p1: {p1/tot*100:.1f}%, p2: {p2/tot*100:.1f}%, '
          + f'p3: {p3/tot*100:.1f}%, p0: {p0/tot*100:.1f}%')

    if details:  
        for mod_key, mod_val in stat.items():
            if mod_key != 'total':
                slots = mod_val['slots']
                p1 = mod_val['prio1']
                max1 = mod_val['max1']
                p2 = mod_val['prio2']
                max2 = mod_val['max2']
                p3 = mod_val['prio3']
                max3 = mod_val['max3']
                p0 = mod_val['prio0']
                tot = p1+p2+p3+p0

                print(f'{mod_key}: {tot}/{slots}, '
                    + f'p1: {p1/tot*100:.1f}% ({max1/slots*100:.1f}%), '
                    + f'p2: {p2/tot*100:.1f}% ({max2/slots*100:.1f}%), '
                    + f'p3: {p3/tot*100:.1f}% ({max3/slots*100:.1f}%), '
                    + f'p0: {p0/tot*100:.1f}%')

    print()
