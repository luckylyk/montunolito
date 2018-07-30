import os
from geometries import get_button_menu_rect, shrink_rect
from painting import get_icon, draw_icon


ICONDIR = os.path.dirname(__file__)
def icon(filename):
    return os.path.join(ICONDIR, 'icons', filename)


class MenuItem():
    def __init__(self, rect, pixmap, mirror=False):
        self.icon = get_icon(pixmap, mirror)
        self._rect = shrink_rect(rect, 12)
        self.hovered = False
        self._clicked = False

    def set_clicked_state(self, cursor, state=None):
        if state is None:
            self._clicked = self._rect.contains(cursor)
        else:
            self._clicked = state

    def set_hovered_state(self, cursor):
        self.hovered = self._rect.contains(cursor)

    def draw(self, painter):
        draw_icon(painter, self.icon, self._rect, self.hovered, self._clicked)


class Menu():
    def __init__(self, rect):
        self._new = MenuItem(get_button_menu_rect(rect, 0), icon('new.png'))
        self._save = MenuItem(get_button_menu_rect(rect, 1), icon('open.png'))
        self._open = MenuItem(get_button_menu_rect(rect, 2), icon('save.png'))
        self._undo = MenuItem(get_button_menu_rect(rect, 3), icon('undo.ico'))
        self._redo = MenuItem(
            get_button_menu_rect(rect, 4), icon('undo.ico'), mirror=True)
        self._trash = MenuItem(
            get_button_menu_rect(rect, 5), icon('trash.png'))

        self._items = (
            self._new,
            self._save,
            self._open,
            self._undo,
            self._redo,
            self._trash)

    def set_clicked_states(self, cursor, state=None):
        for item in self._items:
            item.set_clicked_state(cursor, state)

    def hovered_index(self):
        for i, item in enumerate(self._items):
            if item.hovered is True:
                return i

    def set_hovered_states(self, cursor):
        for item in self._items:
            item.set_hovered_state(cursor)

    def draw(self, painter):
        for item in self._items:
            item.draw(painter)
