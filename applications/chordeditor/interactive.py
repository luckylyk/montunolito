from montunolito.core.solfege import NOTES, CHORDS
from montunolito.core.utils import (
    remap_number, split_array, set_array_lenght_multiple)

from chordeditor.painting import (
    draw_note_item, draw_staff, draw_chord, draw_selection_rects,
    draw_selection_square)
from chordeditor.geometries import (
    extract_items_rect, get_staff_path, get_selection_rects, get_square_rect,
    extract_staffs_rects, extract_heighth_rects, get_repeat_path,
    get_staff_selecter_rect, get_staff_selecter_path, grow_rect)


class IGItem():
    def __init__(self, rect, text, index=None):
        self.index = index
        self.text = text
        self.rect = rect
        self.hovered = False
        self.active = False

    def set_state(self, cursor, active=False):
        if not self.rect.contains(cursor):
            self.hovered = False
            return
        self.hovered = True
        self.active = active

    def draw(self, painter):
        draw_note_item(painter, self)


class IGNoteSelecter():
    def __init__(self, rect, tonality):
        self.rect = rect
        self.notes = []
        self.enable = False
        self.set_tonality(tonality)

    def set_tonality(self, tonality):
        self.notes = []
        for i in range(12):
            self.notes.append(IGItem(
                extract_items_rect(self.rect, i, len(NOTES)),
                NOTES[remap_number(i + tonality, 12)],
                index=i))

    def set_states(self, cursor, clicked=False):
        active_note = self.active_note()
        for igitem in self.notes:
            active = igitem == active_note if active_note else clicked
            active = active if self.enable else False
            igitem.set_state(cursor, active=active)

    def active_note(self):
        for igitem in self.notes:
            if igitem.active:
                return igitem
        return None

    def released(self):
        for igitem in self.notes:
            igitem.active = False

    def draw(self, painter):
        for igitem in self.notes:
            igitem.draw(painter)


FUNCTIONS = (
    'Major', 'Minor', 'M6', 'm6', 'M7', 'm7', 'M7M', 'm7M', 'M7b9',
    'm7b9', 'M9', 'm9', 'M11', 'm11', 'dim', 'sus4', 'aug', 'qm')


class IGFunctionSelecter():
    def __init__(self, rect):
        self.rect = rect
        self.chords = [
            IGItem(extract_items_rect(rect, i, len(FUNCTIONS)), name)
            for i, name in enumerate(FUNCTIONS)]
        self.enable = False

    def set_states(self, cursor, clicked=False):
        for igitem in self.chords:
            active = clicked if igitem.rect.contains(cursor) and self.enable else False
            igitem.set_state(cursor, active=active)
            if active:
                for ii in self.chords:
                    if igitem != ii:
                        ii.active = False

    def active_chord(self):
        for igitem in self.chords:
            if igitem.active:
                return igitem
        return None

    def released(self):
        for igitem in self.chords:
            igitem.active = False

    def draw(self, painter):
        for igitem in self.chords:
            igitem.draw(painter)


class IGStaff():
    def __init__(self, rect, chords, final=False, tonality=0):
        self.chords = [
            IGChord(rect, chord, tonality)
            for rect, chord in zip(chords, extract_heighth_rects(rect))]
        self.rect = rect
        self.final = final
        self.selecter_hovered = False
        self.selected = False

        self.path = get_staff_path(self.rect, self.final)
        self.selecter_rect = get_staff_selecter_rect(self.rect)
        self.selecter_path = get_staff_selecter_path(self.selecter_rect)
        self.selected_rect = grow_rect(self.rect, 4)

    def set_hover(self, cursor):
        self.selecter_hovered = self.selecter_rect.contains(cursor)

    def set_rect(self, rect):
        chord_rects = extract_heighth_rects(rect)
        for i, igchord in enumerate(self.chords):
            igchord.set_rect(chord_rects[i])
        self.rect = rect
        self.path = get_staff_path(self.rect, self.final)
        self.selecter_rect = get_staff_selecter_rect(self.rect)
        self.selecter_path = get_staff_selecter_path(self.selecter_rect)
        self.selected_rect = grow_rect(self.rect, 4)

    def draw(self, painter):
        for igchord in self.chords:
            igchord.draw(painter)
        draw_staff(painter, self)
        selection_rects = get_selection_rects(self.chords)
        if selection_rects:
            draw_selection_rects(painter, selection_rects)


