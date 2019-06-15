from PyQt5.QtWidgets import QWidget, QTabWidget, QMainWindow
from .searchWindow import SearchWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):

        self.setWindowTitle('银行管理系统')
        
        # 定义Tab控件
        tabs = QTabWidget(self)

        #创建选项卡小控件窗口
        self.tab1 = SearchWindow(columns=("aaa", "bbb"))
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        #将选项卡添加到顶层窗口中
        tabs.addTab(self.tab1, "支行管理")
        tabs.addTab(self.tab2, "Tab 2")
        tabs.addTab(self.tab3, "Tab 3")

        # QTabWidget的控件大小
        tabs.resize(900, 700) 
        # 主窗体的大小
        self.resize(950, 750)

