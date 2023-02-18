import sys
import pickle
import ast
from PyQt5 import QtWidgets, QtGui, QtCore
import FinalListWindow
from PyQt5.QtWidgets import QApplication
import GroceriesPreviewWindow
from GroceriesPreviewWindow import GroceriesPreviewWindow
import sqlite3


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
        
        self.recipes_button = QtWidgets.QPushButton("Recipes", self)
        self.recipes_button.clicked.connect(self.open_recipe_database)
        
        day_layout = QtWidgets.QHBoxLayout()
        day_layout.addWidget(QtWidgets.QLabel("Day:", self))
        day_layout.addWidget(self.day_combo)
        
        item_layout = QtWidgets.QHBoxLayout()
        item_layout.addWidget(QtWidgets.QLabel("Item:", self))
        item_layout.addWidget(self.item_edit)
        item_layout.addStretch(1)
        item_layout.addWidget((self.recipes_button))

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
                if item == "\n":
                    # ignore newline characters
                    continue
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
            else:
                self.groceries[self.current_day].append("\n")
        self.item_edit.clear()
        self.update_item_list()
    
    def remove_item(self):
        items = self.item_list.selectedItems()
        if items:
            for item in items:
                row = self.item_list.row(item)
                self.groceries[self.current_day].pop(row)
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
            
    def add_blank_line(self):
        self.groceries[self.current_day].append("\n")
        self.update_item_list() 
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_C and event.modifiers() == QtCore.Qt.ControlModifier:
            self.copy_selected_items()
        elif event.key() == QtCore.Qt.Key_V and event.modifiers() == QtCore.Qt.ControlModifier:
            self.paste_items()
        elif event.key() in [QtCore.Qt.Key_Delete, QtCore.Qt.Key_Backspace]:
            self.remove_item()    
        else:
            super().keyPressEvent(event)        
            
    def show_context_menu(self, pos):
        menu = QtWidgets.QMenu(self)

        cut_action = menu.addAction("Cut")
        cut_action.triggered.connect(self.cut_selected_items)
        copy_regular_action = menu.addAction("Copy selection")
        copy_regular_action.triggered.connect(self.copy_selected_items_regularly)        
        copy_action = menu.addAction("Copy selection as list")
        copy_action.triggered.connect(self.copy_selected_items)
        paste_action = menu.addAction("Paste selection")
        paste_action.triggered.connect(self.paste_items)
        paste_week_action = menu.addAction("Paste entire Week")
        paste_week_action.triggered.connect(self.show_week_preview)
        clear_action = menu.addAction("Clear day")
        clear_action.triggered.connect(self.clear_day)
        copy_list_text_action = menu.addAction("Export entire list as text")
        copy_list_text_action.triggered.connect(self.copy_list_as_text)
        add_to_pantry_action = menu.addAction("Add to Pantry")
        add_to_pantry_action.triggered.connect(self.add_selected_to_pantry)
        remove_pantry_action = menu.addAction("Remove from Pantry")
        remove_pantry_action.triggered.connect(self.remove_selected_from_pantry)
        blank_line_action = menu.addAction("Add blank line")
        blank_line_action.triggered.connect(self.add_blank_line)
        add_heading_action = menu.addAction("Add Heading")
        add_heading_action.triggered.connect(self.add_heading)
        

        menu.exec_(self.item_list.mapToGlobal(pos))
        
    def cut_selected_items(self):
        self.copy_selected_items()
        self.remove_item()
        
    def remove_selected_from_pantry(self):
        selected_items = [item.text() for item in self.item_list.selectedItems()]
        pantry_list = self.groceries.get("Pantry", [])
        for item in selected_items:
            if item in pantry_list:
                pantry_list.remove(item)
        self.groceries["Pantry"] = pantry_list
        self.update_item_list()    
        
    def add_selected_to_pantry(self):
        items = [item.text() for item in self.item_list.selectedItems()]
        if items:
            self.groceries["Pantry"].extend(items)    
        
    def generate_text_from_list(self):
        text = []
        for day, items in self.groceries.items():
            items_text = ", ".join(items)
            text.append(f'"{day}": [{items_text}]')
        return "\n".join(text)

    def copy_list_as_text(self):
        week_text = ""
        for day, items in self.groceries.items():
            week_text += f'{day}: [{", ".join(repr(item) for item in items)}],\n'
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(week_text)
        
    
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
        for item in items:
            if item == '':
                self.add_blank_line()
            else:
                self.groceries[self.current_day].append(item)
        self.update_item_list()  

    def add_heading(self):
        heading, ok = QtWidgets.QInputDialog.getText(self, "Add Heading", "Enter Heading:")
        if ok:
            self.groceries[self.current_day].append(heading)
            self.groceries["Pantry"].append(heading)
            # Add a new line after the heading
            self.groceries[self.current_day].append("\n")

            self.update_item_list()
            
            
    def add_recipe_heading(self, title):
        self.groceries[self.current_day].append(title)
        self.groceries["Pantry"].append(title)
        # Add a new line after the heading
        self.groceries[self.current_day].append("\n")
            
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
                items = [ast.literal_eval(item.strip()) for item in items.strip()[1:-1].split(", ")]
                week[day] = items
            except (ValueError, SyntaxError):
                # if the line cannot be split into two parts or if the item is not a valid expression, skip it
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
        
    def open_recipe_database(self):
        RecipeDatabaseWindow.recipe_database_window = RecipeDatabaseWindow(self)
        RecipeDatabaseWindow.recipe_database_window.show()

