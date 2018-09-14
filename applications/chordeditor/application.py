

import json
from montunolito.core.chord import deepcopy, get_new_chordgrid
from montunolito.libs.manager import UndoManager, CopyManager
from montunolito.libs.qt.shortcuts import set_shortcut
from montunolito.libs.qt.dialogs import (
    data_lost_question, save_dialog, open_dialog)
from chordeditor.widgets import ChordGridView


TITLE = 'Chord Editor'


class ChordGridEditor():

    def __init__(self, chords):
        self._workingfile = None
        self.title = TITLE
        self.view = ChordGridView(chords)
        self.update_title()
        self._undo_manager = UndoManager(chords, deepcopy)
        self._copy_manager = CopyManager(chords, self.is_index_selected)

        self.view.menu.newRequested.connect(self.new)
        self.view.menu.openRequested.connect(self.open)
        self.view.menu.saveRequested.connect(self.save)
        self.view.menu.addRequested.connect(self.add)
        self.view.menu.deleteRequested.connect(self.delete)
        self.view.menu.cutRequested.connect(self.cut)
        self.view.menu.copyRequested.connect(self.copy)
        self.view.menu.pasteRequested.connect(self.paste)
        self.view.menu.undoRequested.connect(self.undo)
        self.view.menu.redoRequested.connect(self.redo)

        self.view.chordgrid_editor.gridModified.connect(self.modified)
        self.view.chordgrid_editor.lastIndexModified.connect(self._copy_manager.set_index)

        set_shortcut("Ctrl+Z", self.view, self.undo)
        set_shortcut("Ctrl+Y", self.view, self.redo)
        set_shortcut("Ctrl+N", self.view, self.new)
        set_shortcut("Ctrl+S", self.view, self.save)
        set_shortcut("Ctrl+O", self.view, self.open)
        set_shortcut("Ctrl+X", self.view, self.cut)
        set_shortcut("Ctrl+C", self.view, self.copy)
        set_shortcut("Ctrl+V", self.view, self.paste)
        set_shortcut("del", self.view, self.delete)

    @property
    def chordgrid(self):
        return self._undo_manager.data

    def set_title(self, title):
        self.title = title
        self.update_title()

    def update_title(self):
        title = self.title + (" - " + self._workingfile if self._workingfile else "")
        self.view.setWindowTitle(title)

    def set_parentview(self, parent=None):
        self.view.setParent(parent)

    def show(self):
        self.view.show()

    def new(self):
        if self.check_save() is not True:
            return

        chordgrid = get_new_chordgrid()
        self._workingfile = None
        self.view.chordgrid_editor.set_chordgrid(chordgrid)
        self._undo_manager = UndoManager(chordgrid, deepcopy)
        self._copy_manager.set_array(self._undo_manager.data)
        self.update_title()

    def open(self):
        if not self.check_save():
            return

        filename = open_dialog(filter_="mmc")
        if not filename:
            return

        with open(filename, 'r') as f:
            chordgrid = json.load(f)
        self._workingfile = filename
        self.view.chordgrid_editor.set_chordgrid(chordgrid)
        self._undo_manager = UndoManager(chordgrid, deepcopy)
        self._copy_manager.set_array(self._undo_manager.data)
        self.update_title()

    def save(self):
        if self._workingfile is None:
            filename = save_dialog(filter_="mmc")
            if not filename:
                return
            self._workingfile = filename

        with open(self._workingfile, 'w') as f:
            chordgrid = self._undo_manager.data
            json.dump(chordgrid, f, indent=2)

        self._undo_manager.set_data_saved()
        self.update_title()

    def add(self):
        chordgrid = self._undo_manager.data
        chordgrid.extend([None] * 32)
        self.view.chordgrid_editor.set_chordgrid(chordgrid)
        self.modified()

    def delete(self):
        self.view.chordgrid_editor.delete_selection()

    def cut(self):
        chordgrid = self._copy_manager.cut()
        self.view.chordgrid_editor.set_chordgrid(chordgrid)
        self.modified()

    def copy(self):
        self._copy_manager.copy()

    def paste(self):
        data = self._copy_manager.paste()
        if data is not None:
            self.view.chordgrid_editor.set_chordgrid(data)
            self.modified()

    def undo(self):
        self._undo_manager.undo()
        data = self._undo_manager.data
        self.view.chordgrid_editor.set_chordgrid(data)
        self._copy_manager.set_array(data)

    def redo(self):
        self._undo_manager.redo()
        data = self._undo_manager.data
        self.view.chordgrid_editor.set_chordgrid(data)
        self._copy_manager.set_array(data)

    def modified(self):
        data = self.view.chordgrid_editor.chordgrid
        self._undo_manager.set_data_modified(data)
        self._copy_manager.set_array(data)

    def check_save(self):
        if self._undo_manager.data_saved is False:
            result = data_lost_question()
            if result is True:
                self.save()
                return True
            elif result is None:
                return False
        return True

    def is_index_selected(self, index):
        return self.view.chordgrid_editor.is_index_selected(index)
