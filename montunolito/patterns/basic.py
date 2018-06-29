NAME = 'basic'

PATTERN = {
    1: [(1, 0, 6, 1), (1, 3, 5, 1), (2, 3, 5, 1)],
    2: [(0, 6, 0, 1), (0, 3, 5, 1), (0, 1, 0, 1)],
    3: [(0, 6, 0, 1), (0, 6, 0, 6), (0, 3, 5, 1)],
    4: [(0, 6, 1, 1), (0, 2, 3, 4), (0, 6, 0, 1), (0, 6, 1, 0), (1, 0, 1, 0)],
    'relationships': {
        (1, 0): {(2, 0): 5, (2, 1): 0, (2, 2): 3},
        (1, 1): {(2, 0): 2, (2, 1): 5, (2, 2): 3},
        (1, 2): {(2, 0): 2, (2, 1): 5, (2, 2): 3},
        (2, 0): {(3, 0): 5, (3, 1): 1, (3, 2): 1},
        (2, 1): {(3, 0): 2, (3, 1): 3, (3, 2): 4},
        (2, 2): {(3, 0): 2, (3, 1): 3, (3, 2): 4},
        (3, 0): {(4, 0): 3, (4, 1): 1, (4, 2): 2, (4, 3): 2, (4, 4): 3},
        (3, 1): {(4, 0): 0, (4, 1): 3, (4, 2): 0, (4, 3): 2, (4, 4): 5},
        (3, 2): {(4, 0): 2, (4, 1): 0, (4, 2): 2, (4, 3): 0, (4, 4): 4},
        (4, 0): {(1, 0): 3, (1, 1): 3, (1, 2): 0}, 
        (4, 1): {(1, 0): 2, (1, 1): 0, (1, 2): 5},
        (4, 2): {(1, 0): 4, (1, 1): 2, (1, 2): 0},
        (4, 3): {(1, 0): 4, (1, 1): 0, (1, 2): 0},
        (4, 4): {(1, 0): 2, (1, 1): 4, (1, 2): 0}},
    'behaviors': {
        (1, 0): {'static': 3, 'diatonic': 1, 'arpegic': 5, 'chromatic': 0},
        (1, 1): {'static': 0, 'diatonic': 0, 'arpegic': 5, 'chromatic': 0},
        (1, 2): {'static': 0, 'diatonic': 3, 'arpegic': 5, 'chromatic': 0},
        (2, 0): {'static': 5, 'diatonic': 3, 'arpegic': 3, 'chromatic': 2},
        (2, 1): {'static': 0, 'diatonic': 0, 'arpegic': 5, 'chromatic': 0},
        (2, 2): {'static': 2, 'diatonic': 3, 'arpegic': 0, 'chromatic': 3},
        (3, 0): {'static': 5, 'diatonic': 3, 'arpegic': 3, 'chromatic': 2},
        (3, 1): {'static': 5, 'diatonic': 0, 'arpegic': 0, 'chromatic': 0},
        (3, 2): {'static': 0, 'diatonic': 0, 'arpegic': 5, 'chromatic': 0},
        (4, 0): {'static': 5, 'diatonic': 0, 'arpegic': 0, 'chromatic': 0},
        (4, 1): {'static': 0, 'diatonic': 3, 'arpegic': 1, 'chromatic': 3},
        (4, 2): {'static': 5, 'diatonic': 3, 'arpegic': 3, 'chromatic': 2},
        (4, 3): {'static': 3, 'diatonic': 0, 'arpegic': 3, 'chromatic': 1},
        (4, 4): {'static': 0, 'diatonic': 3, 'arpegic': 0, 'chromatic': 3}}
        }