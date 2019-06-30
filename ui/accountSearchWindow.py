from PyQt5.QtWidgets import QPushButton, QInputDialog, QTableWidgetItem
from datetime import datetime

from .searchWindow import SearchWindow
from .warningWindow import showWarningWindow
from .dataTypeConvert import convertToInitial

class AccountSearchWindow(SearchWindow):
    def __init__(self, columnDefs, searchFunc, updateFunc, deleteFunc, insertFunc, ownFunc, searchOwnerFunc, parent=None):
        super(AccountSearchWindow, self).__init__(columnDefs, searchFunc, updateFunc, deleteFunc, insertFunc, self.initAdditionalButtons(), True)
        self.ownFunc = ownFunc
        self.searchOwnerFunc = searchOwnerFunc

    def initAdditionalButtons(self):
        self.searchOwnerButton = QPushButton("查询所有者")
        self.searchOwnerButton.clicked.connect(self.searchOwner)
        ownButton = QPushButton("绑定客户")
        ownButton.clicked.connect(self.ownAccount)
        self.searchOwnerButtonIndex = 0
        return [self.searchOwnerButton, ownButton]

    def ownAccount(self):
        if self.table.currentRow() < 0:
            showWarningWindow(self, "请先选择某个数据！")
            return
        clientDialog = QInputDialog()
        client, ok = clientDialog.getText(self, "input", "请输入客户身份证号：")
        if ok:
            data = [ client ]
            for col in self.pkIndexes:
                dataType = self.columnDefs[col]["type"]
                data.append(convertToInitial[dataType](self.table.item(self.table.currentRow(), col).text()))
            try:
                self.ownFunc(data)
            except Exception as e:
                showWarningWindow(self, e)
            return
            self.searchData()

    def searchOwner(self):
        if self.table.currentRow() < 0:
            showWarningWindow(self, "请先选择某个数据！")
            return
        data = []
        for col in self.pkIndexes:
            dataType = self.columnDefs[col]["type"]
            data.append(convertToInitial[dataType](self.table.item(self.table.currentRow(), col).text()))
        
        try:
            result = self.searchOwnerFunc(data)
        except Exception as e:
            showWarningWindow(self, e)
            return

        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels([ "账户号", "身份证号", "最近访问日期" ])
        self.table.clearContents()
        self.table.setRowCount(len(result))
        for row in range(len(result)):
            self.table.setItem(row, 0, QTableWidgetItem(str(result[row][0])))
            self.table.setItem(row, 1, QTableWidgetItem(str(result[row][1])))
            self.table.setItem(row, 2, QTableWidgetItem(result[row][2].strftime("%Y-%m-%d")))
        self.toggleButtons([self.searchOwnerButtonIndex])
        self.searchOwnerButton.setText("返回")
        self.searchOwnerButton.clicked.disconnect(self.searchOwner)
        self.searchOwnerButton.clicked.connect(self.getBack)

    def getBack(self):
        self.table.setColumnCount(len(self.columnDefs))
        self.table.setHorizontalHeaderLabels([ column["name"] for column in self.columnDefs ])
        self.toggleButtons([self.searchOwnerButtonIndex])
        self.searchOwnerButton.setText("查询所有者")
        self.searchOwnerButton.clicked.disconnect(self.getBack)
        self.searchOwnerButton.clicked.connect(self.searchOwner)
        self.searchData()
