from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox

class InputDataWindow(QWidget):
    def __init__(self, columnsDefs, presetData, okCallback, parent=None):
        # okCallback 点击确认后的回调函数

        super(QWidget, self).__init__(parent)
        self.columnsDefs = columnsDefs
        self.presetData = presetData
        self.okCallback = okCallback
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)


        def createInputItem(column, presetData):
            candidates = column.get("candidates", None)
            if candidates is None:
                return QLineEdit(presetData)
            comboBox = QComboBox()
            comboBox.addItems(candidates)
            for index in range(len(candidates)):
                if candidates[index] == presetData:
                    comboBox.setCurrentIndex(index)
                    break
            return comboBox


        inputs = [ (QLabel(column["name"] + ":"), createInputItem(column, data)) for (column, data) in zip(self.columnsDefs, self.presetData)]
        line = 1
        for input in inputs:
            grid.addWidget(input[0], line, 0)
            grid.addWidget(input[1], line, 1)
            line += 1


        def getInputItemData(inputItem):
            if isinstance(inputItem, QLineEdit):
                return inputItem.text()
            return inputItem.currentText()


        okButton = QPushButton("确认")
        okButton.clicked.connect(lambda : (self.okCallback([getInputItemData(input[1]) for input in inputs]) or self.close()))
        okButton.setDefault(True)
        okButton.setShortcut(QKeySequence.InsertParagraphSeparator)

        cancelButton = QPushButton("取消")
        cancelButton.clicked.connect(self.close)

        grid.addWidget(okButton, line, 0)
        grid.addWidget(cancelButton, line, 1)
        self.setLayout(grid)

