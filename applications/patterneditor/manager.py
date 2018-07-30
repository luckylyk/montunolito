from montunolito.core.pattern import deepcopy


class DataStreamManager():
    def __init__(self, pattern):
        self._current_state = pattern.copy()
        self._modified = False
        self._undo_stack = []
        self._redo_stack = []

    @property
    def pattern(self):
        return deepcopy(self._current_state)

    def undo(self):
        if not self._undo_stack:
            return
        self._redo_stack.append(deepcopy(self._current_state))
        self._current_state = deepcopy(self._undo_stack[-1])
        del self._undo_stack[-1]

    def redo(self):
        if not self._redo_stack:
            return

        self._undo_stack.append(deepcopy(self._current_state))
        self._current_state = deepcopy(self._redo_stack[-1])
        del self._redo_stack[-1]

    def set_data_modified(self, pattern):
        self._redo_stack = []
        self._undo_stack.append(deepcopy(self._current_state))
        self._current_state = deepcopy(pattern)
        self._modified = True

    def set_data_saved(self):
        self._modified = False

    @property
    def data_saved(self):
        return not self._modified
