
from coordinates import (
    get_slider_segmented_line_path, get_slider_handler_path,
    get_slider_handler_rect)
from draws import draw_slider_path


class Slider(object):
    def __init__(self, rect, value=5, max=10):
        self.rect = rect
        self.value = value
        self._segmented_line_path = \
            get_slider_segmented_line_path(rect, max+1)
        self._value_rects = [
            get_slider_handler_rect(rect, v, max) for v in range(max + 1)]
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
        draw_slider_path(painter, self._segmented_line_path, hover=False)
        hovered = self.hovered_value(cursor) == self.value
        draw_slider_path(
            painter,
            self._value_path,
            hover=hovered,
            background=True,
            pressed=pressed)