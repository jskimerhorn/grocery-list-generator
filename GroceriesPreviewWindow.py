from PyQt5 import QtWidgets, QtGui, QtCore
import pickle
class GroceriesPreviewWindow(QtWidgets.QDialog):
    def __init__(self, week, groceries, parent):
        super().__init__(parent)
        self.week = week
        self.groceries = groceries
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.setWindowTitle("Week Preview")
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        layout.addWidget(self.list_widget)
        self.update_list_widget()
        button_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(button_layout)
        accept_button = QtWidgets.QPushButton("Accept")
        accept_button.clicked.connect(self.accept_groceries)
        button_layout.addWidget(accept_button)
        reject_button = QtWidgets.QPushButton("Reject")
        reject_button.clicked.connect(self.reject)
        button_layout.addWidget(reject_button)
        copy_button = QtWidgets.QPushButton("Copy")
        copy_button.clicked.connect(self.copy_selected_items)
        button_layout.addWidget(copy_button)

    def update_list_widget(self):
        self.list_widget.clear()
        all_days = set(self.week.keys()).union(self.groceries.keys())
        for day in all_days:
            items = self.groceries.get(day, []) + self.week.get(day, [])
            self.list_widget.addItem(f"{day}: {items}")

    def accept_groceries(self):
        self.parent.groceries = self.groceries
        self.parent.update_item_list()
        self.accept()

    def copy_selected_items(self):
        selected_items = self.list_widget.selectedItems()
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.clear()
        if selected_items:
           selected_text = "\n".join([item.text() for item in selected_items])
           clipboard.setText(selected_text)