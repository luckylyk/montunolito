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
        'File is not saved',
        message,
        buttons=buttons,
        defaultButton=QtWidgets.QMessageBox.Yes)

    if result == QtWidgets.QMessageBox.Yes:
        return True
    elif result == QtWidgets.QMessageBox.No:
        return False
    return None


def save_dialog(path=None, filter_=None):
    filter_ = '*.' + filter_ if filter_ else '*.json'
    filenames = QtWidgets.QFileDialog.getSaveFileName(
        None,
        caption='Save file',
        directory=path or os.path.expanduser("~"),
        filter=filter_)
    filename = filenames[0]
    if not filename:
        return
    end = filter_[1:]
    if not filename.lower().endswith(end):
        filename += end
    return filename


def open_dialog(path=None, filter_=None):
    filter_ = '*.' + filter_ if filter_ else '*.json'
    filenames = QtWidgets.QFileDialog.getOpenFileName(
        None,
        caption='Open file',
        directory=path or os.path.expanduser("~"),
        filter=filter_)
    return filenames[0]


def invalid_file_dialog(path):
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle("Invalid file")
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText('file is invalid : \n{}'.format(path))
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()


def check_pattern_dialog(result, details):
    if result:
        icon = QtWidgets.QMessageBox.Information
        text = "The pattern is valid"
    else:
        icon = QtWidgets.QMessageBox.Critical
        text = "The pattern is broken !"

    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle("Pattern check")
    msg.setIcon(icon)
    msg.setText(text)
    msg.setDetailedText(details)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()