from PyQt5.QtWidgets import QWidget, QTabWidget, QMainWindow
from .searchWindow import SearchWindow

from API.subbank import subbank_add, subbank_delete, subbank_update, subbank_search
from API.employee import employee_add, employee_delete, employee_update, employee_search
from API.client import client_add, client_delete, client_update, client_search

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
        #将选项卡添加到顶层窗口中
        tabs.addTab(self.subbankTab, "支行管理")

        employeeColumnDefs = ({
            "name": "身份证号",
            "isPK": True,
            "type": "string",
        }, {
            "name": "姓名",
            "isPK": False,
            "type": "string",
        }, {
            "name": "联系电话",
            "isPK": False,
            "type": "string",
        }, {
            "name": "家庭住址",
            "isPK": False,
            "type": "string",
        }, {
            "name": "开始工作日期",
            "isPK": False,
            "type": "date",
        }, {
            "name": "支行名字",
            "isPK": False,
            "type": "string",
        })
        self.employeeTab = SearchWindow(employeeColumnDefs, employee_search, employee_update, employee_delete, employee_add)
        tabs.addTab(self.employeeTab, "员工管理")

        clientColumnDefs = ({
            "name": "身份证号",
            "isPK": True,
            "type": "string",
        }, {
            "name": "姓名",
            "isPK": False,
            "type": "string",
        }, {
            "name": "联系电话",
            "isPK": False,
            "type": "string",
        }, {
            "name": "家庭住址",
            "isPK": False,
            "type": "string",
        }, {
            "name": "联系人姓名",
            "isPK": False,
            "type": "string",
        }, {
            "name": "联系人电话",
            "isPK": False,
            "type": "string",
        }, {
            "name": "联系人邮箱",
            "isPK": False,
            "type": "string",
        }, {
            "name": "关系",
            "isPK": False,
            "type": "string",
        })
        self.clientTab = SearchWindow(clientColumnDefs, client_search, client_update, client_delete, client_add)
        tabs.addTab(self.clientTab, "客户管理")

        # QTabWidget的控件大小
        tabs.resize(900, 700) 
        # 主窗体的大小
        self.resize(950, 750)

