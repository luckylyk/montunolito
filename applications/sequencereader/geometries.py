from PyQt5 import QtCore

MEASURE_WIDTH = 200
MEASURE_HEIGHT = MEASURE_WIDTH * .8
KEYSPACE_WIDTH = 100


def extract_measures_rects(rect):
    left = KEYSPACE_WIDTH
    top = 0
    rects = []
    while top < rect.height():
        rects.append(QtCore.QRect(left, top, MEASURE_WIDTH, MEASURE_HEIGHT))
        left += MEASURE_WIDTH
        if left > (rect.width() - MEASURE_WIDTH):
            left = KEYSPACE_WIDTH
            top += MEASURE_HEIGHT

    return rects


def extract_keys_rects(rect):
    top = 0
    rects = []
    while top < rect.height():
        rects.append(QtCore.QRect(0, top, KEYSPACE_WIDTH, MEASURE_HEIGHT))
        top += MEASURE_HEIGHT
    return rects
