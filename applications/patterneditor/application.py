
from widgets import PatternEditorWidget, NewMenu
from manager import DataStreamManager
from dialogs import data_lost_question
from balloons import FigureBalloon, BehaviorsBalloon, ConnectionBalloon
from montunolito.patterns import PATTERNS
from montunolito.core.pattern import (
    delete_figure_at, get_new_pattern, get_existing_indexes, get_figure_at,
    set_figure_at, get_behaviors_at, set_behaviors_at, get_relationship,
    set_relationship, append_figure_at_row)


class PatternEditor():
    def __init__(self):
        self._widget = PatternEditorWidget(PATTERNS['montuno'])
        self._data_stream_manager = DataStreamManager(PATTERNS['montuno'])

        self._widget.menu.newPatternRequested.connect(self.new_pattern)
        self._widget.menu.openPatternRequested.connect(self.open_pattern)
        self._widget.menu.savePatternRequested.connect(self.save_pattern)
        self._widget.menu.undoRequested.connect(self.undo)
        self._widget.menu.redoRequested.connect(self.redo)
        self._widget.menu.deleteRequested.connect(self.delete_selected_indexes)

        self._widget.graph.figureClicked.connect(self.edit_figure)
        self._widget.graph.behaviorClicked.connect(self.edit_behaviors)
        self._widget.graph.connectionClicked.connect(self.edit_connection)
        self._widget.graph.rowClicked.connect(self.append_index_at_row)

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

    def undo(self):
        self._data_stream_manager.undo()
        self._widget.graph.set_pattern(self._data_stream_manager.pattern)

    def redo(self):
        self._data_stream_manager.redo()
        self._widget.graph.set_pattern(self._data_stream_manager.pattern)

    def new_pattern(self):
        result = NewMenu(sorted(list(PATTERNS.keys()))).exec_()
        if self.check_save() is not True:
            return
        pattern = PATTERNS[result] if result else get_new_pattern()
        self._data_stream_manager = DataStreamManager(pattern)
        self._widget.graph.set_pattern(pattern)

    def check_save(self):
        if self._data_stream_manager.data_saved is False:
            result = data_lost_question()
            if result is True:
                self.save_pattern()
                return True
            elif result is None:
                return False
        return True

    def open_pattern(self):
        if not self.check_save():
            return

    def save_pattern(self):
        self._data_stream_manager.set_data_saved()

    def delete_selected_indexes(self):
        indexes = [
            i.index for i in self._widget.graph.pattern.selected_indexes()]
        if not indexes:
            return
        pattern = self._data_stream_manager.pattern
        for index in indexes:
            delete_figure_at(pattern, index)
        self._data_stream_manager.set_data_modified(pattern)
        self._widget.graph.set_pattern(pattern)

