from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QTableWidget, QAbstractItemView, QPushButton, QHBoxLayout, QCheckBox, QTableWidgetItem, QMessageBox

from .inputDataWindow import InputDataWindow

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

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置选择行为，以行为单位
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 设置选择模式，只选择单行
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setSortingEnabled(True)   # 设置表头可以自动排序

        tableHeight = 5
        grid.addWidget(self.table, line, 0, tableHeight, 0)
        line += tableHeight

        buttons = [ QPushButton(text) for text in ("查询", "新增", "修改", "删除") ]
        for i in range(len(buttons)):
            grid.addWidget(buttons[i], line, i + 2)
        
        buttons[1].clicked.connect(self.showAddWindow)
        buttons[2].clicked.connect(self.showModifyWindow)
        buttons[3].clicked.connect(self.deleteLine)
        self.setLayout(grid)

    def addLine(self, data):
        # table中增加一行
        row = self.table.rowCount()
        self.table.setRowCount(row + 1)
        
        for i in range(len(data)):
            self.table.setItem(row, i, QTableWidgetItem(data[i]))

    def deleteLine(self):
        reply = QMessageBox.question(self, 'Message', '确定删除?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.table.removeRow(self.table.currentRow())

    def modifyData(self, modifyRow, data):
        for col in range(len(data)):
            self.table.item(modifyRow, col).setText(data[col])

    def showAddWindow(self):
        # 展示 新增 窗口
        self.addWindow = InputDataWindow(self.columns, ["" for tmp in self.columns], self.addLine)
        self.addWindow.show()

    def showModifyWindow(self):
        # 展示 修改 窗口
        currentRow = self.table.currentRow()
        if currentRow < 0:
            return
        presetData = [self.table.item(currentRow, col).text() for col in range(self.table.columnCount())]
        self.modifyWindow = InputDataWindow(self.columns, presetData, lambda data:self.modifyData(currentRow, data))
        self.modifyWindow.show()
