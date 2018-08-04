import json

from montunolito.patterns import PATTERNS
from montunolito.core.pattern import (
    delete_figure_at, get_new_pattern, get_existing_indexes, get_figure_at,
    set_figure_at, get_behaviors_at, set_behaviors_at, get_relationship,
    set_relationship, append_figure_at_row)

from montunolito.libs.qt.manager import DataStreamManager
from montunolito.libs.qt.shortcuts import set_shortcut
from montunolito.libs.qt.dialogs import (
    data_lost_question, save_dialog, open_dialog)
from montunolito.libs.jsonutils import pattern_to_json, json_to_pattern

from widgets import PatternEditorWidget, NewMenu, ThemesMenu
from balloons import FigureBalloon, BehaviorsBalloon, ConnectionBalloon
from themes import THEMES


class PatternEditor():
    def __init__(self):
        self._workingfile = None
        self._widget = PatternEditorWidget(PATTERNS['montuno'])
        self._data_stream_manager = DataStreamManager(PATTERNS['montuno'])

        self._widget.menu.newPatternRequested.connect(self.new)
        self._widget.menu.openPatternRequested.connect(self.open)
        self._widget.menu.savePatternRequested.connect(self.save)
        self._widget.menu.undoRequested.connect(self.undo)
        self._widget.menu.redoRequested.connect(self.redo)
        self._widget.menu.deleteRequested.connect(self.delete_selected_indexes)
        self._widget.menu.themesRequested.connect(self.set_theme)

        self._widget.graph.figureClicked.connect(self.edit_figure)
        self._widget.graph.behaviorClicked.connect(self.edit_behaviors)
        self._widget.graph.connectionClicked.connect(self.edit_connection)
        self._widget.graph.rowClicked.connect(self.append_index_at_row)

        set_shortcut("Ctrl+Z", self._widget, self.undo)
        set_shortcut("Ctrl+Y", self._widget, self.redo)
        set_shortcut("Ctrl+N", self._widget, self.new)
        set_shortcut("Ctrl+S", self._widget, self.save)
        set_shortcut("Ctrl+O", self._widget, self.open)
        set_shortcut("del", self._widget, self.delete_selected_indexes)

    def append_index_at_row(self, row):
        pattern = self._data_stream_manager.pattern
        figure = (0, 0, 0, 0)
        append_figure_at_row(pattern, figure, row)
        self.modified(pattern)

    def edit_figure(self, index, point):
        pattern = self._data_stream_manager.pattern
        figure = get_figure_at(pattern, index)
        balloon = FigureBalloon(figure, parent=self._widget)
        result = balloon.exec_(point)
        if result is True:
            set_figure_at(pattern, index, balloon.figure)
            self.modified(pattern)

    def edit_behaviors(self, index, point):
        pattern = self._data_stream_manager.pattern
        behaviors = get_behaviors_at(pattern, index)
        balloon = BehaviorsBalloon(behaviors, parent=self._widget)
        result = balloon.exec_(point)
        if result is True:
            set_behaviors_at(pattern, index, balloon.behaviors)
            self.modified(pattern)

    def edit_connection(self, in_index, out_index, point):
        pattern = self._data_stream_manager.pattern
        relationship = get_relationship(pattern, in_index, out_index)
        balloon = ConnectionBalloon(relationship, parent=self._widget)
        result = balloon.exec_(point)
        if result is True:
            set_relationship(pattern, in_index, out_index, balloon.value)
            self.modified(pattern)

    def show(self):
        self._widget.show()

    def modified(self, pattern):
        self._data_stream_manager.set_data_modified(pattern)
        self._widget.graph.set_pattern(pattern)

    def new(self):
        result = NewMenu(sorted(list(PATTERNS.keys()))).exec_()
        if self.check_save() is not True:
            return
        pattern = PATTERNS[result] if result else get_new_pattern()
        self._workingfile = None
        self._data_stream_manager = DataStreamManager(pattern)
        self._widget.graph.set_pattern(pattern)

    def open(self):
        if not self.check_save():
            return
        filename = open_dialog()
        if not filename:
            return
        with open(filename, 'r') as f:
            pattern = json.load(f)
            pattern = json_to_pattern(pattern)
        self._workingfile = filename
        self.modified(pattern)
        self._data_stream_manager = DataStreamManager(pattern)

    def save(self):
        if self._workingfile is None:
            filename = save_dialog()
            if not filename:
                return
            self._workingfile = filename
        with open(self._workingfile, 'w') as f:
            p = pattern_to_json(self._data_stream_manager.pattern)
            json.dump(p, f, indent=2)
        self._data_stream_manager.set_data_saved()

    def undo(self):
        self._data_stream_manager.undo()
        self._widget.graph.set_pattern(self._data_stream_manager.pattern)

    def redo(self):
        self._data_stream_manager.redo()
        self._widget.graph.set_pattern(self._data_stream_manager.pattern)

    def check_save(self):
        if self._data_stream_manager.data_saved is False:
            result = data_lost_question()
            if result is True:
                self.save()
                return True
            elif result is None:
                return False
        return True

    def delete_selected_indexes(self):
        indexes = [
            i.index for i in self._widget.graph.pattern.selected_indexes()]
        # delete by the last index to avoid reindexing durange the procedure
        # and avoid crashes with multi selected indexes delete
        indexes = [i for i in reversed(sorted(indexes))]
        if not indexes:
            return
        pattern = self._data_stream_manager.pattern
        for index in indexes:
            delete_figure_at(pattern, index)
        self._data_stream_manager.set_data_modified(pattern)
        self._widget.graph.set_pattern(pattern)

    def set_theme(self):
        theme = ThemesMenu(sorted(list(THEMES.keys()))).exec_()
        self._widget.set_theme(theme)
