import pandas as pd

def get_choices(blocks: list[str], priorities_df: pd.DataFrame, weights=[3, 2, 1]) -> pd.DataFrame:

    n_people = len(priorities_df)

    block_names = [block for block in blocks.keys()]

    dict = {}
    first = {}
    seconds = {}
    thirds = {}
    score = {}
    
    max_length_first = {}
    max_length_seconds = {}
    max_length_thirds = {}

    last_name_list = []
    first_name_list = []
    class_list = []

    choices_df = pd.DataFrame()


    for block_name in block_names:
        first[block_name] = []
        seconds[block_name] = []
        thirds[block_name] = []
        score[block_name] = []
        max_length_first[block_name] = 0
        max_length_seconds[block_name] = 0
        max_length_thirds[block_name] = 0

    for id, row in priorities_df.iterrows():
        last_name_list.append(row['last_name'])
        first_name_list.append(row['first_name'])
        class_list.append(row['class'])

        for block_id, block_name in enumerate(block_names):

            p1 = []
            p2 = []
            p3 = []

            for item in row['priorities']:
                if block_id == item['module_type'] - 1:
                    if item['priority'] == 3:
                        p1.append(item['module_name'])
                    if item['priority'] == 2:
                        p2.append(item['module_name'])
                    if item['priority'] == 1:
                        p3.append(item['module_name'])

                if len(p1) > max_length_first[block_name]:
                    max_length_first[block_name] = len(p1)
                if len(p2) > max_length_seconds[block_name]:
                    max_length_seconds[block_name] = len(p2)
                if len(p3) > max_length_thirds[block_name]:
                    max_length_thirds[block_name] = len(p3)
            
            first[block_name].append(p1)
            seconds[block_name].append(p2)
            thirds[block_name].append(p3)
            score[block_name].append(weights[0] * len(p1) + weights[1] * len(p2) + weights[2] * len(p3))

    dict['last_name'] = last_name_list
    dict['first_name'] = first_name_list
    dict['class'] = class_list

    total_score = [0] * n_people

    for block_name in block_names:
        col_names_first = [f'{block_name}_first_{i}' for i in range(max_length_first[block_name])]
        col_names_seconds = [f'{block_name}_second_{i}' for i in range(max_length_seconds[block_name])]
        col_names_thirds = [f'{block_name}_third_{i}' for i in range(max_length_thirds[block_name])]
        col_name_score = f'{block_name}_score'

        dict[f'{block_name}_first_choice'] = first[block_name]    
        dict[f'{block_name}_second_choices'] = seconds[block_name]
        dict[f'{block_name}_third_choices'] = thirds[block_name]
        dict[f'{block_name}_score'] = score[block_name]

        choices_df[col_names_first] = pd.DataFrame(dict[f'{block_name}_first_choice'])
        choices_df[col_names_seconds] = pd.DataFrame(dict[f'{block_name}_second_choices'])
        choices_df[col_names_thirds] = pd.DataFrame(dict[f'{block_name}_third_choices'])
        choices_df[col_name_score] = pd.DataFrame(dict[f'{block_name}_score'])

        for i, s in enumerate(dict[f'{block_name}_score']):
            total_score[i] += s

    dict['total_score'] = total_score
    choices_df['total_score'] = pd.DataFrame(dict['total_score'])


    return choices_df