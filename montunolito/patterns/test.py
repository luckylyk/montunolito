
NAME = 'test'


PATTERN = {
    'figures': 
    [
        [(1, 1, 1, 1), (1, 0, 1, 1)],
        [(1, 1, 1, 1)],
        [(1, 0, 1, 1)],
        [(1, 0, 0, 1), (1, 0, 1, 1), (1, 1, 1, 1)]
    ],
    'relationships':
    {
        (0, 0): {(1, 0): 5},
        (0, 1): {(1, 0): 5},
        (1, 0): {(2, 0): 5},
        (2, 0): {(3, 0): 5, (3, 1): 5, (3, 2): 5},
        (3, 0): {(0, 0): 5, (0, 1): 5},
        (3, 1): {(0, 0): 5, (0, 1): 5},
        (3, 2): {(0, 0): 5, (0, 1): 5}
    },
    'behaviors': {
        (0, 0): {'static': 1, 'melodic': 2, 'arpegic': 0},
        (0, 1): {'static': 0, 'melodic': 2, 'arpegic': 0},
        (1, 0): {'static': 1, 'melodic': 2, 'arpegic': 0},
        (2, 0): {'static': 1, 'melodic': 2, 'arpegic': 0},
        (3, 0): {'static': 1, 'melodic': 2, 'arpegic': 0},
        (3, 1): {'static': 0, 'melodic': 2, 'arpegic': 1},
        (3, 2): {'static': 0, 'melodic': 2, 'arpegic': 1}
    }
}