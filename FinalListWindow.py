from PyQt5 import QtWidgets, QtGui, QtCore

class FinalListWindow(QtWidgets.QWidget):
    def __init__(self, final_list, parent=None):
        super().__init__(parent)
        self.text_edit = QtWidgets.QTextEdit()
        text = "\n".join(final_list)
        text = "# Items on List\nGeneral items\n" + text
        self.text_edit.setText(text)
        self.text_edit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.text_edit.customContextMenuRequested.connect(self.show_context_menu)
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.text_edit)
        self.setLayout(layout)
        self.setWindowFlags(QtCore.Qt.Window)

    def show_context_menu(self, pos):
        menu = self.text_edit.createStandardContextMenu()
        menu.exec_(self.text_edit.mapToGlobal(pos))