
from montunolito.core.pattern import (
    get_index_occurence_probablity, get_existing_indexes, get_figure_at,
    get_out_connected_indexes, get_connection_strongness)

from coordinates import (
    get_index_behavior_rect, get_index_figure_rect, get_index_inplug_rect,
    get_index_outplug_rect, get_index_body_rect, get_row_rect, get_index_rect,
    get_connection_path, get_connection_handler_rect, shrink_rect)
from draws import draw_index, draw_row_background, draw_connection
from figure import Figure


class IGIndex(object):
    def __init__(self, index, pattern):
        self.pattern = pattern
        self.index = index

        self._rect = get_index_rect(*index)
        self._inplug_rect = get_index_inplug_rect(self._rect)
        self._outplug_rect = get_index_outplug_rect(self._rect)
        self._body_rect = get_index_body_rect(self._rect)
        self._figure_rect = get_index_figure_rect(self._body_rect)
        self._behavior_rect = get_index_behavior_rect(self._body_rect)

        self._figure = Figure(self.figure(), shrink_rect(self._figure_rect,5))

        self._rects = [
            self._inplug_rect,
            self._outplug_rect,
            self._body_rect,
            self._figure_rect,
            self._behavior_rect]

        self.selected = False

    @property
    def occurence(self):
        return get_index_occurence_probablity(self.pattern, self.index)

    @property
    def out_plug_center(self):
        return self._outplug_rect.center()

    @property
    def in_plug_center(self):
        return self._inplug_rect.center()

    @property
    def out_connected_indexes(self):
        return get_out_connected_indexes(self.pattern, self.index)

    def highlight_rects(self, cursor):
        return [rect for rect in self._rects if rect.contains(cursor)]

    def figure(self):
        return get_figure_at(self.pattern, self.index)

    def figure_hovered(self, cursor):
        return self._figure_rect.contains(cursor)

    def behavior_hovered(self, cursor):
        return self._behavior_rect.contains(cursor)

    def set_selected_state(self, cursor):
        if not self.selected:
            self.selected = (
                self._body_rect.contains(cursor) and
                not self._figure_rect.contains(cursor) and
                not self._behavior_rect.contains(cursor))
        else:
            self.selected = self._rect.contains(cursor)

    def draw(self, painter, cursor):
        draw_index(
            painter,
            self.occurence,
            self._inplug_rect,
            self._outplug_rect,
            self._body_rect,
            self._figure_rect,
            self._behavior_rect,
            selected=self.selected,
            highlight_rects=self.highlight_rects(cursor))
        self._figure.draw(painter, cursor, hoverable=False)


class IGConnection(object):
    def __init__(self, pattern, in_index, out_index):
        self.pattern = pattern
        self.in_index = in_index
        self.out_index = out_index
        self._path = get_connection_path(
            in_index.in_plug_center, out_index.out_plug_center)
        self._handler_rect = get_connection_handler_rect(self._path)

    def is_hovered(self, cursor):
        return self._handler_rect.contains(cursor)

    def draw(self, painter, cursor):
        draw_connection(
            painter, self._path, self._handler_rect,
            hover=self.is_hovered(cursor))

    def strongness(self):
        return get_connection_strongness(
            self.pattern.pattern, self.in_index.index, self.out_index.index)

    def contains(self, index):
        return index in (self.in_index, self.out_index)


class IGPattern(object):
    def __init__(self, pattern):
        self._pattern = pattern
        self._indexes = [
            IGIndex(index, pattern) for index in get_existing_indexes(pattern)]
        self._connections = [
            IGConnection(self, self.index(in_index), out_index)
            for out_index in self._indexes
            for in_index in
            get_out_connected_indexes(pattern, out_index.index)]

    @property
    def pattern(self):
        return self._pattern

    @property
    def rows(self):
        return self._pattern['quarters']

    def draw(self, painter, cursor):
        for row_number, row in enumerate(self.rows):
            row_rect = get_row_rect(row_number, len(row))
            hover = row_rect.contains(cursor)
            draw_row_background(painter, row_rect, row_number + 1, hover)

        for index in self._indexes:
            if index.selected:
                for connection in self._connections:
                    if connection.contains(index):
                        connection.draw(painter, cursor)

        for index in self._indexes:
            index.draw(painter, cursor)

    def get_index_action_hovered(self, cursor):
        for index in self._indexes:
            if index.figure_hovered(cursor):
                return 'fingerstate', index
            if index.behavior_hovered(cursor):
                return 'behavior', index
            if index.selected:
                for connection in self._connections:
                    if connection.contains(index):
                        if connection.is_hovered(cursor):
                            return 'connection', connection
        return None, None

    def set_selected_states(self, cursor):
        for connection in self._connections:
            if connection.is_hovered(cursor):
                return
        for index in self._indexes:
            index.set_selected_state(cursor)

    def index(self, index):
        for i in self._indexes:
            if i.index == index:
                return i