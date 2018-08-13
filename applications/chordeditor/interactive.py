from montunolito.core.solfege import NOTES, CHORDS
from montunolito.core.utils import (
    remap_number, split_array, set_array_lenght_multiple)

from painting import draw_note_item, draw_staff
from geometries import (
    extract_noteitem_rect, extract_chordname_rect, get_staff_path,
    extract_staffs_rects, extract_heighth_rects, get_repeat_path)


class IGItem():
    def __init__(self, rect, name):
        self.displayname = name
        self.rect = rect
        self.hovered = False
        self.clicked = False

    def set_state(self, cursor, clicked=False):
        if not self.rect.contains(cursor):
            self.hovered = False
            self.clicked = False
            return
        self.hovered = True
        self.clicked = clicked

    def draw(self, painter):
        draw_note_item(painter, self)


class IGNoteSelecter():
    def __init__(self, rect, key):
        self.rect = rect
        self.notes = [
            IGItem(extract_noteitem_rect(rect, i),
            NOTES[remap_number(i + key, 12)])
            for i in range(12)]

    def draw(self, painter):
        for note in self.notes:
            note.draw(painter)


class IGChordSelecter():
    def __init__(self, rect, name):
        self.rect = rect
        self.chords = [
            IGItem(extract_chordname_rect(rect, i), name)
            for i, name in enumerate (CHORDS.keys())]

    def draw(self, painter):
        for chord in self.chords:
            chord.draw(painter)


class IGStaff():
    def __init__(self, rect, chords, final=False, tonality=0):
        self.chords = [
            IGChord(rect, chord, tonality)
            for rect, chord in zip(chords, extract_heighth_rects(rect))]
        self.rect = rect
        self.final = final
        self.path = get_staff_path(self.rect, self.final)

    def draw(self, painter):
        draw_staff(painter, self.path)
        for igchord in self.chords:
            igchord.draw(painter)



class IGChord():
    def __init__(self, chord, rect, tonality=0):
        self.rect = rect
        self.chord = chord
        self.tonality = tonality

    def draw(self, painter):
        print (self.chord)
        if self.chord is None:
            painter.drawPath(get_repeat_path(self.rect))


class IGChordGrid():
    def __init__(self, rect, chordgrid, tonality=0):
        self.rect = rect
        chordgrids = split_array(chordgrid, 16)
        set_array_lenght_multiple(chordgrids[-1], 16)
        staff_rects = extract_staffs_rects(self.rect, len(chordgrids))
        self.staffs = []
        for i, (chords, rect) in enumerate(zip(chordgrids, staff_rects)):
            staff = IGStaff(
                rect,
                chords,
                final=i == len(chordgrids) - 1,
                tonality=tonality)
            self.staffs.append(staff)

    def draw(self, painter):
        for staff in self.staffs:
            staff.draw(painter)