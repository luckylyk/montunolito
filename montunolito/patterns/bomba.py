
NAME = 'Puerto Rican Bomba (simple)'

PATTERN = {
    "figures": [
        [(1, 0, 5, 6)],
        [(0, 5, 0, 6)],
        [(0, 6, 0, 2)],
        [(6, 0, 6, 0), (1, 0, 1, 0)]
    ],
    "relationships": {
        (0, 0): {(1, 0): 5},
        (1, 0): {(2, 0): 5},
        (2, 0): {(3, 0): 1, (3, 1): 1},
        (3, 0): {(0, 0): 1},
        (3, 1): {(0, 0): 1}
    },
    "behaviors": {
        (0, 0): {"melodic": 0, "static": 3, "arpegic": 1},
        (1, 0): {"melodic": 0, "static": 2, "arpegic": 1},
        (2, 0): {"melodic": 0, "static": 2, "arpegic": 1},
        (3, 0): {"melodic": 0, "static": 3, "arpegic": 3},
        (3, 1): {"melodic": 3, "static": 4, "arpegic": 1}},
}