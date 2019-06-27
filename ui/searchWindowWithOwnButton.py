from PyQt5.QtWidgets import QPushButton, QInputDialog
from .searchWindow import SearchWindow
from .warningWindow import showWarningWindow

class SearchWindowWithOwnButton(SearchWindow):
    def __init__(self, columnDefs, searchFunc, updateFunc, deleteFunc, insertFunc, ownFunc, recordOperator, ownButtonText, ownDialogInfo, parent=None):
        super(SearchWindowWithOwnButton, self).__init__(columnDefs, searchFunc, updateFunc, deleteFunc, insertFunc, recordOperator)
        self.ownFunc = ownFunc
        self.ownButtonText = ownButtonText
        self.ownDialogInfo = ownDialogInfo

        self.initOwnButton()

    def initOwnButton(self):
        ownButton = QPushButton(self.ownButtonText)
        ownButton.clicked.connect(self.ownData)
        self.buttons.insert(0, ownButton)

    def ownData(self):
        linkTargetDialog = QInputDialog()
        linkTarget, ok = linkTargetDialog.getText(self, "input", self.ownDialogInfo)
        if ok:
            data = []
            for col in self.pkIndexes:
                dataType = self.columnDefs[col]["type"]
                data.append(convertToInitial[dataType](self.table.item(self.table.currentRow(), col).text()))
            data.append(linkTarget)
            try:
                self.ownFunc(data)
            except Exception as e:
                showWarningWindow(self, e)
            return
            self.searchData()
