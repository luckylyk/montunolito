
from draws import draw_note_path
from coordinates import (
    get_note_path, get_beam_tail_path, get_beams_connection_path,
    get_eighth_rest_path, extract_noterects)

from montunolito.core.solfege import FINGERSSTATES


FINGERSTATES_PATH_KWARGS = [
    None,
    {'note1': True, 'note2': False, 'note3': False, 'note4': True},
    {'note1': True, 'note2': False, 'note3': False, 'note4': False},
    {'note1': False, 'note2': True, 'note3': False, 'note4': False},
    {'note1': False, 'note2': False, 'note3': True, 'note4': False},
    {'note1': False, 'note2': False, 'note3': False, 'note4': True},
    {'note1': False, 'note2': True, 'note3': False, 'note4': True},
    {'note1': True, 'note2': True, 'note3': True, 'note4': True}]


class Fingerstates(object):
    def __init__(self, fingerstates_indexes, rect):
        self._fingerstates_indexes = fingerstates_indexes
        self._noterects = extract_noterects(rect)
        self.selected = None

    def set_selected_state(self, cursor):
        for i, noterect in enumerate(self._noterects):
            if noterect.contains(cursor):
                self.selected = i
                break
        else:
            self.selected = None

    def draw(self, painter, cursor):
        previous_fingerstates_index = None
        previous_kwargs = None

        for i, fingerstates_index in enumerate(self._fingerstates_indexes):
            noterect = self._noterects[i]
            hover = noterect.contains(cursor)
            selected = self.selected == i
            kwargs = FINGERSTATES_PATH_KWARGS[fingerstates_index]

            if not kwargs:
                previous_fingerstates_index = fingerstates_index
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

            if previous_fingerstates_index:
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
                    i == len(self._fingerstates_indexes) - 1 or
                    FINGERSTATES_PATH_KWARGS[self._fingerstates_indexes[i + 1]]
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
            previous_fingerstates_index = fingerstates_index
