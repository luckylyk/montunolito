
from montunolito.core.pattern import (
    get_index_occurence_probablity, get_existing_indexes, get_figure_at,
    get_out_connected_indexes, get_relationship, get_behaviors_at,
    get_row_lenght)

from context import DrawContext
from painting import draw_index, draw_row_background, draw_connection, draw_mas, draw_row_plus
from figure import IGFigure
from geometries import (
    get_index_behavior_rect, get_index_figure_rect, get_index_inplug_rect,
    get_index_outplug_rect, get_index_body_rect, get_row_rect, get_index_rect,
    get_connection_path, get_connection_handler_rect, shrink_rect,
    get_mas_rects, get_row_body_rect, get_row_plus_rect, get_row_body_path,
    connection_handler_path, get_return_connection_path)


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
        draw_index(painter, self, highlight_rects=self.highlight_rects(cursor))
        self._igfigure.draw(painter, cursor, hoverable=False)
        draw_mas(painter, self._mas_rects, **self.behaviors)


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
            self._body_path,
            self.is_hovered(cursor))
        draw_row_plus(
            painter,
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
            self.path)
        self.triangle_path = connection_handler_path(
            self._drawcontext, self.path, self.returner)

    def is_hovered(self, cursor):
        return self.handler_rect.contains(cursor)

    def draw(self, painter, cursor):
        draw_connection(painter, self, hover=self.is_hovered(cursor))

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