class IGChord():
    def __init__(self, chord, rect, tonality=0):
        self.active = False
        self.hovered = False
        self.selected = False

        self.rect = rect
        self.chord = chord
        self.tonality = tonality
        self.name = self.note() + ' ' + chord['name'] if chord else None
        self.path = get_repeat_path(self.rect) if self.chord is None else None

    def set_tonality(self, tonality):
        self.tonality = tonality
        name = self.note() + ' ' + self.chord['name'] if self.chord else None
        self.name = name

    def note(self):
        return NOTES[remap_number(self.chord['degree'] + self.tonality, 12)]

    def set_rect(self, rect):
        self.rect = rect
        self.path = get_repeat_path(self.rect) if self.chord is None else None

    def set_chord(self, chord):
        self.chord = chord
        if chord is None:
            self.path = get_repeat_path(self.rect)
            self.name = None
            return
        self.path = None
        self.name = self.note() + ' ' + chord['name']

    def activate(self, cursor):
        self.active = self.rect.contains(cursor)

    def set_hover(self, cursor):
        self.hovered = self.rect.contains(cursor)

    def draw(self, painter):
        draw_chord(painter, self)


class IGSelectionSquare():
    def __init__(self):
        self.in_point = None
        self.out_point = None

    def reset(self):
        self.in_point = None
        self.out_point = None

    @property
    def rect(self):
        if not all([self.in_point, self.out_point]):
            return
        return get_square_rect(self.in_point, self.out_point)

    def draw(self, painter):
        draw_selection_square(painter, self.rect)


class IGChordGrid():
    def __init__(self, rect, chordgrid, tonality=0):
        self.rect = rect
        self.staffs = None
        self.tonality = tonality
        self.set_chordgrid(chordgrid)

    def set_chordgrid(self, chordgrid):
        chordgrids = split_array(chordgrid, 32)
        set_array_lenght_multiple(chordgrids[-1], 32)
        staff_rects = extract_staffs_rects(self.rect, len(chordgrids))
        self.staffs = []
        for i, (chords, rect) in enumerate(zip(chordgrids, staff_rects)):
            staff = IGStaff(
                rect,
                chords,
                final=i == len(chordgrids) - 1,
                tonality=self.tonality)
            self.staffs.append(staff)

    def activate(self, cursor):
        for igchord in self.igchords():
            igchord.activate(cursor)

    def set_hover(self, cursor):
        for igchord in self.igchords():
            igchord.set_hover(cursor)
        for igstaff in self.staffs:
            igstaff.set_hover(cursor)

    def igchords(self):
        return [
            igchord for igstaff in self.staffs
            for igchord in igstaff.chords]

    def active_index(self):
        for i, igchord in enumerate(self.igchords()):
            if igchord.active:
                return i

    def hovered_index(self):
        for i, igchord in enumerate(self.igchords()):
            if igchord.hovered:
                return i

    def selected_indexes(self):
        return [
            i for i, igchord in enumerate(self.igchords()) if igchord.selected]

    def selected_chords(self):
        return [self.igchord(i) for i in self.selected_indexes()]

    @property
    def chordgrid(self):
        return [igchord.chord for igchord in self.igchords()]

    def igchord(self, index):
        if index is None:
            return None
        staff = index // 32
        index = index % 32
        return self.staffs[staff].chords[index]

    def released(self):
        for igchord in self.igchords():
            igchord.active = False

    def clear_selection(self):
        for igchord in self.igchords():
            igchord.selected = False
        for igstaff in self.staffs:
            igstaff.selected = False

    def select_staff(self):
        for igstaff in self.staffs:
            if igstaff.selecter_hovered is True:
                igstaff.selected = True

    def select_hovered(self, rect=None):
        if rect is not None:
            igchords = [
                igchord for igchord in self.igchords()
                if rect.intersects(igchord.rect)]
            for igchord in igchords:
                igchord.selected = True
        else:
            igchord = self.igchord(self.hovered_index())
            if igchord:
                igchord.selected = True

    def delete_selected_staffs(self):
        for igstaff in reversed(self.staffs):
            if igstaff.selected is True:
                self.staffs.remove(igstaff)
                del igstaff
        count = len(self.staffs)
        rects = extract_staffs_rects(self.rect, count)
        for i, igstaff in enumerate(self.staffs):
            igstaff.final = i == count - 1
            igstaff.set_rect(rects[i])

    def select_range(self, index_1, index_2=None):
        index_2 = index_2 or index_1
        start = min([index_1, index_2])
        end = max([index_1, index_2])
        for i in range(start, end + 1):
            self.igchord(i).selected = True

    def draw(self, painter):
        for igstaff in self.staffs:
            igstaff.draw(painter)
        selection_rects = get_selection_rects(self.staffs, 4)
        draw_selection_rects(painter, selection_rects, staff=True)