class RecipeDatabaseWindow(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.grocery_list_window = parent
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Recipe Database")
        self.setWindowIcon(QtGui.QIcon("icon.png"))

        # Create a layout for the recipe database window
        layout = QtWidgets.QVBoxLayout()

        # Add a label and a list widget to display the recipes
        self.recipes_label = QtWidgets.QLabel("Recipes:", self)
        layout.addWidget(self.recipes_label)

        self.recipe_list = QtWidgets.QListWidget(self)
        titles = self.get_recipe_titles("recipes.db")
        for title in titles:
            self.recipe_list.addItem(title)
        layout.addWidget(self.recipe_list)

        # Create a horizontal layout for the buttons
        buttons_layout = QtWidgets.QHBoxLayout()

        # Add the Import button
        self.import_button = QtWidgets.QPushButton("Import", self)
        self.import_button.clicked.connect(self.add_recipe)
        buttons_layout.addWidget(self.import_button)
        
         # Add the Delete button
        self.delete_button = QtWidgets.QPushButton("Delete", self)
        self.delete_button.clicked.connect(self.delete_recipe)
        buttons_layout.addWidget(self.delete_button)
        
        # Add the Export button
        self.export_button = QtWidgets.QPushButton("Export", self)
        self.export_button.clicked.connect(self.export_recipe)
        buttons_layout.addWidget(self.export_button)

        # Add the buttons layout to the main layout
        layout.addLayout(buttons_layout)

        self.setLayout(layout)
        self.setWindowFlags(QtCore.Qt.Window)
        
    
        
    def add_recipe(self):
        # Create the dialog
        dialog = AddRecipeDialog(self)

        # Show the dialog and wait for the user to accept or reject it
        result = dialog.exec_()

        # If the user accepted the dialog, insert the recipe into the database
        if result == QtWidgets.QDialog.Accepted:
            title = dialog.title_input.text()
            ingredients = dialog.ingredients_input.text()

            # Connect to the SQLite database
            conn = sqlite3.connect("recipes.db")
            c = conn.cursor()

            # Insert the recipe data into the database
            c.execute("INSERT INTO recipes (title, ingredients) VALUES (?, ?)", (title, ingredients))
            conn.commit()

            # Close the database connection
            conn.close()

            # Update the recipe list
            titles = self.get_recipe_titles("recipes.db")
            self.recipe_list.clear()
            self.recipe_list.addItems(titles)
            
    def get_recipe_titles(self, recipes_db):
        conn = sqlite3.connect(recipes_db)
        c = conn.cursor()
        c.execute("SELECT title FROM recipes")
        titles = [row[0] for row in c.fetchall()]
        conn.close()
        return titles
        
    def export_recipe(self):
        selected = self.recipe_list.selectedItems()
        if selected:
            selected_item = selected[0]
            title = selected_item.text()
            ingredients = self.get_ingredients(title)
            self.grocery_list_window.groceries[self.grocery_list_window.current_day].append(title)
            self.grocery_list_window.groceries["Pantry"].append(title)
            # Add a new line after the heading
            self.grocery_list_window.groceries[self.grocery_list_window.current_day].append("\n")
            for ingredient in ingredients.split(','):
                self.grocery_list_window.groceries[self.grocery_list_window.current_day].append(ingredient)
            self.grocery_list_window.groceries[self.grocery_list_window.current_day].append("\n")
            self.grocery_list_window.update_item_list()
            
    

    def get_ingredients(self, title):
        conn = sqlite3.connect("recipes.db")
        c = conn.cursor()
        c.execute("SELECT ingredients FROM recipes WHERE title=?", (title,))
        ingredients = c.fetchone()[0]
        conn.close()
        return ingredients
        
    def delete_recipe(self):
        # Get the currently selected recipe
        selected = self.recipe_list.selectedItems()
        if not selected:
            # If no recipe is selected, do nothing
            return

        selected_item = selected[0]
        title = selected_item.text()

        # Show a confirmation dialog to confirm deletion
        confirmation = QtWidgets.QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete the recipe \"{title}\"?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if confirmation == QtWidgets.QMessageBox.Yes:
            # Connect to the SQLite database
            conn = sqlite3.connect("recipes.db")
            c = conn.cursor()

            # Delete the selected recipe from the database
            c.execute("DELETE FROM recipes WHERE title=?", (title,))
            conn.commit()

            # Close the database connection
            conn.close()

            # Update the recipe list
            self.recipe_list.takeItem(self.recipe_list.row(selected_item))

            # Clear the grocery list if the deleted recipe is in it
            if title in self.grocery_list_window.groceries[self.grocery_list_window.current_day]:
                self.grocery_list_window.groceries[self.grocery_list_window.current_day].remove(title)
                self.grocery_list_window.update_item_list()


        

class AddRecipeDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the title and ingredients inputs
        self.title_input = QtWidgets.QLineEdit()
        self.ingredients_input = QtWidgets.QLineEdit()

        # Create the layout for the inputs
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Title:"))
        layout.addWidget(self.title_input)
        layout.addWidget(QtWidgets.QLabel("Ingredients:"))
        layout.addWidget(self.ingredients_input)

        # Create the OK and Cancel buttons
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        # Set the layout for the dialog
        self.setLayout(layout)


