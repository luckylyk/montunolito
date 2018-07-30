
from widgets import PatternEditorWidget
from manager import DataStreamManager
from dialogs import data_lost_question
from montunolito.patterns import PATTERNS
from montunolito.core.pattern import (
    delete_figure_at, get_new_pattern, get_existing_indexes)


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

    def show(self):
        self._widget.show()

    def undo(self):
        self._data_stream_manager.undo()
        self._widget.graph.set_pattern(self._data_stream_manager.pattern)

    def redo(self):
        self._data_stream_manager.redo()
        self._widget.graph.set_pattern(self._data_stream_manager.pattern)

    def new_pattern(self):
        if self.check_save() is not True:
            return
        self._data_stream_manager = DataStreamManager(get_new_pattern())
        self._widget.graph.set_pattern(get_new_pattern())

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

