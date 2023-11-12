def init_students(students_raw: list, blocks: dict) -> list[dict]:
    """
    Returns list of student data.
    Define fields for priorities and weights per block.
    """
    
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
    """
    Calculate weights (number of priorities per block) for students.
    """
    
    for student in students:
        for i in range(N):
            s = student['block'+str(i+1)]
            s['weight'] = len(s['prio1']) + len(s['prio2']) + len(s['prio3'])


def get_students_stat(students: list, block_nr: int) -> dict:
    """
    Return dictionary with statistics about student selections.
    """
    
    block_key = 'block'+str(block_nr)
    prio1 = prio2 = prio3 = prio0 = 0

    for student in students:
        st = student[block_key]
        choice = st['choice']

        if choice in st['prio1']:
            prio1 += 1
        elif choice in st['prio2']:
            prio2 += 1
        elif choice in st['prio3']:
            prio3 += 1
        else:
            prio0 += 1

    return {'prio1': prio1, 'prio2': prio2, 'prio3': prio3, 'prio0': prio0}    


def get_students_penalty(students: list, block_nr: int, fac2=1, fac3=10, fac0=100) -> int:
    """
    Return penalty for students.
    Parameters:
    fac2, fac3: penalty for assigned module with priority 2 or 3
    fac0: penalty for assigned module without priority
    """
    
    block_key = 'block'+str(block_nr)
    penalty = 0

    for student in students:
        st = student[block_key]
        weight = st['weight']
        choice = st['choice']

        if choice in st['prio1']:
            pass
        elif choice in st['prio2']:
            penalty += weight*fac2
        elif choice in st['prio3']:
            penalty += weight*fac3
        else:
            penalty += weight*fac0

    return penalty


def update_students(block: dict, block_nr: int, students: list) -> None:
    """
    Update student data (upon getting a new try for a block)
    """
    
    block_key = 'block'+str(block_nr)

    for mod_key, mod_val in block.items():
        ids = mod_val['IDs']
        for id in ids:
            st = next(s for s in students if s['ID'] == id)
            student = st[block_key]
            student['choice'] = mod_key


def get_p0_students(block_nr: int, students: list) -> list:
    """
    Return list of students who have been assigned module without priority in block_nr.
    """
    
    p0_students = []
    block_key = 'block'+str(block_nr)

    for student in students:
        st = student[block_key]
        c = st['choice']
        if not (c in st['prio1'] or
                c in st['prio2'] or
                c in st['prio3']):
            p0_students.append({'ID': student['ID'], 'weight': st['weight']})

    return p0_students


def get_classes_for_module(block:dict, module: str, students: list) -> list:
    """
    Return list of classes of students in given module.
    """

    ids = block[module]['IDs']
    classes = []
    for id in ids:
        st = next(s for s in students if s ['ID'] == id)
        classes.append(st['class'])

    return sorted(list(set(classes)))


def get_incomplete_students(students: list, N_blocks: int) -> list:
    """
    Return list of students with missing assignments.
    """
    
    incompletes = []

    for student in students:
        for i in range(1, N_blocks+1):
            if student['block'+str(i)]['choice'] is None:
                incompletes.append({'block': 'block'+str(i), 'ID': student['ID']})

    return incompletes
