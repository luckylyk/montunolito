
from montunolito.core.pattern import (
    get_index_occurence_probablity, get_existing_indexes, get_figure_at,
    get_out_connected_indexes, get_relationship, get_behaviors_at,
    get_row_lenght)
from montunolito.core.solfege import FINGERSSTATES

from context import DrawContext
from painting import (
    draw_index, draw_row_background, draw_connection, draw_mas, draw_row_plus,
    draw_note_path, draw_slider_path)
from geometries import (
    get_index_behavior_rect, get_index_figure_rect, get_index_inplug_rect,
    get_index_outplug_rect, get_index_body_rect, get_row_rect, get_index_rect,
    get_connection_path, get_connection_handler_rect, shrink_rect,
    get_mas_rects, get_row_body_rect, get_row_plus_rect, get_row_body_path,
    connection_handler_path, get_return_connection_path,
    get_note_path, get_beam_tail_path, get_beams_connection_path,
    get_eighth_rest_path, extract_noterects, get_slider_handler_rect,
    get_slider_segmented_line_path, get_slider_handler_path)


class IGSlider(object):
    def __init__(self, rect, drawcontext=None, value=5, maxvalue=10):
        self.rect = rect
        self._drawcontext = drawcontext or DrawContext()
        self.value = value
        self._segmented_line_path = \
            get_slider_segmented_line_path(
                self._drawcontext,
                rect,
                maxvalue + 1)
        self._value_rects = [
            get_slider_handler_rect(rect, v, maxvalue)
            for v in range(maxvalue + 1)]
        self._value_path = get_slider_handler_path(self._value_rects[value])

    def hovered_value(self, cursor):
        for i, rect in enumerate(self._value_rects):
            if rect.contains(cursor):
                return i
        return None

    def set_value(self, cursor):
        for i, rect in enumerate(self._value_rects):
            if rect.contains(cursor):
                self.value = i
                self._value_path = get_slider_handler_path(
                    self._value_rects[i])
                return

    def draw(self, painter, cursor, pressed=False):
        draw_slider_path(
            painter,
            self._drawcontext,
            self._segmented_line_path,
            hover=False)
        hovered = self.hovered_value(cursor) == self.value
        draw_slider_path(
            painter,
            self._drawcontext,
            self._value_path,
            hover=hovered,
            background=True,
            pressed=pressed)


def get_fingerstates_path_kwargs():
    kwargs_list = []
    for fingertstate in FINGERSSTATES:
        if not any(fingertstate):
            kwargs_list.append(None)
            continue
        kwargs = {'note' + str(i + 1): v for i, v in enumerate(fingertstate)}
        kwargs_list.append(kwargs)
    return kwargs_list

FINGERSTATES_PATH_KWARGS = get_fingerstates_path_kwargs()


class IGFingerstateSelecter(object):
    def __init__(self, rect, drawcontext=None):
        self._drawcontext = None or DrawContext()
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
                self._drawcontext,
                note_path,
                hover=hover,
                selected=False)


class IGFigure(object):
    def __init__(self, figure, rect=None, drawcontext=None):
        self._drawcontext = drawcontext or DrawContext()
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
                    self._drawcontext,
                    note_path,
                    hover=hover,
                    selected=selected)
                continue

            note_path = get_note_path(noterect, **kwargs)
            draw_note_path(
                painter,
                self._drawcontext,
                note_path,
                hover=hover,
                selected=selected)

            if previous_fingerstate_index:
                connection_path = get_beams_connection_path(
                    self._noterects[i-1], noterect)
                draw_note_path(
                    painter,
                    self._drawcontext,
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
                    self._drawcontext,
                    tail_path,
                    hover=hover,
                    selected=selected)

            previous_kwargs = kwargs
            previous_fingerstate_index = fingerstate_index


class IGIndex(object):
    def __init__(self, index, pattern, drawcontext=None):
        self._drawcontext = drawcontext or DrawContext()
        self.selected = False
        self.pattern = pattern
        self.index = index

        self._rect = None
        self.inplug_rect = None
        self.outplug_rect = None
        self.body_rect = None
        self.figure_rect = None
        self.behavior_rect = None
        self._mas_rects = None

        self._igfigure = IGFigure(self.figure)
        self._rects = []
        self.update_geometries()

    def update_geometries(self):
        self._rect = get_index_rect(self._drawcontext, *self.index)
        self.inplug_rect = get_index_inplug_rect(
            self._drawcontext, self._rect)
        self.outplug_rect = get_index_outplug_rect(
            self._drawcontext, self._rect)
        self.body_rect = get_index_body_rect(self._drawcontext, self._rect)
        self.figure_rect = get_index_figure_rect(
            self._drawcontext, self.body_rect)
        self.behavior_rect = get_index_behavior_rect(
            self._drawcontext, self.body_rect)
        self._igfigure.set_rect(shrink_rect(self.figure_rect, 5))
        self._mas_rects = get_mas_rects(self.behavior_rect)

        self._rects = [
            self.inplug_rect,
            self.outplug_rect,
            self.body_rect,
            self.figure_rect,
            self.behavior_rect]

    @property
    def occurence(self):
        return get_index_occurence_probablity(self.pattern, self.index)

    @property
    def out_plug_center(self):
        return self.outplug_rect.center()

    @property
    def in_plug_center(self):
        return self.inplug_rect.center()

    @property
    def out_connected_indexes(self):
        return get_out_connected_indexes(self.pattern, self.index)

    def highlight_rects(self, cursor):
        return [rect for rect in self._rects if rect.contains(cursor)]

    @property
    def figure(self):
        return get_figure_at(self.pattern, self.index)

    @property
    def behaviors(self):
        return get_behaviors_at(self.pattern, self.index)

    def figure_hovered(self, cursor):
        return self.figure_rect.contains(cursor)

    def behavior_hovered(self, cursor):
        return self.behavior_rect.contains(cursor)

    def set_selected_state(self, cursor):
        if not self.selected:
            self.selected = (
                self.body_rect.contains(cursor) and
                not self.figure_rect.contains(cursor) and
                not self.behavior_rect.contains(cursor))
        else:
            self.selected = self._rect.contains(cursor)

    def draw(self, painter, cursor):
        draw_index(
            painter,
            self._drawcontext,
            self,
            highlight_rects=self.highlight_rects(cursor))
        self._igfigure.draw(painter, cursor, hoverable=False)
        draw_mas(painter, self._drawcontext, self._mas_rects, **self.behaviors)


