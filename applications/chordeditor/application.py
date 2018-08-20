

import json
from montunolito.core.chord import deepcopy, get_new_chordgrid
from montunolito.libs.qt.manager import DataStreamManager
from montunolito.libs.qt.shortcuts import set_shortcut
from montunolito.libs.qt.dialogs import (
    data_lost_question, save_dialog, open_dialog)
from widgets import ChordGridView


class ChordGridEditor():
    def __init__(self, chords):
        self._workingfile = None
        self._view = ChordGridView(chords)
        self._data_stream_manager = DataStreamManager(chords, deepcopy)

        self._view.menu.newRequested.connect(self.new)
        self._view.menu.openRequested.connect(self.open)
        self._view.menu.saveRequested.connect(self.save)
        self._view.menu.addRequested.connect(self.add)
        self._view.menu.deleteRequested.connect(self.delete)
        self._view.menu.cutRequested.connect(self.cut)
        self._view.menu.copyRequested.connect(self.copy)
        self._view.menu.pasteRequested.connect(self.paste)
        self._view.menu.undoRequested.connect(self.undo)
        self._view.menu.redoRequested.connect(self.redo)

        self._view.chordgrid_editor.gridModified.connect(self.modified)

        set_shortcut("Ctrl+Z", self._view, self.undo)
        set_shortcut("Ctrl+Y", self._view, self.redo)
        set_shortcut("Ctrl+N", self._view, self.new)
        set_shortcut("Ctrl+S", self._view, self.save)
        set_shortcut("Ctrl+O", self._view, self.open)
        set_shortcut("Ctrl+X", self._view, self.cut)
        set_shortcut("Ctrl+C", self._view, self.copy)
        set_shortcut("Ctrl+V", self._view, self.paste)
        set_shortcut("del", self._view, self.delete)

    def show(self):
        self._view.show()

    def new(self):
        if self.check_save() is not True:
            return
        print('new')
        chordgrid = get_new_chordgrid()
        self._workingfile = None
        self._view.chordgrid_editor.set_chordgrid(chordgrid)
        self._data_stream_manager = DataStreamManager(chordgrid, deepcopy)

    def open(self):
        if not self.check_save():
            return
        filename = open_dialog()
        if not filename:
            return
        with open(filename, 'r') as f:
            chordgrid = json.load(f)
        self._workingfile = filename
        self._view.chordgrid_editor.set_chordgrid(chordgrid)
        self._data_stream_manager = DataStreamManager(chordgrid, deepcopy)

    def save(self):
        if self._workingfile is None:
            filename = save_dialog()
            if not filename:
                return
            self._workingfile = filename
        with open(self._workingfile, 'w') as f:
            chordgrid = self._data_stream_manager.data
            json.dump(chordgrid, f, indent=2)
        self._data_stream_manager.set_data_saved()

    def add(self):
        chordgrid = self._data_stream_manager.data
        chordgrid.extend([None] * 32)
        self._view.chordgrid_editor.set_chordgrid(chordgrid)
        self.modified()

    def delete(self):
        self._view.chordgrid_editor.delete_selection()

    def cut(self):
        pass

    def copy(self):
        pass

    def paste(self):
        pass

    def undo(self):
        self._data_stream_manager.undo()
        data = self._data_stream_manager.data
        self._view.chordgrid_editor.set_chordgrid(data)

    def redo(self):
        self._data_stream_manager.redo()
        data = self._data_stream_manager.data
        self._view.chordgrid_editor.set_chordgrid(data)

    def modified(self):
        data = self._view.chordgrid_editor.chordgrid
        self._data_stream_manager.set_data_modified(data)

    def check_save(self):
        if self._data_stream_manager.data_saved is False:
            result = data_lost_question()
            if result is True:
                self.save()
                return True
            elif result is None:
                return False
        return True