
NAME = 'montuno'


PATTERN = {
    'quarters': [
        [(1, 0, 6, 1), (1, 3, 5, 1), (2, 3, 5, 1)],
        [(0, 6, 0, 1), (0, 3, 5, 1), (0, 1, 0, 1)],
        [(0, 6, 0, 1), (0, 6, 0, 6), (0, 3, 5, 1)],
        [(0, 6, 1, 1), (0, 2, 3, 4), (0, 6, 0, 1), (0, 6, 1, 0), (1, 0, 1, 0)]
    ],
    'relationships': {
        (0, 0): {(1, 0): 5, (1, 1): 0, (1, 2): 3},
        (0, 1): {(1, 0): 2, (1, 1): 5, (1, 2): 3},
        (0, 2): {(1, 0): 2, (1, 1): 5, (1, 2): 3},
        (1, 0): {(2, 0): 5, (2, 1): 1, (2, 2): 1},
        (1, 1): {(2, 0): 2, (2, 1): 3, (2, 2): 4},
        (1, 2): {(2, 0): 2, (2, 1): 3, (2, 2): 4},
        (2, 0): {(3, 0): 3, (3, 1): 1, (3, 2): 2, (3, 3): 2, (3, 4): 3},
        (2, 1): {(3, 0): 0, (3, 1): 3, (3, 2): 0, (3, 3): 2, (3, 4): 5},
        (2, 2): {(3, 0): 2, (3, 1): 0, (3, 2): 2, (3, 3): 0, (3, 4): 4},
        (3, 0): {(0, 0): 3, (0, 1): 3, (0, 2): 0}, 
        (3, 1): {(0, 0): 2, (0, 1): 0, (0, 2): 5},
        (3, 2): {(0, 0): 4, (0, 1): 2, (0, 2): 0},
        (3, 3): {(0, 0): 4, (0, 1): 0, (0, 2): 0},
        (3, 4): {(0, 0): 2, (0, 1): 4, (0, 2): 0}
    },
    'behaviors': {
        (0, 0): {'static': 3, 'melodic': 1, 'arpegic': 5},
        (0, 1): {'static': 0, 'melodic': 0, 'arpegic': 5},
        (0, 2): {'static': 0, 'melodic': 3, 'arpegic': 5},
        (1, 0): {'static': 5, 'melodic': 5, 'arpegic': 3},
        (1, 1): {'static': 0, 'melodic': 0, 'arpegic': 5},
        (1, 2): {'static': 2, 'melodic': 6, 'arpegic': 0},
        (2, 0): {'static': 5, 'melodic': 5, 'arpegic': 3},
        (2, 1): {'static': 5, 'melodic': 0, 'arpegic': 0},
        (2, 2): {'static': 0, 'melodic': 0, 'arpegic': 5},
        (3, 0): {'static': 5, 'melodic': 0, 'arpegic': 0},
        (3, 1): {'static': 0, 'melodic': 6, 'arpegic': 1},
        (3, 2): {'static': 5, 'melodic': 5, 'arpegic': 3},
        (3, 3): {'static': 3, 'melodic': 1, 'arpegic': 3},
        (3, 4): {'static': 0, 'melodic': 6, 'arpegic': 0}
    }
}