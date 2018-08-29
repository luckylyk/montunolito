from PyQt5 import QtCore


MEASURE_WIDTH = 250
MEASURE_HEIGHT = MEASURE_WIDTH * .65
KEYSPACE_WIDTH = 50


def extract_measures_rects(rect):
    left = KEYSPACE_WIDTH
    top = 0
    rects = []
    while top < rect.height():
        rects.append(QtCore.QRect(left, top, MEASURE_WIDTH, MEASURE_HEIGHT))
        left += MEASURE_WIDTH
        if left > (rect.width() - (MEASURE_WIDTH / 2)):
            left = KEYSPACE_WIDTH
            top += MEASURE_HEIGHT
    return rects


def extract_rects_keyspaces(rect):
    top = 0
    rects = []
    while top < rect.height():
        rects.append(QtCore.QRect(0, top, KEYSPACE_WIDTH, MEASURE_HEIGHT))
        top += MEASURE_HEIGHT
    return rects


def extract_quarters_rects(measurerect):
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


def extract_notes_rects(quarterrect):
    padding = quarterrect.width() * .125
    quarterrect = QtCore.QRectF(
        quarterrect.left() + padding, quarterrect.top(),
        quarterrect.width() - (2 * padding), quarterrect.height())
    width = quarterrect.width() * .1
    spacing = (quarterrect.width() - (width * 4)) / 3
    rects = []
    for i in range(4):
        rects.append(
            QtCore.QRect(
                quarterrect.left() + ((width + spacing) * i),
                quarterrect.top(),
                width,
                quarterrect.height()))
    return rects
