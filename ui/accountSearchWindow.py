from PyQt5.QtWidgets import QPushButton, QInputDialog
from .searchWindow import SearchWindow
from .warningWindow import showWarningWindow
from .dataTypeConvert import convertToInitial

class AccountSearchWindow(SearchWindow):
    def __init__(self, columnDefs, searchFunc, updateFunc, deleteFunc, insertFunc, ownFunc, parent=None):
        super(AccountSearchWindow, self).__init__(columnDefs, searchFunc, updateFunc, deleteFunc, insertFunc, self.initOwnButton(), True)
        self.ownFunc = ownFunc

    def initOwnButton(self):
        ownButton = QPushButton("绑定客户")
        ownButton.clicked.connect(self.ownAccount)
        return [ownButton]

    def ownAccount(self):
        clientDialog = QInputDialog()
        client, ok = clientDialog.getText(self, "input", "请输入客户身份证号：")
        if ok:
            data = []
            for col in self.pkIndexes:
                dataType = self.columnDefs[col]["type"]
                data.append(convertToInitial[dataType](self.table.item(self.table.currentRow(), col).text()))
            data.append(client)
            try:
                self.ownFunc(data)
            except Exception as e:
                showWarningWindow(self, e)
            return
            self.searchData()
