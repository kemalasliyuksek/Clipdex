import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
                             QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QHeaderView, QMessageBox)

from clipdex_gui.dialogs import SnippetDialog

from clipdex_core.snippet_manager import SnippetManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clipdex - Snippet Manager")
        self.setGeometry(300, 300, 800, 500)

        # Initialize the SnippetManager
        self.snippet_manager = SnippetManager()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        self.main_layout = QVBoxLayout(self.central_widget)

        # Create the table
        self.table = QTableWidget()
        self.setup_table()
        self.main_layout.addWidget(self.table)

        # Buttons layout
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add")
        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")

        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)
        self.main_layout.addLayout(button_layout)

        # Load the data into the table
        self.populate_table()

        # Connect the buttons to the functions
        self.add_btn.clicked.connect(self.add_snippet)
        self.edit_btn.clicked.connect(self.edit_snippet)
        self.delete_btn.clicked.connect(self.delete_snippet)

    def setup_table(self):
        """Sets up the table."""
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Shortcut", "Expansion"])

        # QHeaderView None gelirse linter uyarısını önlemek için kontrol
        header = self.table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        self.table.setColumnWidth(0, 200)  # Initial width for the shortcut column
        self.table.setSortingEnabled(True)  # Enable sorting

    def populate_table(self):
        """Reads the data from snippets.json and populates the table."""
        self.table.setSortingEnabled(False) # Disable sorting during updates

        snippets = self.snippet_manager.load_snippets()
        self.table.setRowCount(len(snippets))

        row = 0
        for shortcut, expansion in snippets.items():
            self.table.setItem(row, 0, QTableWidgetItem(shortcut))
            self.table.setItem(row, 1, QTableWidgetItem(expansion))
            row += 1

        self.table.setSortingEnabled(True) # Re-enable sorting

    def add_snippet(self):
        """Opens the new snippet dialog."""
        dialog = SnippetDialog(self)
        if dialog.exec():  # .exec() opens the dialog and returns True if the user clicks OK
            data = dialog.get_data()
            if not data["shortcut"] or not data["expansion"]:
                QMessageBox.warning(self, "Warning", "Shortcut and text fields cannot be left blank.")
                return

            snippets = self.snippet_manager.load_snippets()
            snippets[data["shortcut"]] = data["expansion"]
            self.snippet_manager.save_snippets(snippets)
            self.populate_table()  # Refresh the table

    def edit_snippet(self):
        """Opens the edit snippet dialog."""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a shortcut to edit.")
            return

        item_shortcut = self.table.item(current_row, 0)
        item_expansion = self.table.item(current_row, 1)

        if item_shortcut is None or item_expansion is None:
            QMessageBox.warning(self, "Warning", "Selected row is invalid.")
            return

        old_shortcut = item_shortcut.text()
        expansion = item_expansion.text()

        dialog = SnippetDialog(self, shortcut=old_shortcut, expansion=expansion)
        if dialog.exec():
            data = dialog.get_data()
            if not data["shortcut"] or not data["expansion"]:
                QMessageBox.warning(self, "Warning", "Shortcut and text fields cannot be left blank.")
                return

            snippets = self.snippet_manager.load_snippets()
            # Delete the old shortcut (if it was changed)
            if old_shortcut in snippets:
                del snippets[old_shortcut]

            snippets[data["shortcut"]] = data["expansion"]
            self.snippet_manager.save_snippets(snippets)
            self.populate_table()

    def delete_snippet(self):
        """Deletes the selected shortcut."""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a shortcut to delete.")
            return

        item_shortcut = self.table.item(current_row, 0)
        if item_shortcut is None:
            QMessageBox.warning(self, "Warning", "Selected row is invalid.")
            return

        shortcut = item_shortcut.text()

        reply = QMessageBox.question(self, "Delete Confirmation",
                                     f"'{shortcut}' shortcut to delete?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            snippets = self.snippet_manager.load_snippets()
            if shortcut in snippets:
                del snippets[shortcut]
                self.snippet_manager.save_snippets(snippets)
                self.populate_table()

# Test the main execution block
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())