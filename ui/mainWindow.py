from PyQt5.QtWidgets import QWidget, QTabWidget, QMainWindow
from .searchWindow import SearchWindow

from API.subbank import subbank_add, subbank_delete, subbank_update, subbank_search

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):

        self.setWindowTitle('银行管理系统')
        
        # 定义Tab控件
        tabs = QTabWidget(self)

        #创建选项卡控件
        subbankColumnDefs = ({
            "name": "名字",
            "isPK": True,   # isPK: 删除数据时需要传递该键值
            "type": "string",
        }, {
            "name": "城市",
            "isPK": False,
            "type": "string",
        }, {
            "name": "资产",
            "isPK": False,
            "type": "number",
        })
        self.subbankTab = SearchWindow(subbankColumnDefs, subbank_search, subbank_update, subbank_delete, subbank_add)
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        #将选项卡添加到顶层窗口中
        tabs.addTab(self.subbankTab, "支行管理")
        tabs.addTab(self.tab2, "Tab 2")
        tabs.addTab(self.tab3, "Tab 3")

        # QTabWidget的控件大小
        tabs.resize(900, 700) 
        # 主窗体的大小
        self.resize(950, 750)

