from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox, QPushButton, QTableWidget, QAbstractItemView, QTableWidgetItem

from .warningWindow import showWarningWindow

class StatisticWindow(QWidget):
    def __init__(self, statistic_search, parent=None):
        super(StatisticWindow, self).__init__(parent)

        self.statistic_search = statistic_search

        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        # 搜索条件输入部分
        grid.addWidget(QLabel("业务:"), 1, 0)
        self.serviceComboBox = QComboBox()
        self.serviceComboBox.addItems(["储蓄", "贷款"])
        grid.addWidget(self.serviceComboBox, 1, 1)
        grid.addWidget(QLabel("年:"), 2, 0)
        self.yearComboBox = QComboBox()
        self.yearComboBox.addItems([ str(x) for x in range(21) ])
        grid.addWidget(self.yearComboBox, 2, 1)
        grid.addWidget(QLabel("月:"), 3, 0)
        self.monthComboBox = QComboBox()
        self.monthComboBox.addItems([ str(x) for x in range(12) ])
        grid.addWidget(self.monthComboBox, 3, 1)

        # 展示表格部分
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels([ "支行", "业务总金额", "用户数" ])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置选择行为，以行为单位
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 设置选择模式，只选择单行
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setFocusPolicy(Qt.NoFocus)
        grid.addWidget(self.table, 4, 0, 5, 0)

        # 统计按钮
        button = QPushButton("统计")
        button.clicked.connect(self.buttonHandler)
        grid.addWidget(button, 9, 2)

        self.setLayout(grid)

    def buttonHandler(self):
        conditions = ({
            "name": "业务",
            "condition": self.serviceComboBox.currentText(),
        }, {
            "name": "时间",
            "condition": f"{self.yearComboBox.currentText()}-{self.monthComboBox.currentText()}",
        })
        try:
            data = self.statistic_search(conditions)
        except Exception as e:
            showWarningWindow(self, e)
            return
        
        self.table.clearContents()
        self.table.setRowCount(len(data))
        for row in range(len(data)):
            for col in range(len(data[row])):
                self.table.setItem(row, col, QTableWidgetItem(str(data[row][col])))
