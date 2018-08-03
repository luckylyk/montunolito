from PyQt5 import QtWidgets
import os

def data_lost_question():
    message = (
        'Some datas will be lost\n'
        'Do you wan\'t to save before continue?')

    buttons = (
        QtWidgets.QMessageBox.Yes |
        QtWidgets.QMessageBox.No |
        QtWidgets.QMessageBox.Cancel)

    result = QtWidgets.QMessageBox.question(
        None,
        'Pattern is not Save',
        message,
        buttons=buttons,
        defaultButton=QtWidgets.QMessageBox.Yes)

    if result == QtWidgets.QMessageBox.Yes:
        return True
    elif result == QtWidgets.QMessageBox.No:
        return False
    return None


def save_dialog(path=None):
    filenames = QtWidgets.QFileDialog.getSaveFileName(
        None,
        caption='Save pattern',
        directory=path or os.path.expanduser("~"),
        filter='*.json')
    filename = filenames[0]
    if not filename:
        return
    if not filename.lower().endswith(".json"):
        filename += ".json"
    return filename


def open_dialog(path=None):
    filenames = QtWidgets.QFileDialog.getOpenFileName(
        None,
        caption='Save pattern',
        directory=path or os.path.expanduser("~"),
        filter='*.json')
    return filenames[0]