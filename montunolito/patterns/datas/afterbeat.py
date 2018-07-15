
NAME = 'afterbeat'


PATTERN = {
    'quarters': [
        [(0, 7, 0, 7)],
        [(0, 7, 0, 7)],
        [(0, 7, 0, 7)],
        [(0, 7, 0, 7)]
    ],
    'relationships': {
        (0, 0): {(1, 0): 5},
        (1, 0): {(2, 0): 5},
        (2, 0): {(3, 0): 5},
        (3, 0): {(0, 0): 5}
    },
    'behaviors': {
        (0, 0): {'static': 5, 'melodic': 0, 'arpegic': 0},
        (1, 0): {'static': 5, 'melodic': 0, 'arpegic': 0},
        (2, 0): {'static': 5, 'melodic': 0, 'arpegic': 0},
        (3, 0): {'static': 5, 'melodic': 0, 'arpegic': 0}
    }
}