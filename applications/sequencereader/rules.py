from montunolito.core.utils import past_and_futur, remap_number
from montunolito.core.solfege import SCALE_LENGTH, NOTES

# positons scales
SHARP_SCALE = 0, 0, 1, 2, 2, 3, 3, 4, 5, 5, 6, 6
BEMOLE_SCALE = 0, 1, 1, 2, 3, 3, 4, 4, 5, 6, 6, 7

SHARP_KEY_SIGNATURES_POSITIONS = 33, 30, 34, 31, 28, 32, 29
BEMOL_KEY_SIGNATURES_POSITIONS = 29, 32, 28, 31, 27, 30, 26
SHARP_NOTES_ALTERED = 8, 3, 10, 5, 0, 7, 2
BEMOL_NOTES_ALTERED = [n for n in reversed(SHARP_NOTES_ALTERED)]
SIGNATURES = (
    'C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#',
    'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'B')

ALTERED_INDEXES = 1, 4, 6, 9, 11
POSITION_PER_NATURAL_NOTES = [
    i for i in range(89) if len(NOTES[remap_number(i, SCALE_LENGTH)]) == 1]

STAFF_LINES_NUMBERS = 26
POSITIONS_COUNT = 54
LINE_MATCHERS = {m: [(m * 2) - i for i in range(1, 3)] for m in range(13)}
LINE_MATCHERS.update(
    {m: [(m * 2) - i for i in range(2, 4)] for m in range(18, 28)})


def get_signature_positions(signature, major=True):
    if is_empty_signature(signature, major=major):
        return []

    if is_bemol_signature(signature, major=major):
        signatures = get_bemol_signatures(major=major)
        positions = BEMOL_KEY_SIGNATURES_POSITIONS
    else:
        signatures = get_sharp_signatures(major=major)
        positions = SHARP_KEY_SIGNATURES_POSITIONS

    index = signatures.index(signature)
    return positions[:index + 1]


def is_empty_signature(signature, major=True):
    if major:
        return signature == 'C'
    return signature == 'A'


def is_bemol_signature(signature, major=True):
    return signature in get_bemol_signatures(major=major)


def get_bemol_signatures(major=True):
    if major:
        return SIGNATURES[8:]
    return [e for e in reversed(SIGNATURES[11:] + SIGNATURES[:3])]


def get_sharp_signatures(major=True):
    if major:
        return SIGNATURES[1:8]
    return SIGNATURES[11:] + SIGNATURES[:2]


def get_matching_line(position):
    for line, positions in LINE_MATCHERS.items():
        if position in positions:
            return line


def get_note_position(note, display_scale=None):
    display_scale = display_scale or BEMOLE_SCALE
    offset = (note // SCALE_LENGTH) * 7
    line = display_scale[remap_number(note, SCALE_LENGTH)]
    return offset + line


def get_beams_directions(sequence):
    directions = []
    positions_averages = []
    for _, notes, next_notes in past_and_futur(sequence):
        if not notes:
            directions.append(None)
            positions_averages = []
            continue

        positions_averages.append(
            sum([get_note_position(n) for n in notes]) / len(notes))
        if not next_notes:
            averages_count = len(positions_averages)
            average = sum([a for a in positions_averages]) / averages_count
            for _ in range(averages_count):
                directions.append('up' if average < 29 else 'down')
    return directions


def is_altered(note):
    return remap_number(note, SCALE_LENGTH) in ALTERED_INDEXES


def get_alteration_value(note, position):
    reference = POSITION_PER_NATURAL_NOTES[position]
    return note - reference


def get_visible_alteration(sequence, signature):
    '''TODO'''


class Signature():
    def __init__(self):
        self.mode = None
        self.signature = None
        self.positions = None
        self.shape = None

    def reset(self):
        self.mode = None
        self.signature = None
        self.positions = None
        self.shape = None

    def set_values(self, signature=None, mode=None, ):
        self.mode = mode or self.mode
        self.signature = signature or self.signature
        self.process()

    def process(self):
        if None in (self.signature, self.mode):
            return
        major = self.mode == 'major'
        self.positions = get_signature_positions(self.signature, major=major)

    def is_bemol(self):
        return is_bemol_signature(self.signature, self.mode == 'major')

    def is_empty(self):
        return bool(len(self.positions))

    def is_sharp(self):
        return not any([self.is_bemol(), self.is_empty()])