NAME = 'Cumbia (melody)'


PATTERN = {
    "behaviors": {
        (3, 0): {"arpegic": 0, "static": 5, "melodic": 0},
        (3, 1): {"arpegic": 5, "static": 0, "melodic": 0},
        (2, 0): {"arpegic": 0, "static": 6, "melodic": 0},
        (2, 1): {"arpegic": 4, "static": 2, "melodic": 0},
        (1, 0): {"arpegic": 0, "static": 6, "melodic": 0},
        (0, 0): {"arpegic": 0, "static": 6, "melodic": 0}
    },
    "figures": [
        [(0, 0, 7, 0)],
        [(0, 0, 7, 0)],
        [(0, 0, 7, 0), (0, 3, 6, 3)],
        [(0, 0, 7, 0), (0, 3, 7, 0)]
    ],
    "relationships": {
        (3, 0): {(0, 0): 1},
        (3, 1): {(0, 0): 1},
        (2, 0): {(3, 0): 10, (3, 1): 0},
        (2, 1): {(3, 0): 0, (3, 1): 1},
        (1, 0): {(2, 1): 1, (2, 0): 4},
        (0, 0): {(1, 0): 10}
    }
}