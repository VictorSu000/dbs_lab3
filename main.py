import sys
from PyQt5.QtWidgets import QApplication

from ui.mainWindow import MainWindow
         
app = QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
