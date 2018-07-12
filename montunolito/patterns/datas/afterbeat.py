
NAME = 'afterbeat'

PATTERN = {
    1: [(0, 7, 0, 7)],
    2: [(0, 7, 0, 7)],
    3: [(0, 7, 0, 7)],
    4: [(0, 7, 0, 7)],
    'relationships': {
        (1, 0): {(2, 0): 5},
        (2, 0): {(3, 0): 5},
        (3, 0): {(4, 0): 5},
        (4, 0): {(1, 0): 5}},
    'behaviors': {
        (1, 0): {'static': 5, 'diatonic': 0, 'arpegic': 0, 'chromatic': 0},
        (2, 0): {'static': 5, 'diatonic': 0, 'arpegic': 0, 'chromatic': 0},
        (3, 0): {'static': 5, 'diatonic': 0, 'arpegic': 0, 'chromatic': 0},
        (4, 0): {'static': 5, 'diatonic': 0, 'arpegic': 0, 'chromatic': 0}
        }}