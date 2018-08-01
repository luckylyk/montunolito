from montunolito.core.solfege import FINGERSSTATES
from painting import draw_note_path
from context import DrawContext
from geometries import (
    get_note_path, get_beam_tail_path, get_beams_connection_path,
    get_eighth_rest_path, extract_noterects)


FINGERSTATES_PATH_KWARGS = [
    None,
    {
        'note1': True,
        'note2': False,
        'note3': False,
        'note4': False,
        'note5': True
    },
    {
        'note1': True,
        'note2': False,
        'note3': False,
        'note4': False,
        'note5': False
    },
    {
        'note1': False,
        'note2': True,
        'note3': False,
        'note4': False,
        'note5': False
    },
    {
        'note1': False,
        'note2': False,
        'note3': True,
        'note4': False,
        'note5': False
    },
    {
        'note1': False,
        'note2': False,
        'note3': False,
        'note4': True,
        'note5': False
    },
    {
        'note1': False,
        'note2': True,
        'note3': False,
        'note4': True,
        'note5': False
    },
    {
        'note1': True,
        'note2': True,
        'note3': True,
        'note4': True,
        'note5': True
    }
]


class IGFingerstateSelecter(object):
    def __init__(self, rect):
        self.rect = rect
        self._noterects = extract_noterects(rect, number=8)

    def get_hovered_index(self, cursor):
        for i, rect in enumerate(self._noterects):
            if rect.contains(cursor):
                return i
        return None

    def draw(self, painter, cursor):
        for i, kwargs in enumerate(FINGERSTATES_PATH_KWARGS):
            noterect = self._noterects[i]
            hover = noterect.contains(cursor)
            if kwargs is None:
                note_path = get_eighth_rest_path(noterect)
            else:
                note_path = get_note_path(noterect, **kwargs)

            draw_note_path(
                painter,
                note_path,
                hover=hover,
                selected=False)


class IGFigure(object):
    def __init__(self, figure, rect=None):
        self._figure = list(figure)
        self._rect = rect
        self._noterects = extract_noterects(rect) if rect else None
        self.selected = None

    def set_selected_state(self, cursor):
        if not self._rect.contains(cursor):
            return

        for i, noterect in enumerate(self._noterects):
            if noterect.contains(cursor):
                self.selected = i
                break
        else:
            self.selected = None

    @property
    def figure(self):
        return tuple(self._figure)

    def set_rect(self, rect):
        self._rect = rect
        self._noterects = extract_noterects(rect)

    def set_fingerstate(self, eighth_index, fingerstate_index):
        self._figure[eighth_index] = fingerstate_index

    def draw(self, painter, cursor, hoverable=True):
        if self._rect is None:
            return

        previous_fingerstate_index = None
        previous_kwargs = None

        for i, fingerstate_index in enumerate(self._figure):
            noterect = self._noterects[i]
            hover = noterect.contains(cursor) and hoverable
            selected = self.selected == i
            kwargs = FINGERSTATES_PATH_KWARGS[fingerstate_index]

            if not kwargs:
                previous_fingerstate_index = fingerstate_index
                previous_kwargs = kwargs
                note_path = get_eighth_rest_path(noterect)
                draw_note_path(
                    painter,
                    note_path,
                    hover=hover,
                    selected=selected)
                continue

            note_path = get_note_path(noterect, **kwargs)
            draw_note_path(
                painter,
                note_path,
                hover=hover,
                selected=selected)

            if previous_fingerstate_index:
                connection_path = get_beams_connection_path(
                    self._noterects[i-1], noterect)
                draw_note_path(
                    painter,
                    connection_path,
                    hover=hover,
                    selected=selected)

            conditions = (
                previous_kwargs is None and
                (
                    i == len(self._figure) - 1 or
                    FINGERSTATES_PATH_KWARGS[self._figure[i + 1]]
                    is None
                ))

            if conditions:
                tail_path = get_beam_tail_path(noterect)
                draw_note_path(
                    painter,
                    tail_path,
                    hover=hover,
                    selected=selected)

            previous_kwargs = kwargs
            previous_fingerstate_index = fingerstate_index
