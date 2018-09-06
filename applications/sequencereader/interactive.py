
from montunolito.core.utils import split_array

from sequencereader.painting import draw_measure, draw_quarter, draw_keyspace
from sequencereader.shapes import (
    get_notes_bodies_path, get_path, G_KEY, get_measure_separator,
    get_notes_connections_path, get_eighth_rest_path,
    get_notes_alterations_path)
from sequencereader.staff import get_standard_staff_lines, get_beams_directions
from sequencereader.geometries import (
    extract_quarters_rects, extract_notes_lefts,
    get_note_body_and_alterations_centers)


class IGQuater(object):
    def __init__(self, rect, sequence):
        self.rect = rect
        self.sequence = sequence
        self.lefts = None
        self.directions = None
        self.centers = None
        self.alteration_centers = None
        self.bodies = None
        self.alterations = None
        self.connections = None
        self.rests = None

    def set_rect(self, rect):
        if rect is None:
            return
        self.rect = rect
        self.lefts = extract_notes_lefts(self.rect)
        self.directions = get_beams_directions(self.sequence)
        self.centers, self.alteration_centers = self._get_note_centers()
        self.bodies = get_notes_bodies_path(self.centers, self.rect.height())
        self.alterations = get_notes_alterations_path(
            self.alteration_centers, self.rect.height())
        self.connections = get_notes_connections_path(
            self.lefts, self.rect.top(), self.rect.height(), self.sequence)
        self.rests = self._get_rests_paths()

    def _get_rests_paths(self):
        rests = []
        for notes, left in zip(self.sequence, self.lefts):
            if not notes:
                rests.append(
                    get_eighth_rest_path(
                        left, self.rect.top(), self.rect.height()))
        return rests

    def _get_note_centers(self):
        centers = []
        alteration_centers = []
        iterator = zip(self.sequence, self.directions, self.lefts)
        for notes, direction, x in iterator:
            c, a = get_note_body_and_alterations_centers(
                notes, x, self.rect.top(), self.rect.height(), direction)
            centers.extend(c)
            alteration_centers.extend(a)
        return centers, alteration_centers

    def draw(self, painter):
        draw_quarter(painter, self)



class IGMeasure(object):
    def __init__(self, rect, sequence):
        self.rect = rect
        self.staff_lines = get_standard_staff_lines(rect) if rect else None
        self.separator = get_measure_separator(rect) if rect else None
        sequences = split_array(sequence, 4)
        rects = extract_quarters_rects(rect) if rect else [None] * 2
        self.igquarters = [IGQuater(r, s) for r, s in zip(rects, sequences)]

    def set_rect(self, rect):
        self.rect = rect
        self.staff_lines = get_standard_staff_lines(rect) if rect else None
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
        self.staff_lines = get_standard_staff_lines(rect) if rect else None
        ratio =  self.rect.height() / 3.5
        self.key = get_path(G_KEY, ratio, position=self.rect.center())

    def set_rect(self, rect):
        self.rect = rect
        self.staff_lines = get_standard_staff_lines(rect) if rect else None
        ratio =  self.rect.height() / 3.5
        self.key = get_path(G_KEY, ratio, position=self.rect.center())

    def draw(self, painter):
        if self.rect is None:
            return
        draw_keyspace(painter, self)