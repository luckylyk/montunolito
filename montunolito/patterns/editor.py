
EMPTY_PATTERN = {
    'quarters': [],
    'relationships': {},
    'behaviors': {}
}
EMPTY_BEHAVIORS = {'static': 0, 'melodic': 0, 'arpegic': 0}


def get_new_pattern():
    return EMPTY_PATTERN.copy()


def append_quarter_row(pattern):
    pattern['quarters'].append([])


def append_fingerstates_indexes(pattern, fingerstates_indexes, row):
    # add fingerstates indexes
    pattern['quarters'][row].append(fingerstates_indexes)

    # add behabiors
    index = row, len(pattern['quarters'][row]) - 1
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


def delete_fingerstates_indexes(pattern, index):
    row, column = index
    indexes_to_offset = sorted([
        (r, c) for (r, c) in get_existing_indexes_in_row(pattern, row)
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
    del pattern['quarters'][row][column]


def get_existing_indexes(pattern):
    indexes = []
    for index, quarter in enumerate(pattern['quarters']):
        for i, _ in enumerate(quarter):
            indexes.append(tuple([index, i]))
    return indexes


def get_existing_indexes_in_row(pattern, row):
    return [
        indexe for indexe in get_existing_indexes(pattern)
        if indexe[0] == row]


def index_exists(pattern, index):
    row, column = index
    conditions = (
        len(pattern['quarters']) <= row or
        len(pattern['quarters'][row]) <= column)
    if conditions:
        return False
    return True


def get_next_row(pattern, row):
    row += 1
    row = row if row < len(pattern['quarters']) else 0
    return row


def get_previous_row(pattern, row):
    row -= 1
    row = row if row >= 0 else len(pattern['quarters']) - 1
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