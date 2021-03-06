# every pattern contains 3 keys: figures, relationships and behaviors
# keys 'figures' contains differents alternative array of hand pattern index.
# the key number correspond the figure of the pattern (1 = first figure, etc)
# the 'relationship' key contains a dict. His keys represent the pattern index
# it contain the pattern index of the next figure and a value
# (between 0 and 5)
# it's for generate random patterns.
# this is data and will be moved in JSON files. Every pattern will be save as
# different json file.


EMPTY_PATTERN = {
    'figures': [[], [], [], []],
    'relationships': {},
    'behaviors': {}
}
EMPTY_BEHAVIORS = {'static': 1, 'melodic': 1, 'arpegic': 1}


def get_new_pattern():
    return deepcopy(EMPTY_PATTERN)


def append_figure_row(pattern):
    pattern['figures'].append([])


def append_figure_at_row(pattern, figure, row):
    # add fingerstates indexes
    pattern['figures'][row].append(figure)

    # add behabiors
    index = row, len(pattern['figures'][row]) - 1
    pattern['behaviors'][index] = EMPTY_BEHAVIORS.copy()

    # add relationships
    next_row = get_next_row(pattern, row)
    relationships_indexes = get_existing_indexes_in_row(pattern, next_row)
    relationships = {i: 1 for i in relationships_indexes}
    pattern['relationships'][index] = relationships

    previous_row = get_previous_row(pattern, row)
    relationships_indexes = get_existing_indexes_in_row(pattern, previous_row)
    for relationships_index in relationships_indexes:
        pattern['relationships'][relationships_index].update({index: 0})


def delete_figure_at(pattern, index):
    row, column = index
    indexes_to_offset = sorted(
        [(r, c) for (r, c) in get_existing_indexes_in_row(pattern, row)
         if c > column],
        key=lambda x: x[1])

    # remove and offset behaviors
    if indexes_to_offset:
        for (r, c) in indexes_to_offset:
            pattern['behaviors'][(r, c-1)] = pattern['behaviors'][(r, c)]
        del pattern['behaviors'][indexes_to_offset[-1]]
    else:
        del pattern['behaviors'][index]

    # remove and offset relationships indexes
    if indexes_to_offset:
        for (r, c) in indexes_to_offset:
            pattern['relationships'][(r, c-1)] = \
                pattern['relationships'][(r, c)]
        del pattern['relationships'][indexes_to_offset[-1]]
    else:
        del pattern['relationships'][index]

    # clean relationship in other indexes
    previous_row = get_previous_row(pattern, row)
    relationship_indexes = get_existing_indexes_in_row(pattern, previous_row)
    for relationship_index in relationship_indexes:
        if indexes_to_offset:
            for (r, c) in indexes_to_offset:
                pattern['relationships'][relationship_index][(r, c-1)] = \
                    pattern['relationships'][relationship_index][(r, c)]
            del pattern['relationships'][relationship_index][indexes_to_offset[-1]]
        else:
            del pattern['relationships'][relationship_index][index]

    # remove fingerstates indexes
    del pattern['figures'][row][column]


def get_existing_indexes(pattern):
    indexes = []
    for index, figure in enumerate(pattern['figures']):
        for i, _ in enumerate(figure):
            indexes.append(tuple([index, i]))
    return indexes


def get_existing_indexes_in_row(pattern, row):
    return [
        indexe for indexe in get_existing_indexes(pattern)
        if indexe[0] == row]


def index_exists(pattern, index):
    row, column = index
    conditions = (
        len(pattern['figures']) <= row or
        len(pattern['figures'][row]) <= column)
    if conditions:
        return False
    return True


def get_next_row(pattern, row):
    row += 1
    row = row if row < len(pattern['figures']) else 0
    return row


def get_row_lenght(pattern, row=None):
    if row is not None:
        return len(pattern['figures'][row])
    return max([len(row) for row in pattern['figures']])


def get_previous_row(pattern, row):
    row -= 1
    row = row if row >= 0 else len(pattern['figures']) - 1
    return row


