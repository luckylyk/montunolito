
from montunolito.core.utils import split_array
from PyQt5 import QtCore
from sequencereader.painting import draw_measure, draw_quarter, draw_keyspace
from sequencereader.shapes import (
    get_notes_bodies_path, get_path, G_KEY, get_measure_separator,
    get_notes_connections_path, get_eighth_rest_path,
    get_notes_alterations_path)
from sequencereader.rules import (
    get_beams_directions, POSITIONS_COUNT, get_note_position)
from sequencereader.staff import (
    get_standard_staff_lines, get_beam_bottom, get_beams_tops,
    get_extra_stafflines_path, get_top_from_position)
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
        self.rests = None
        self.bodies = None
        self.alterations = None
        self.connections = None
        self.extralines = None

    def set_rect(self, rect):
        if rect is None:
            return

        self.rect = rect
        self.lefts = extract_notes_lefts(self.rect)
        self.directions = get_beams_directions(self.sequence)
        self.centers, self.alteration_centers = self._get_note_centers()
        self.rests = self._get_rests_paths()
        self.bodies = get_notes_bodies_path(self.centers, self.rect.height())
        self.alterations = get_notes_alterations_path(
            self.alteration_centers, self.rect.height())
        self.connections = get_notes_connections_path(
            self.lefts,
            self.rect.height(),
            self._get_beams_tops(),
            self._get_beams_bottoms(),
            self.directions)
        self.extralines = self._get_extra_stafflines()

    def _get_beams_bottoms(self):
        top = self.rect.top()
        height = self.rect.height()
        return [
            top + get_beam_bottom(height, notes, d == 'up')
            if notes else None
            for d, notes in zip(self.directions, self.sequence)]

    def _get_beams_tops(self):
        height = self.rect.height()
        return [
            self.rect.top() + t if t else t
            for t in get_beams_tops(height, self.sequence, self.directions)]

    def _get_rests_paths(self):
        rests = []
        for i, (notes, left) in enumerate(zip(self.sequence, self.lefts)):
            if i % 2 != 0:
                continue
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

    def _get_extra_stafflines(self):
        radius = (self.rect.height() / POSITIONS_COUNT) * 1.25
        path = []
        index = 0
        for notes in self.sequence:
            notes_centers = self.centers[index: index + len(notes)]
            index += len(notes)
            positions = [get_note_position(n) for n in notes]
            down_lines = get_extra_stafflines_path(
                self.rect.top(),
                self.rect.height(),
                radius,
                notes_centers,
                positions)

            up_lines = get_extra_stafflines_path(
                self.rect.top(),
                self.rect.height(),
                radius,
                notes_centers,
                positions,
                up=True)

            path.append(down_lines)
            path.append(up_lines)
        return path

    def draw(self, painter):
        draw_quarter(painter, self)


class IGMeasure(object):
    def __init__(self, rect, sequence):
        self.rect = rect
        self.end = False
        self.staff_lines = get_standard_staff_lines(rect) if rect else None
        self.separator = get_measure_separator(rect, self.end) if rect else None
        sequences = split_array(sequence, 4)
        rects = extract_quarters_rects(rect) if rect else [None] * 2
        self.igquarters = [IGQuater(r, s) for r, s in zip(rects, sequences)]
        self.positions = None

    def set_rect(self, rect):
        self.rect = rect
        self.staff_lines = get_standard_staff_lines(rect) if rect else None
        self.separator = get_measure_separator(rect, self.end) if rect else None
        rects = extract_quarters_rects(rect) if rect else [None] * 2
        for igquater, rect in zip(self.igquarters, rects):
            igquater.set_rect(rect)
        if not rect:
            return
        self.positions = [QtCore.QPointF(12, get_top_from_position(self.rect.height(), i)) for i in range(POSITIONS_COUNT)]

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
        ratio = self.rect.height() / 3.5
        self.key = get_path(G_KEY, ratio, position=self.rect.center())

    def set_rect(self, rect):
        self.rect = rect
        self.staff_lines = get_standard_staff_lines(rect) if rect else None
        ratio = self.rect.height() / 3.5
        self.key = get_path(G_KEY, ratio, position=self.rect.center())

    def draw(self, painter):
        if self.rect is None:
            return
        draw_keyspace(painter, self)
