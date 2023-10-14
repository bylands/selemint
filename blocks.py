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
        slots = mod_val['slots']
        ids = mod_val['IDs']
        max1 = mod_val['prio1']
        max2 = mod_val['prio2']
        max3 = mod_val['prio3']
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
            
        block_stat[mod_key] = {'slots': slots+prio1+prio2+prio3+prio0,
                               'prio1': prio1, 
                               'max1': max1,
                               'prio2': prio2, 
                               'max2': max2,
                               'prio3': prio3, 
                               'max3': max3,
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
                      fac2=1, fac3=2, fac0=10, faclow=10, threshold=0.5) -> int:
    stat = get_block_stat(block, block_nr, students)
    low = 0
    for mod_key, mod_val in stat.items():
        if mod_key != 'total':
            slots = mod_val['slots']
            p1 = mod_val['prio1']
            p2 = mod_val['prio2']
            p3 = mod_val['prio3']
            p0 = mod_val['prio0']
            if (p1+p2+p3+p0)/slots < threshold:
                low += faclow

    totals = stat['total']
    p1 = totals['totp1']
    p2 = totals['totp2']
    p3 = totals['totp3']
    p0 = totals['totp0']
    

    return (fac2*p2
            +fac3*p3
            +fac0*p0
            +low)

