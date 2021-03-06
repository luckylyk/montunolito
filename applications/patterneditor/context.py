from patterneditor.themes import THEMES


class DrawContext(object):
    def __init__(self):
        self._size_multiplier = 1
        self._size_increase_factor = 1.1
        self.colors = THEMES['default']

    def size(self, size):
        return size * self._size_multiplier

    def increase_size(self):
        if self._size_multiplier < 2:
            self._size_multiplier *= self._size_increase_factor

    def decrease_size(self):
        if self._size_multiplier > .5:
            self._size_multiplier /= self._size_increase_factor

    def reset_size(self):
        self._size_multiplier = 1

    def set_theme(self, theme):
        new_theme = {k: v for k, v in THEMES['default'].items()}
        new_theme.update(THEMES[theme])
        self.colors = new_theme
