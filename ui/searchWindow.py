from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QTableWidget, QAbstractItemView, QPushButton

from .addWindow import AddWindow

class SearchWindow(QWidget):
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

        table = QTableWidget()
        table.setColumnCount(len(self.columns))
        table.setHorizontalHeaderLabels(self.columns)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSortingEnabled(True)   # 设置表头可以自动排序

        tableHeight = 5
        grid.addWidget(table, line, 0, tableHeight, 0)
        line += tableHeight

        buttons = [ QPushButton(text) for text in ("查询", "增加", "删除", "保存") ]
        for i in range(len(buttons)):
            grid.addWidget(buttons[i], line, i + 2)
        
        buttons[1].clicked.connect(self.showAddWindow)
        self.setLayout(grid)

    def showAddWindow(self):
        self.addWindow = AddWindow(columns=self.columns)
        self.addWindow.show()