def set_relationship_value(pattern, out_index, in_index, value):
    conditions = (
        index_exists(pattern, out_index) and
        index_exists(pattern, in_index))
    if not conditions:
        raise IndexError(
            "pattern doesn't contain index {} or {}".format(
                out_index, in_index))

    pattern['relationships'][out_index][in_index] = value


def set_behavior_value(pattern, index, behavior, value):
    if not index_exists(pattern, index):
        raise IndexError("pattern doesn't contain index {}".format(index))
    pattern['behaviors'][index][behavior] = value


def get_index_occurence_probablity(pattern, index):
    if not index_exists(pattern, index):
        raise IndexError("pattern doesn't contain index {}".format(index))

    row, _ = index
    row_to_check = get_previous_row(pattern, row)
    indexes_to_check = get_existing_indexes_in_row(pattern, row_to_check)
    total = 0
    index_score = 0
    for index_to_check in indexes_to_check:
        for i, v in pattern['relationships'][index_to_check].items():
            total += v
            if i == index:
                index_score += v
    if total == 0:
        return 0
    return round((float(index_score) / total) * 100)


def get_out_connected_indexes(pattern, index):
    relationships = pattern['relationships'].get(index, {})
    return [index for index, value in relationships.items()]


def get_in_connected_indexes(pattern, index):
    indexes = []
    previous_row = get_previous_row(pattern, index[0])
    in_indexes = get_existing_indexes_in_row(pattern, previous_row)
    for in_index in in_indexes:
        if pattern['relationships'].get(in_index, {}).get(index):
            indexes.append(in_index)
    return indexes


def get_relationship(pattern, in_index, out_index):
    return pattern['relationships'][out_index][in_index]


def set_relationship(pattern, in_index, out_index, value):
    pattern['relationships'][out_index][in_index] = value


def get_figure_at(pattern, index):
    row, col = index
    return pattern['figures'][row][col]


def set_figure_at(pattern, index, figure):
    row, col = index
    pattern['figures'][row][col] = figure


def get_behaviors_at(pattern, index):
    return pattern['behaviors'][index]


def set_behaviors_at(pattern, index, behaviors):
    pattern['behaviors'][index] = behaviors


def deepcopy(pattern):
    cpattern = {}
    cpattern['figures'] = [row[:] for row in pattern['figures']]
    cpattern['relationships'] = {
        k: {l: w for l, w in v.items()}
        for k, v in pattern['relationships'].items()}
    cpattern['behaviors'] = {
        k: {l: w for l, w in v.items()}
        for k, v in pattern['behaviors'].items()}
    return cpattern


def is_dead_end(pattern, index):
    relationships = pattern['relationships'][index]
    iterability = sum([v for v in relationships.values()])
    return not bool(iterability)


def is_valid_pattern(pattern):
    try:
        pattern['figures']
        pattern['relationships']
        pattern['behaviors']
        return True
    except KeyError:
        return False


def is_iterable_pattern(pattern):
    errors = []
    warnings = []

    for i, figure in enumerate(pattern['figures']):
        if not figure:
            errors.append('pattern contain emtpy row: {}'.format(i))

    for index, behaviors in pattern['behaviors'].items():
        result = sum([v for v in behaviors.values()])
        if not result:
            errors.append(
                'figure at {} doesn\'t have behaviors indices'.format(index))

    indexes = get_existing_indexes(pattern)
    for index in indexes:
        if not get_index_occurence_probablity(pattern, index):
            warnings.append('figure at {} will never played'.format(index))
            continue
        if is_dead_end(pattern, index):
            errors.append(
                'figure at {} is a dead end,'
                'it doesn\'t have out relationships'.format(index))

    result = not bool(errors)
    log = 'Errors: {}\n\nWarnings: {}'.format(
        '\n  - '.join(errors) if errors else 'No errors',
        '\n  - '.join(warnings) if warnings else 'No warnings')
    return result, log
