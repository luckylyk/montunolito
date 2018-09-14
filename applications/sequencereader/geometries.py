import sys
from PyQt5 import QtCore
from sequencereader.rules import POSITIONS_COUNT, get_note_position, is_altered


MEASURE_WIDTH = 325
MEASURE_HEIGHT = MEASURE_WIDTH * .75
MEASURE_HSPACING = -30
KEYSPACE_WIDTH = 30


def get_widget_size(signature, line_count):
    signature_width = define_signature_width(MEASURE_HEIGHT, signature)
    width = KEYSPACE_WIDTH + signature_width + (MEASURE_WIDTH * 4)
    height = \
        (line_count * (MEASURE_HEIGHT + MEASURE_HSPACING)) - MEASURE_HSPACING
    return QtCore.QSize(width, height)


def extract_measures_rects(rect, signature):
    signature_width = define_signature_width(MEASURE_HEIGHT, signature)
    left = KEYSPACE_WIDTH + signature_width
    top = 0
    rects = []
    while top < rect.height():
        rects.append(QtCore.QRect(left, top, MEASURE_WIDTH, MEASURE_HEIGHT))
        left += MEASURE_WIDTH
        if left > (rect.width() - (MEASURE_WIDTH / 2)):
            left = KEYSPACE_WIDTH + signature_width
            top += MEASURE_HEIGHT + MEASURE_HSPACING
    return rects


def define_signature_width(height, signature):
    return height / 15 * len(signature.positions)


def extract_signature_rects(rect, signature):
    width = define_signature_width(MEASURE_HEIGHT, signature)
    left = KEYSPACE_WIDTH
    top = 0
    rects = []
    while top < rect.height():
        rects.append(QtCore.QRect(left, top, width, MEASURE_HEIGHT))
        top += MEASURE_HEIGHT + MEASURE_HSPACING
    return rects


def extract_rects_keyspaces(rect):
    top = 0
    rects = []
    while top < rect.height():
        rects.append(QtCore.QRect(0, top, KEYSPACE_WIDTH, MEASURE_HEIGHT))
        top += MEASURE_HEIGHT + MEASURE_HSPACING
    return rects


def extract_quarters_rects(measurerect):
    padding = measurerect.width() * .08
    measurerect = QtCore.QRectF(
        measurerect.left() + padding, measurerect.top(),
        measurerect.width() - (2 * padding), measurerect.height())
    width = measurerect.width() / 2
    rects = []
    for i in range(2):
        rects.append(
            QtCore.QRect(
                measurerect.left() + (width * i),
                measurerect.top(),
                width,
                measurerect.height()))
    return rects


def extract_notes_lefts(quarterrect):
    padding = quarterrect.width() * .125
    quarterrect = QtCore.QRectF(
        quarterrect.left() + padding, quarterrect.top(),
        quarterrect.width() - (2 * padding), quarterrect.height())
    width = quarterrect.width() * .1
    spacing = (quarterrect.width() - (width * 4)) / 3
    return [quarterrect.left() + ((width + spacing) * i) for i in range(4)]


def get_note_x(x, radius, difference, direction):
    if direction == 'up':
        return x - radius if difference > 1 else x + radius
    return x + radius if difference > 1 else x - radius


def get_alteration_x(x, radius, difference, direction):
    left = x - (radius * 3.5) if difference > 5 else x - (radius * 6)
    if direction != 'up':
        left += radius * 1.25
    return left


def get_top_from_position(height, position):
    position = POSITIONS_COUNT - position
    return (height / POSITIONS_COUNT) * (position - 1)


def get_note_body_and_alterations_centers(
        notes, alterations, x, y, height, direction, display_scale):
    radius = height / POSITIONS_COUNT
    previous_position = sys.maxsize
    previous_alteration_position = sys.maxsize
    centers = []
    alterations_centers = []
    for note, alteration in zip(notes, alterations):
        position = get_note_position(note, display_scale)
        top = y + get_top_from_position(height, position)
        difference = abs(position - previous_position)
        left = get_note_x(x, radius, difference, direction)
        centers.append(QtCore.QPointF(left, top))
        previous_position = position

        if alteration is None:
            continue
        difference = abs(position - previous_alteration_position)
        left = get_alteration_x(x, radius, difference, direction)
        alterations_centers.append(QtCore.QPointF(left, top))
        previous_alteration_position = position if difference > 5 else sys.maxsize

    return centers, alterations_centers
