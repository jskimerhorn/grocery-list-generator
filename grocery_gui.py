import sys
from PyQt5 import QtWidgets
from GroceryListWindow import GroceryListWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = GroceryListWindow()
    window.show()
    sys.exit(app.exec_())