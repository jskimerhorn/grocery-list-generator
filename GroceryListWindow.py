import sys
import pickle
from PyQt5 import QtWidgets, QtGui, QtCore
import FinalListWindow
import GroceriesPreviewWindow
from PyQt5.QtWidgets import QApplication
from GroceriesPreviewWindow import GroceriesPreviewWindow


class GroceryListWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Grocery List Generator")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        
        
        self.groceries = {
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
            "Saturday": [],
            "Sunday": [],
            "General": [],
            "Pantry": [],
        }
        
        self.days = list(self.groceries.keys())
        self.current_day = self.days[0]
        
        self.day_combo = QtWidgets.QComboBox(self)
        self.day_combo.addItems(self.days)
        self.day_combo.setCurrentText(self.current_day)
        self.day_combo.currentTextChanged.connect(self.day_changed)
        
        self.item_edit = QtWidgets.QLineEdit(self)
        self.item_edit.returnPressed.connect(self.add_item)
        
        self.item_list = QtWidgets.QListWidget(self)
        self.item_list.installEventFilter(self)
        self.item_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.item_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.item_list.customContextMenuRequested.connect(self.show_context_menu)
        self.update_item_list()
        
        self.add_button = QtWidgets.QPushButton("Add", self)
        self.add_button.clicked.connect(self.add_item)
        
        self.remove_button = QtWidgets.QPushButton("Remove", self)
        self.remove_button.clicked.connect(self.remove_item)
        
        self.generate_button = QtWidgets.QPushButton("Generate Final List", self)
        self.generate_button.clicked.connect(self.generate_final_list)
        
        self.save_button = QtWidgets.QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_groceries)
        
        self.load_button = QtWidgets.QPushButton("Load", self)
        self.load_button.clicked.connect(self.load_groceries)
        
        day_layout = QtWidgets.QHBoxLayout()
        day_layout.addWidget(QtWidgets.QLabel("Day:", self))
        day_layout.addWidget(self.day_combo)
        
        item_layout = QtWidgets.QHBoxLayout()
        item_layout.addWidget(QtWidgets.QLabel("Item:", self))
        item_layout.addWidget(self.item_edit)
        item_layout.addStretch(1)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.generate_button)
        
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(day_layout)
        layout.addLayout(item_layout)
        layout.addWidget(self.item_list)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    

    def generate_grocery_list(self):
        grocery_list = {}
        for day, items in self.groceries.items():
            if day in ["Pantry", "General"]:
                continue
            for item in items:
                if item in grocery_list:
                    grocery_list[item] += 1
                else:
                    grocery_list[item] = 1

        pantry_list = self.groceries.get("Pantry", [])
        for item in pantry_list:
            if item in grocery_list:
                grocery_list[item] -= 1
                if grocery_list[item] == 0:
                    grocery_list.pop(item)

        grocery_result = []
        for item, count in grocery_list.items():
            if count > 0:
                if count > 1:
                    grocery_result.append(f"{item} ({count}x)")
                else:
                    grocery_result.append(item)

        general_list = self.groceries.get("General", [])
        general_count = {}
        for item in general_list:
            if item in general_count:
                general_count[item] += 1
            else:
                general_count[item] = 1

        general_result = []
        for item, count in general_count.items():
            if count > 0:
                if count > 1:
                    general_result.append(f"{item} ({count}x)")
                else:
                    general_result.append(item)

        return grocery_result, general_result
        
    def update_item_list(self):
        items = self.groceries[self.current_day]
        self.item_list.clear()
        self.item_list.addItems(items)
    
    def day_changed(self, day):
        self.current_day = day
        self.update_item_list()
    
    def add_item(self):
        items = self.item_edit.text().split(",")
        for item in items:
            item = item.strip()
            if item:
               self.groceries[self.current_day].append(item)
        self.item_edit.clear()
        self.update_item_list()
    
    def remove_item(self):
        items = self.item_list.selectedItems()
        if items:
            for item in items:
                self.groceries[self.current_day].remove(item.text())
            self.update_item_list()
    
    def generate_final_list(self):
        grocery_list, general_list = self.generate_grocery_list()
        self.list_window = FinalListWindow.FinalListWindow(grocery_list, general_list, parent=self)
        self.list_window.show()
     
   
    
    def copy_all_items(self):
        all_items = [item.text() for item in self.list_window.findItems("*", QtCore.Qt.MatchWildcard)]
        if all_items:
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText("\n".join(all_items))
    
    def save_groceries(self):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Groceries", "", "Pickle Files (*.pkl)")
        if file_name:
            with open(file_name, "wb") as f:
                pickle.dump(self.groceries, f)
    
    def load_groceries(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load Groceries", "", "Pickle Files (*.pkl)")
        if file_name:
            with open(file_name, "rb") as f:
                self.groceries = pickle.load(f)
            self.update_item_list()
            
    def show_context_menu(self, pos):
        menu = QtWidgets.QMenu(self)
        clear_action = menu.addAction("Clear day")
        clear_action.triggered.connect(self.clear_day)
        copy_regular_action = menu.addAction("Copy selection")
        copy_regular_action.triggered.connect(self.copy_selected_items_regularly)        
        copy_action = menu.addAction("Copy selection as list")
        copy_action.triggered.connect(self.copy_selected_items)
        paste_action = menu.addAction("Paste selection")
        paste_action.triggered.connect(self.paste_items)
        paste_week_action = menu.addAction("Paste entire Week")
        paste_week_action.triggered.connect(self.show_week_preview)
        copy_list_text_action = menu.addAction("Export entire list as text")
        copy_list_text_action.triggered.connect(self.copy_list_as_text)
        menu.exec_(self.item_list.mapToGlobal(pos))
        
        
    def generate_text_from_list(self):
        text = []
        for day, items in self.groceries.items():
            items_text = ", ".join(items)
            text.append(f'"{day}": [{items_text}]')
        return "\n".join(text)

    def copy_list_as_text(self):
        text = self.generate_text_from_list()
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(text)
        
    
    def clear_day(self):
        self.groceries[self.current_day] = []
        self.update_item_list()
    
    def copy_selected_items(self):
        selected_items = [item.text() for item in self.item_list.selectedItems()]
        if selected_items:
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText(", ".join(selected_items))
    
    def copy_selected_items_regularly(self):
        selected_items = [item.text() for item in self.item_list.selectedItems()]
        if selected_items:
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText("\n".join(selected_items))
            
    def paste_items(self):
        clipboard = QtWidgets.QApplication.clipboard()
        items = clipboard.text().split(",")
        items = [item.strip() for item in items]
        items = [item for sublist in [item.split("\n") for item in items] for item in sublist]
        self.groceries[self.current_day].extend(items)
        self.update_item_list()  
    
    def parse_and_format_week_text(self):
        clipboard = QtWidgets.QApplication.clipboard()
        text = clipboard.text()
        lines = text.strip().split("\n")
        week = {}
        for line in lines:
            try:
                line = line.strip()
                if line.endswith(","):
                    line = line[:-1]
                day, items = line.split(":")
                day = day.strip().strip('"')
                items = [item.strip().strip('"') for item in items.strip()[1:-1].split(", ")]
                week[day] = items
            except ValueError:
                # if the line cannot be split into two parts, skip it
                continue
        return week

    def show_week_preview(self):
        week = self.parse_and_format_week_text()
        updated_groceries = self.groceries.copy()
        for day, items in week.items():
            if day in updated_groceries:
                updated_groceries[day] += items
            else:
                updated_groceries[day] = items
        self.week_preview = GroceriesPreviewWindow(week, updated_groceries, self)
        self.week_preview.show() 
