def init_students(students_raw: list, blocks: dict) -> list[dict]:
    students = []

    for i, student in enumerate(students_raw):
    
        s = {'ID': f'{i:03}',
            'last_name': student['last_name'],
            'first_name': student['first_name'],
            'class': student['class'],
            'block1': {'prio1': [], 'prio2': [], 'prio3': [], 'weight': 1},
            'block2': {'prio1': [], 'prio2': [], 'prio3': [], 'weight': 1},
            'block3': {'prio1': [], 'prio2': [], 'prio3': [], 'weight': 1},
            'block4': {'prio1': [], 'prio2': [], 'prio3': [], 'weight': 1},
            'block5': {'prio1': [], 'prio2': [], 'prio3': [], 'weight': 1}
        }
        for p in student['priorities']:
            if (mod_prio := p['priority']) in (1, 2, 3):
                
                mod_type = p['module_type']
                mod_name = p['module_name']
                block = str(mod_type)
                prio = 'prio'+str(4-mod_prio)
                s['block'+block][prio].append(mod_name)

                blocks[block][mod_name][prio] += 1

        students.append(s)

    return students

def calc_weights(students: list, N: int) -> None:
    for student in students:
        for i in range(N):
            s = student['block'+str(i+1)]
            s['weight'] = len(s['prio1']) + len(s['prio2']) + len(s['prio3'])


def get_students_penalty(students: list, block_nr: int, fac2=1, fac3=2, fac0=10) -> int:
    block_key = 'block'+str(block_nr)
    penalty = 0

    for student in students:
        s = student[block_key]
        weight = s['weight']
        choice = s['choice']

        if choice in s['prio1']:
            pass
        elif choice in s['prio2']:
            penalty += weight*fac2
        elif choice in s['prio3']:
            penalty += weight*fac3
        else:
            penalty += weight*fac0

    return penalty


def get_p0_students(block: dict, block_nr: int, students:list) -> list:
    p0_students = []
    block_key = 'block'+str(block_nr)

    for mod_key, mod_val in block.items():
        ids = mod_val['IDs']
        for id in ids:
            st = next(s for s in students if s['ID'] == id)
            student = st[block_key]

            if not (mod_key in student['prio1'] or 
                    mod_key in student['prio2'] or 
                    mod_key in student['prio3']):
                p0_students.append({'ID': st['ID'], 'weight': student['weight']})

    return p0_students

