from PyQt5 import QtWidgets


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
