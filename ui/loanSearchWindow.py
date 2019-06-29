from PyQt5.QtWidgets import QPushButton, QInputDialog
from .searchWindow import SearchWindow
from .inputDataWindow import InputDataWindow
from .warningWindow import showWarningWindow
from .dataTypeConvert import convertToInitial

class LoanSearchWindow(SearchWindow):
    def __init__(self, columnDefs, searchFunc, deleteFunc, insertFunc, fundAdd, takeLoan, parent=None):
        super(LoanSearchWindow, self).__init__(columnDefs, searchFunc, lambda : None, deleteFunc, insertFunc, self.initAdditionalButtons(), False, False)
        self.fundAdd = fundAdd
        self.takeLoan = takeLoan

    def initAdditionalButtons(self):
        fundAddButton = QPushButton("发放款项")
        fundAddButton.clicked.connect(self.fundAddHandler)
        takeLoanButton = QPushButton("关联贷款")
        takeLoanButton.clicked.connect(self.takeLoanHandler)
        return [fundAddButton, takeLoanButton]

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
