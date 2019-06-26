from PyQt5.QtWidgets import QMessageBox

def showWarningWindow(widget, exception):
    return QMessageBox.warning(widget, "Warning", str(exception))