class IGRow(object):
    def __init__(self, number, lenght, drawcontext=None):
        self._drawcontext = drawcontext or DrawContext()
        self.number = number
        self._lenght = lenght

        self._rect = None
        self._body_rect = None
        self._plus_rect = None
        self._body_path = None
        self.update_geometries()

    def update_geometries(self):
        self._rect = get_row_rect(self._drawcontext, self.number, self._lenght)
        self._body_rect = get_row_body_rect(self._drawcontext, self._rect)
        self._plus_rect = get_row_plus_rect(self._drawcontext, self._rect)
        self._body_path = get_row_body_path(
            self._drawcontext, self._body_rect, self._plus_rect)

    def is_hovered(self, cursor):
        return self._rect.contains(cursor)

    def plus_is_hovered(self, cursor):
        return self._plus_rect.contains(cursor)

    def draw(self, painter, cursor):
        draw_row_background(
            painter,
            self._drawcontext,
            self._body_path,
            self.is_hovered(cursor))
        draw_row_plus(
            painter,
            self._drawcontext,
            self._plus_rect,
            self.plus_is_hovered(cursor))


class IGConnection(object):
    def __init__(
            self, pattern, in_index, out_index, drawcontext=None):
        self._drawcontext = drawcontext or DrawContext()
        self.pattern = pattern
        self.in_index = in_index
        self.out_index = out_index
        self.returner = in_index.index[0] < out_index.index[0]
        self.path = None
        self.handler_rect = None
        self.triangle_path = None
        self.update_geometries()

    def update_geometries(self):
        if not self.returner:
            self.path = get_connection_path(
                self.in_index.in_plug_center, self.out_index.out_plug_center)
        else:
            out_row_lenght = get_row_lenght(
                self.pattern.pattern, self.out_index.index[0])
            in_row_lenght = get_row_lenght(
                self.pattern.pattern, self.in_index.index[0])
            self.path = get_return_connection_path(
                self._drawcontext,
                out_point=self.out_index.out_plug_center,
                in_point=self.in_index.in_plug_center,
                incol=self.in_index.index[1],
                outcol=self.out_index.index[1],
                out_row_lenght=out_row_lenght,
                in_row_lenght=in_row_lenght,
                max_lenght=get_row_lenght(self.pattern.pattern))
        self.handler_rect = get_connection_handler_rect(
            self._drawcontext,
            self.path,
            returner=self.returner)
        self.triangle_path = connection_handler_path(
            self._drawcontext, self.path, self.returner)

    def is_hovered(self, cursor):
        return self.handler_rect.contains(cursor)

    def draw(self, painter, cursor):
        draw_connection(
            painter,
            self._drawcontext,
            self,
            hover=self.is_hovered(cursor))

    @property
    def strongness(self):
        return get_relationship(
            self.pattern.pattern, self.in_index.index, self.out_index.index)

    def contains(self, index):
        return index in (self.in_index, self.out_index)


class IGPattern(object):
    def __init__(self, pattern, drawcontext=None):
        self._drawcontext = drawcontext or DrawContext()
        self._pattern = pattern
        self._igrows = [
            IGRow(number, len(row), self._drawcontext)
            for number, row in enumerate(self.rows)]
        self._igindexes = [
            IGIndex(index, pattern, self._drawcontext)
            for index in get_existing_indexes(pattern)]
        self._igconnections = [
            IGConnection(
                self, self.igindex(in_index),
                out_index,
                self._drawcontext)
            for out_index in self._igindexes
            for in_index in
            get_out_connected_indexes(pattern, out_index.index)]

    def update_geometries(self):
        for item in self._igindexes + self._igconnections + self._igrows:
            item.update_geometries()

    @property
    def pattern(self):
        return self._pattern

    @property
    def rows(self):
        return self._pattern['quarters']

    def draw(self, painter, cursor):
        for row in self._igrows:
            row.draw(painter, cursor)

        for index in self._igindexes:
            if index.selected:
                for connection in self._igconnections:
                    if connection.contains(index):
                        connection.draw(painter, cursor)

        for index in self._igindexes:
            index.draw(painter, cursor)

    def get_index_action_hovered(self, cursor):
        for index in self._igindexes:
            if index.figure_hovered(cursor):
                return 'figure', index
            if index.behavior_hovered(cursor):
                return 'behavior', index
            if index.selected:
                for connection in self._igconnections:
                    if connection.contains(index):
                        if connection.is_hovered(cursor):
                            return 'connection', connection
        for row in self._igrows:
            if row.plus_is_hovered(cursor):
                return 'row', row
        return None, None

    def set_selected_states(self, cursor):
        for connection in self._igconnections:
            if connection.is_hovered(cursor):
                return
        for index in self._igindexes:
            index.set_selected_state(cursor)

    def select_indexes(self, indexes):
        for igindex in self._igindexes:
            if igindex.index in indexes:
                igindex.selected = True

    def igindex(self, index):
        for i in self._igindexes:
            if i.index == index:
                return i

    def selected_indexes(self):
        return [index for index in self._igindexes if index.selected]
