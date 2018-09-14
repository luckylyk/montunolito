
from PyQt5 import QtCore

from montunolito.core.utils import split_array

from sequencereader.painting import (
    draw_measure, draw_quarter, draw_keyspace, draw_signature)
from sequencereader.shapes import (
    get_notes_bodies_path, get_path, G_KEY, get_measure_separator,
    get_notes_connections_path, get_eighth_rest_path, FLAT, SHARP,
    get_notes_alterations_path)
from sequencereader.rules import (
    get_beams_directions, POSITIONS_COUNT, get_note_position,
    get_signature_positions, is_empty_signature, is_flat_signature,
    get_alterations)
from sequencereader.staff import (
    get_standard_staff_lines, get_beam_bottom, get_beams_tops,
    get_extra_stafflines_path, get_top_from_position, get_signature_centers)
from sequencereader.geometries import (
    extract_quarters_rects, extract_notes_lefts,
    get_note_body_and_alterations_centers)


class IGQuarter(object):
    def __init__(self, rect, sequence, alterations, display_scale):
        self.rect = rect
        self.sequence = sequence
        self.alterations = alterations
        self.display_scale = display_scale
        self.alterations_path = None
        self.lefts = None
        self.directions = None
        self.centers = None
        self.alteration_centers = None
        self.rests = None
        self.bodies = None
        self.connections = None
        self.extralines = None

    def set_rect(self, rect):
        if rect is None:
            return
        self.rect = rect
        self.lefts = extract_notes_lefts(self.rect)
        self.directions = get_beams_directions(self.sequence)
        self.update()

    def update(self):
        self.centers, self.alteration_centers = self._get_note_centers()
        self.rests = self._get_rests_paths()
        self.bodies = get_notes_bodies_path(self.centers, self.rect.height())
        self.alterations_path = get_notes_alterations_path(
            [v for a in self.alterations for v in a if v is not None],
            self.alteration_centers,
            self.rect.height())
        self.connections = get_notes_connections_path(
            self.lefts,
            self.rect.height(),
            self._get_beams_tops(),
            self._get_beams_bottoms(),
            self.directions)
        self.extralines = self._get_extra_stafflines()

    def set_alterations(self, alterations, display_scale):
        self.alterations = alterations
        self.display_scale = display_scale
        if self.rect:
            self.update()

    def _get_beams_bottoms(self):
        top = self.rect.top()
        height = self.rect.height()
        return [
            top + get_beam_bottom(height, notes, self.display_scale, d == 'up')
            if notes else None
            for d, notes in zip(self.directions, self.sequence)]

    def _get_beams_tops(self):
        return [
            self.rect.top() + t if t else t
            for t in get_beams_tops(
                self.rect.height(),
                self.sequence,
                self.directions,
                self.display_scale)]

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
        iterator = zip(self.sequence, self.directions, self.lefts, self.alterations)
        for notes, direction, x, alterations in iterator:
            c, a = get_note_body_and_alterations_centers(
                notes=notes,
                alterations=alterations,
                x=x,
                y=self.rect.top(),
                height=self.rect.height(),
                direction=direction,
                display_scale=self.display_scale)
            centers.extend(c)
            alteration_centers.extend(a)
        return centers, alteration_centers

    def _get_extra_stafflines(self):
        radius = (self.rect.height() / POSITIONS_COUNT) * 1.25
        scale = self.display_scale
        path = []
        index = 0
        for notes in self.sequence:
            notes_centers = self.centers[index: index + len(notes)]
            index += len(notes)
            positions = [get_note_position(n, scale) for n in notes]
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
    def __init__(self, rect, sequence, signature):
        self.rect = rect
        self.end = False
        self.staff_lines = get_standard_staff_lines(rect) if rect else None
        self.separator = get_measure_separator(rect, self.end) if rect else None
        self.sequence = sequence
        alterations = split_array(get_alterations(sequence, signature.tonality), 4)
        sequences = split_array(sequence, 4)
        rects = extract_quarters_rects(rect) if rect else [None] * 2
        self.igquarters = [
            IGQuarter(r, s, a, signature.display_scale())
            for r, s, a in zip(rects, sequences, alterations)]

    def set_rect(self, rect):
        self.rect = rect
        self.staff_lines = get_standard_staff_lines(rect) if rect else None
        self.separator = get_measure_separator(rect, self.end) if rect else None
        rects = extract_quarters_rects(rect) if rect else [None] * 2
        for igquater, rect in zip(self.igquarters, rects):
            igquater.set_rect(rect)
        if not rect:
            return

    def set_signature(self, signature):
        alterations = split_array(get_alterations(self.sequence, signature.tonality), 4)
        for a, igquarter in zip(alterations, self.igquarters):
            igquarter.set_alterations(a, signature.display_scale())

    def draw(self, painter):
        if self.rect is None:
            return
        draw_measure(painter, self)
        for igquater in self.igquarters:
            igquater.draw(painter)


class IGSignature():
    def __init__(self, rect, signature):
        self.rect = rect
        self.tonality = signature
        self.centers = get_signature_centers(rect, signature)
        self.shapes = get_notes_alterations_path(
            [self.tonality.value()] * len(self.centers),
            self.centers, self.rect.height())
        self.staff_lines = get_standard_staff_lines(self.rect)

    def draw(self, painter):
        draw_signature(painter, self)


class IGKeySpace():
    def __init__(self, rect):
        self.rect = None
        self.staff_lines = None
        self.key = None
        self.set_rect(rect)

    def set_rect(self, rect):
        self.rect = rect
        self.staff_lines = get_standard_staff_lines(rect) if rect else None
        ratio = self.rect.height() / 3.5
        self.key = get_path(G_KEY, ratio, position=self.rect.center())

    def draw(self, painter):
        if self.rect is None:
            return
        draw_keyspace(painter, self)
