from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton

class AddWindow(QWidget):
    def __init__(self, parent=None, columns=()):
        super(QWidget, self).__init__(parent)
        self.columns = columns
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        line = 1
        for column in self.columns:
            grid.addWidget(QLabel(column + ":"), line, 0)
            grid.addWidget(QLineEdit(), line, 1)
            line += 1

        okButton = QPushButton("取消")
        okButton.clicked.connect(self.close)

        grid.addWidget(okButton, line, 0)
        self.setLayout(grid)

