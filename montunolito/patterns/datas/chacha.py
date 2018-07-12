
NAME = 'chacha'

PATTERN = {
    1: [(1, 6, 0, 6)],
    2: [(1, 6, 0, 6)],
    3: [(1, 6, 0, 6)],
    4: [(1, 6, 0, 6)],
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