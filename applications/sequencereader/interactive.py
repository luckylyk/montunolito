
from sequencereader.painting import draw_measure


class IGMeasure(object):
    def __init__(self, rect, sequence):
        self.rect = rect
        self.sequence = sequence

    def draw(self, painter):
        if self.rect is None:
            return
        draw_measure(painter, self)