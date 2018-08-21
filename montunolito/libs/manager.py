

class CopyManager():

    def __init__(self, array, selection_checker):
        self._array = array
        self._selection_checker = selection_checker
        self._index = None
        self._clipboard = []

    def set_array(self, array):
        self._array = array

    def set_index(self, index):
        self._index = index

    def cut(self):
        self.copy()
        return [
            e if self._selection_checker(i) is False else None
            for i, e in enumerate(self._array)]

    def copy(self):
        self._clipboard = [
            (i, e) for i, e in enumerate(self._array)
            if self._selection_checker(i)]

    def paste(self):
        if not self._clipboard:
            return

        offset = self._clipboard[-1][0] - self._clipboard[0][0]
        array = [False for _ in range(offset + 1)]
        for i, e in self._clipboard:
            array[i - self._clipboard[0][0]] = e

        insert_index = self._index or len(self._array)
        for elt in array:
            if elt is False:
                if insert_index > len(self._array) - 1:
                    self._array.append(None)
                insert_index += 1
                continue
            if insert_index < len(self._array) - 1:
                self._array[insert_index] = elt
            else:
                self._array.append(elt)
            insert_index += 1
        self._index = insert_index

        return self._array[:]



class UndoManager():
    def __init__(self, data, copier):
        self._copier = copier
        self._current_state = data
        self._modified = False
        self._undo_stack = []
        self._redo_stack = []

    @property
    def data(self):
        return self._copier(self._current_state)

    def undo(self):
        if not self._undo_stack:
            return
        self._redo_stack.append(self._copier(self._current_state))
        self._current_state = self._copier(self._undo_stack[-1])
        del self._undo_stack[-1]

    def redo(self):
        if not self._redo_stack:
            return

        self._undo_stack.append(self._copier(self._current_state))
        self._current_state = self._copier(self._redo_stack[-1])
        del self._redo_stack[-1]

    def set_data_modified(self, pattern):
        self._redo_stack = []
        self._undo_stack.append(self._copier(self._current_state))
        self._current_state = self._copier(pattern)
        self._modified = True

    def set_data_saved(self):
        self._modified = False

    @property
    def data_saved(self):
        return not self._modified
