from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QTableWidget, QAbstractItemView, QPushButton, QHBoxLayout, QCheckBox, QTableWidgetItem, QMessageBox, QInputDialog

from .inputDataWindow import InputDataWindow
from .warningWindow import showWarningWindow

from .dataTypeConvert import convertToInitial, convertToText

class SearchWindow(QWidget):
    def __init__(self, columnDefs, searchFunc, updateFunc, deleteFunc, insertFunc, additionalButtons, recordOperator=False, showUpdateButton=True, parent=None):
        super(SearchWindow, self).__init__(parent)
        self.columnDefs = columnDefs
        self.searchFunc = searchFunc
        self.updateFunc = updateFunc
        self.deleteFunc = deleteFunc
        self.insertFunc = insertFunc

        self.recordOperator = recordOperator
        self.showUpdateButton = showUpdateButton
        self.additionalButtons = additionalButtons
        # pkIndexes 调用删除函数时，需要传的字段(一般是主键)在columnDefs中的下标
        self.pkIndexes = [ index for index in range(len(columnDefs)) if columnDefs[index]["isPK"] ]
        self.initUI()
        self.searchData()

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        line = 1
        self.searchInputs = []
        for column in self.columnDefs:
            grid.addWidget(QLabel(column["name"] + ":"), line, 0)
            searchInputWidget = QLineEdit()
            self.searchInputs.append(searchInputWidget)
            grid.addWidget(searchInputWidget, line, 1)
            line += 1

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.columnDefs))
        self.table.setHorizontalHeaderLabels([ column["name"] for column in self.columnDefs ])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置选择行为，以行为单位
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 设置选择模式，只选择单行
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setFocusPolicy(Qt.NoFocus)

        tableHeight = 5
        grid.addWidget(self.table, line, 0, tableHeight, 0)
        line += tableHeight

        self.offset = len(self.additionalButtons)
        self.buttons = self.additionalButtons
        self.buttons += [ QPushButton(text) for text in ("查询", "新增", "删除") ]
        if self.showUpdateButton:
            self.buttons.append(QPushButton("修改"))

        for i in range(len(self.buttons)):
            grid.addWidget(self.buttons[i], line, i + 2)
        
        self.buttons[self.offset].clicked.connect(self.searchData)
        self.buttons[self.offset + 1].clicked.connect(self.showAddWindow)
        self.buttons[self.offset + 2].clicked.connect(self.deleteLine)
        if self.showUpdateButton:
            self.buttons[self.offset + 3].clicked.connect(self.showModifyWindow)
        self.setLayout(grid)

    def searchData(self):
        conditions = []
        for index in range(len(self.searchInputs)):
            name = self.columnDefs[index]["name"]
            condition = self.searchInputs[index].text()
            if condition != "":
                conditions.append({
                    "name": name,
                    "condition": condition,
                })

        try:
            data = self.searchFunc(conditions)
        except Exception as e:
            showWarningWindow(self, e)
            return

        self.table.clearContents()
        self.table.setRowCount(len(data))
        for row in range(len(data)):
            for col in range(len(data[row])):
                dataType = self.columnDefs[col]["type"]
                self.table.setItem(row, col, QTableWidgetItem(convertToText[dataType](data[row][col])))

    def addLine(self, data):
        try:
            self.insertFunc(data)
        except Exception as e:
            showWarningWindow(self, e)
            return

        self.searchData()

    def deleteLine(self):
        if self.table.currentRow() < 0:
            showWarningWindow(self, "请先选择某个数据！")
            return

        reply = QMessageBox.question(self, 'Message', '确定删除?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            data = []
            for col in self.pkIndexes:
                dataType = self.columnDefs[col]["type"]
                data.append(convertToInitial[dataType](self.table.item(self.table.currentRow(), col).text()))

            try:
                self.deleteFunc(data)
            except Exception as e:
                showWarningWindow(self, e)
                return
                
            self.searchData()

    def modifyData(self, modifyRow, data):
        dataToSend = []
        for col in self.pkIndexes:
            dataType = self.columnDefs[col]["type"]
            dataToSend.append(convertToInitial[dataType](self.table.item(modifyRow, col).text()))

        dataToSend += data

        if self.recordOperator:
            operatorDialog = QInputDialog()
            operator, ok = operatorDialog.getText(self, "input", "请输入操作员身份证号：")
            if ok:
                dataToSend.insert(0, operator)
            else:
                return

        try:
            self.updateFunc(dataToSend)
        except Exception as e:
            showWarningWindow(self, e)
            return

        self.searchData()

    def showAddWindow(self):
        # 展示 新增 窗口
        self.addWindow = InputDataWindow(self.columnDefs, ["" for tmp in self.columnDefs], self.addLine)
        self.addWindow.show()

    def showModifyWindow(self):
        # 展示 修改 窗口
        currentRow = self.table.currentRow()
        if currentRow < 0:
            showWarningWindow(self, "请先选择某个数据！")
            return
        presetData = [self.table.item(currentRow, col).text() for col in range(self.table.columnCount())]
        self.modifyWindow = InputDataWindow(self.columnDefs, presetData, lambda data:self.modifyData(currentRow, data))
        self.modifyWindow.show()

    def toggleButtons(self, ignoreButtonIndexes):
        # 切换按钮（查询、新增、删除、修改）的状态（可用<->不可用）
        # ignoreButtonIndexes 不切换的按钮index
        for index in range(len(self.buttons)):
            if index not in ignoreButtonIndexes:
                self.buttons[index].setEnabled(not self.buttons[index].isEnabled())
