
NAME = 'test'

PATTERN = {
    1: [(1, 1, 1, 1), (1, 0, 1, 1)],
    2: [(1, 1, 1, 1)],
    3: [(1, 0, 1, 1)],
    4: [(1, 0, 0, 1), (1, 0, 1, 1), (1, 1, 1, 1)],
    'relationships': {
        (1, 0): {(2, 0): 5},
        (1, 1): {(2, 0): 5},
        (2, 0): {(3, 0): 5},
        (3, 0): {(4, 0): 5, (4, 1): 5, (4, 2): 5},
        (4, 0): {(1, 0): 5, (1, 1): 5},
        (4, 1): {(1, 0): 5, (1, 1): 5},
        (4, 2): {(1, 0): 5, (1, 1): 5}},
    'behaviors': {
        (1, 0): {'static': 1, 'diatonic': 1, 'arpegic': 0, 'chromatic': 1},
        (1, 1): {'static': 0, 'diatonic': 1, 'arpegic': 0, 'chromatic': 1},
        (2, 0): {'static': 1, 'diatonic': 1, 'arpegic': 0, 'chromatic': 1},
        (3, 0): {'static': 1, 'diatonic': 1, 'arpegic': 0, 'chromatic': 1},
        (4, 0): {'static': 1, 'diatonic': 1, 'arpegic': 0, 'chromatic': 1},
        (4, 1): {'static': 0, 'diatonic': 1, 'arpegic': 1, 'chromatic': 1},
        (4, 2): {'static': 0, 'diatonic': 1, 'arpegic': 1, 'chromatic': 1}
        }}