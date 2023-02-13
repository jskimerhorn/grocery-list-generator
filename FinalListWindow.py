from PyQt5 import QtWidgets, QtGui, QtCore

class FinalListWindow(QtWidgets.QWidget):
    def __init__(self, grocery_list, general_list, parent=None):
        super().__init__(parent)
        self.text_edit = QtWidgets.QTextEdit()
        grocery_text = "\n".join(grocery_list)
        general_text = "\n".join(general_list)
        text = "Items on List\n" + grocery_text + "\n\nGeneral items\n" + general_text
        self.text_edit.setText(text)
        self.text_edit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.text_edit.customContextMenuRequested.connect(self.show_context_menu)
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.text_edit)
        self.setLayout(layout)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("Grocery List")

    def show_context_menu(self, pos):
        menu = self.text_edit.createStandardContextMenu()
        menu.exec_(self.text_edit.mapToGlobal(pos))
        
        self.setWindowFlags(QtCore.Qt.Window)