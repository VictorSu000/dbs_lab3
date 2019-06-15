from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton

class InputDataWindow(QWidget):
    def __init__(self, columns, presetData, okCallback, parent=None):
        # okCallback 点击确认后的回调函数

        super(QWidget, self).__init__(parent)
        self.columns = columns
        self.presetData = presetData
        self.okCallback = okCallback
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        inputs = [ (QLabel(column + ":"), QLineEdit(data)) for (column, data) in zip(self.columns, self.presetData)]
        line = 1
        for input in inputs:
            grid.addWidget(input[0], line, 0)
            grid.addWidget(input[1], line, 1)
            line += 1

        okButton = QPushButton("确认")
        okButton.clicked.connect(lambda : (self.okCallback([input[1].text() for input in inputs]) or self.close()))
        okButton.setDefault(True)
        okButton.setShortcut(QKeySequence.InsertParagraphSeparator)

        cancelButton = QPushButton("取消")
        cancelButton.clicked.connect(self.close)

        grid.addWidget(okButton, line, 0)
        grid.addWidget(cancelButton, line, 1)
        self.setLayout(grid)

