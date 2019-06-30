from PyQt5.QtWidgets import QPushButton, QInputDialog, QTableWidgetItem
from .searchWindow import SearchWindow
from .inputDataWindow import InputDataWindow
from .warningWindow import showWarningWindow
from .dataTypeConvert import convertToInitial

class LoanSearchWindow(SearchWindow):
    def __init__(self, columnDefs, searchFunc, deleteFunc, insertFunc, fundAdd, takeLoan, fundSearch, takeLoanSearch, parent=None):
        super(LoanSearchWindow, self).__init__(columnDefs, searchFunc, lambda : None, deleteFunc, insertFunc, self.initAdditionalButtons(), False, False)
        self.fundAdd = fundAdd
        self.takeLoan = takeLoan
        self.fundSearch = fundSearch
        self.takeLoanSearch = takeLoanSearch

    def initAdditionalButtons(self):
        self.fundSearchButton = QPushButton("款项查询")
        self.fundSearchButton.clicked.connect(self.fundSearchHandler)
        self.takeLoanSearchButton = QPushButton("贷款关联查询")
        self.takeLoanSearchButton.clicked.connect(self.takeLoanSearchHandler)
        fundAddButton = QPushButton("发放款项")
        fundAddButton.clicked.connect(self.fundAddHandler)
        takeLoanButton = QPushButton("关联贷款")
        takeLoanButton.clicked.connect(self.takeLoanHandler)
        self.fundSearchButtonIndex = 0
        self.takeLoanSearchButtonIndex = 1
        return [self.fundSearchButton, self.takeLoanSearchButton, fundAddButton, takeLoanButton]

    def callFundAdd(self, data):
        dataToSend = []
        for col in self.pkIndexes:
            dataType = self.columnDefs[col]["type"]
            dataToSend.append(convertToInitial[dataType](self.table.item(self.table.currentRow(), col).text()))
        try:
            self.fundAdd(dataToSend + data)
        except Exception as e:
            showWarningWindow(self, e)
            return
        self.searchData()

    def fundAddHandler(self):
        if self.table.currentRow() < 0:
            showWarningWindow(self, "请先选择某个数据！")
            return
        fundAddDefs = ({
            "name": "日期",
            "type": "date",
        }, {
            "name": "金额",
            "type": "number",
        })
        
        self.fundAddWindow = InputDataWindow(fundAddDefs, ["" for tmp in fundAddDefs], lambda data : self.callFundAdd(data))
        self.fundAddWindow.show()

    def takeLoanHandler(self):
        if self.table.currentRow() < 0:
            showWarningWindow(self, "请先选择某个数据！")
            return
        clientDialog = QInputDialog()
        client, ok = clientDialog.getText(self, "input", "请输入身份证号：")
        if ok:
            data = []
            for col in self.pkIndexes:
                dataType = self.columnDefs[col]["type"]
                data.append(convertToInitial[dataType](self.table.item(self.table.currentRow(), col).text()))
            data.append(client)
            try:
                self.takeLoan(data)
            except Exception as e:
                showWarningWindow(self, e)
            return
            self.searchData()


    def fundSearchHandler(self):
        if self.table.currentRow() < 0:
            showWarningWindow(self, "请先选择某个数据！")
            return
        data = []
        for col in self.pkIndexes:
            dataType = self.columnDefs[col]["type"]
            data.append(convertToInitial[dataType](self.table.item(self.table.currentRow(), col).text()))
        
        try:
            result = self.fundSearch(data)
        except Exception as e:
            showWarningWindow(self, e)
            return

        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([ "贷款号", "款项号", "日期", "金额" ])
        self.table.clearContents()
        self.table.setRowCount(len(result))
        for row in range(len(result)):
            self.table.setItem(row, 0, QTableWidgetItem(str(result[row][0])))
            self.table.setItem(row, 1, QTableWidgetItem(str(result[row][1])))
            self.table.setItem(row, 2, QTableWidgetItem(result[row][2].strftime("%Y-%m-%d")))
            self.table.setItem(row, 3, QTableWidgetItem(str(result[row][3])))
        self.toggleButtons([self.fundSearchButtonIndex])
        self.fundSearchButton.setText("返回")
        self.fundSearchButton.clicked.disconnect(self.fundSearchHandler)
        self.fundSearchButton.clicked.connect(self.fundSearchGetBack)

    def fundSearchGetBack(self):
        self.table.setColumnCount(len(self.columnDefs))
        self.table.setHorizontalHeaderLabels([ column["name"] for column in self.columnDefs ])
        self.toggleButtons([self.fundSearchButtonIndex])
        self.fundSearchButton.setText("款项查询")
        self.fundSearchButton.clicked.disconnect(self.fundSearchGetBack)
        self.fundSearchButton.clicked.connect(self.fundSearchHandler)
        self.searchData()

    def takeLoanSearchHandler(self):
        if self.table.currentRow() < 0:
            showWarningWindow(self, "请先选择某个数据！")
            return
        data = []
        for col in self.pkIndexes:
            dataType = self.columnDefs[col]["type"]
            data.append(convertToInitial[dataType](self.table.item(self.table.currentRow(), col).text()))
        
        try:
            result = self.takeLoanSearch(data)
        except Exception as e:
            showWarningWindow(self, e)
            return

        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels([ "贷款号", "身份证号" ])
        self.table.clearContents()
        self.table.setRowCount(len(result))
        for row in range(len(result)):
            for col in range(len(result[row])):
                self.table.setItem(row, col, QTableWidgetItem(str(result[row][col])))
        self.toggleButtons([self.takeLoanSearchButtonIndex])
        self.takeLoanSearchButton.setText("返回")
        self.takeLoanSearchButton.clicked.disconnect(self.takeLoanSearchHandler)
        self.takeLoanSearchButton.clicked.connect(self.takeLoanSearchGetBack)

    def takeLoanSearchGetBack(self):
        self.table.setColumnCount(len(self.columnDefs))
        self.table.setHorizontalHeaderLabels([ column["name"] for column in self.columnDefs ])
        self.toggleButtons([self.takeLoanSearchButtonIndex])
        self.takeLoanSearchButton.setText("贷款关联查询")
        self.takeLoanSearchButton.clicked.disconnect(self.takeLoanSearchGetBack)
        self.takeLoanSearchButton.clicked.connect(self.takeLoanSearchHandler)
        self.searchData()