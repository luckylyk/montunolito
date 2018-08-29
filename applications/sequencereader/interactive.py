
from montunolito.core.utils import split_array

from sequencereader.painting import draw_measure, draw_quarter, draw_keyspace
from sequencereader.shapes import (
    get_staff_lines, get_measure_separator, get_notes_paths)
from sequencereader.geometries import (
    extract_quarters_rects, extract_notes_rects)


class IGQuater(object):
    def __init__(self, rect, sequence):
        self.rect = rect
        self.note_rects = extract_notes_rects(rect) if rect else None
        self.sequence = sequence
        self.paths = get_notes_paths(self.note_rects, sequence) if rect else []

    def set_rect(self, rect):
        self.rect = rect
        self.note_rects = extract_notes_rects(rect) if rect else None
        if rect:
            self.paths = get_notes_paths(self.note_rects, self.sequence)
        else:
            self.paths = []

    def draw(self, painter):
        if self.rect is None:
            return
        draw_quarter(painter, self)


class IGMeasure(object):
    def __init__(self, rect, sequence):
        self.rect = rect
        self.staff_lines = get_staff_lines(rect) if rect else None
        self.separator = get_measure_separator(rect) if rect else None
        sequences = split_array(sequence, 4)
        rects = extract_quarters_rects(rect) if rect else [None] * 2
        self.igquarters = [IGQuater(r, s) for r, s in zip(rects, sequences)]

    def set_rect(self, rect):
        self.rect = rect
        self.staff_lines = get_staff_lines(rect) if rect else None
        self.separator = get_measure_separator(rect) if rect else None
        rects = extract_quarters_rects(rect) if rect else [None] * 2
        for igquater, rect in zip(self.igquarters, rects):
            igquater.set_rect(rect)

    def draw(self, painter):
        if self.rect is None:
            return
        draw_measure(painter, self)
        for igquater in self.igquarters:
            igquater.draw(painter)


class IGKeySpace():
    def __init__(self, rect):
        self.rect = rect
        self.staff_lines = get_staff_lines(rect) if rect else None

    def set_rect(self, rect):
        self.rect = rect
        self.staff_lines = get_staff_lines(rect) if rect else None

    def draw(self, painter):
        if self.rect is None:
            return
        draw_keyspace(painter, self)