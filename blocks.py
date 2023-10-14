def init_blocks(blocks: dict) -> None:
    for block in blocks.values():
        for module, slots in block.items():
            block[module] = {'slots': slots, 'prio1': 0, 'prio2': 0, 'prio3': 0, 
                             'factor': 1, 'IDs': []}


def calc_factors(blocks: dict) -> None:
    for block in blocks.values():
        for mod_key, mod_value in block.items():
            slots = mod_value['slots']
            prio1 = mod_value['prio1']
            prio2 = mod_value['prio2']
            prio3 = mod_value['prio3']

            if (empty := slots-prio1) >= 0:
                mod_value['factor'] += 1
                if (empty := empty-prio2) >= 0:
                    mod_value['factor'] += 1
                    if empty - prio3 >= 0:
                        mod_value['factor'] += 1


def get_block_stat(block: dict, block_nr: int, students: list) -> dict:

    block_stat = {}

    total = totp1 = totp2 = totp3 = totp0 = 0

    for mod_key, mod_val in block.items():
        ids = mod_val['IDs']
        prio1 = prio2 = prio3 = prio0 = 0
        for id in ids:
            student = next(s for s in students if s['ID'] == id)
            if mod_key in student['block'+str(block_nr)]['prio1']:
                prio1 += 1
            elif mod_key in student['block'+str(block_nr)]['prio2']:
                prio2 += 1
            elif mod_key in student['block'+str(block_nr)]['prio3']:
                prio3 += 1
            else:
                prio0 += 1
            
        block_stat[mod_key] = {'prio1': prio1, 
                               'prio2': prio2, 
                               'prio3': prio3, 
                               'prio0': prio0}

        total += prio1+prio2+prio3+prio0
        totp1 += prio1
        totp2 += prio2
        totp3 += prio3
        totp0 += prio0

    block_stat['total'] = {'total': total,
                           'totp1': totp1,
                           'totp2': totp2,
                           'totp3': totp3,
                           'totp0': totp0}
    
    return block_stat


def get_block_penalty(block: dict, block_nr: int, students: list, 
                      fac1=1, fac2=2, fac3=3, fac0=10) -> int:
    totals = get_block_stat(block, block_nr, students)['total']

    return (fac1*totals['totp1']
            +fac2*totals['totp2']
            +fac3*totals['totp3']
            +fac0*totals['totp0'])

