import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
                             QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QHeaderView, QMessageBox,
                             QTabWidget, QLabel, QTextEdit)
from PyQt6.QtGui import QFont

from clipdex_gui.dialogs import SnippetDialog

from clipdex_core.snippet_manager import SnippetManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clipdex - Snippet Manager")
        self.setGeometry(300, 300, 500, 600)
        self.setFixedSize(500, 600) # Set the fixed size of the window

        # Initialize the SnippetManager
        self.snippet_manager = SnippetManager()

        # Create tab widget as central widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Create tabs
        self.create_shortcuts_tab()
        self.create_settings_tab()
        self.create_about_tab()

    def create_shortcuts_tab(self):
        """Creates the Shortcuts tab with the existing functionality."""
        shortcuts_widget = QWidget()
        shortcuts_layout = QVBoxLayout(shortcuts_widget)

        # Create the table
        self.table = QTableWidget()
        self.setup_table()
        shortcuts_layout.addWidget(self.table)

        # Buttons layout
        button_layout = QHBoxLayout()
        
        # Create the buttons
        self.add_btn = QPushButton("Add")
        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")

        # Set the height of the buttons
        self.add_btn.setFixedHeight(50)
        self.edit_btn.setFixedHeight(50)
        self.delete_btn.setFixedHeight(50)

        # Add the buttons to the layout
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)
        shortcuts_layout.addLayout(button_layout)

        # Test area
        test_label = QLabel("Test Area:")
        test_label.setStyleSheet("font-weight: bold; margin-top: 10px; font-size: 15px;")
        shortcuts_layout.addWidget(test_label)
        
        self.test_textbox = QTextEdit()
        self.test_textbox.setMaximumHeight(80)
        font = QFont()
        font.setPointSize(15)
        self.test_textbox.setFont(font)
        self.test_textbox.setPlaceholderText("You can test your shortcuts here...")
        shortcuts_layout.addWidget(self.test_textbox)

        # Load the data into the table
        self.populate_table()

        # Connect the buttons to the functions
        self.add_btn.clicked.connect(self.add_snippet)
        self.edit_btn.clicked.connect(self.edit_snippet)
        self.delete_btn.clicked.connect(self.delete_snippet)

        # Add shortcuts tab
        self.tab_widget.addTab(shortcuts_widget, "Shortcuts")

    def create_settings_tab(self):
        """Creates the Settings tab."""
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        
        settings_label = QLabel("Settings")
        settings_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        settings_layout.addWidget(settings_label)
        
        # Placeholder for future settings
        placeholder_label = QLabel("Settings will be added soon...")
        placeholder_label.setStyleSheet("color: gray; margin: 20px;")
        settings_layout.addWidget(placeholder_label)
        
        settings_layout.addStretch()  # Push content to top
        
        self.tab_widget.addTab(settings_widget, "Settings")

    def create_about_tab(self):
        """Creates the About tab."""
        about_widget = QWidget()
        about_layout = QVBoxLayout(about_widget)
        
        about_label = QLabel("About Clipdex")
        about_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        about_layout.addWidget(about_label)
        
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setMaximumHeight(200)
        about_text.setPlainText(
            "Clipdex - Text Expander\n\n"
            "Version: 1.0\n"
            "Text Expander is a tool that allows you to quickly expand your shortcuts.\n\n"
            "Usage:\n"
            "• ':' character to write a shortcut\n"
            "• Space or Enter to expand\n"
            "• Backspace to undo\n\n"
            "This tool is developed with PyQt6 and Python."
        )
        about_layout.addWidget(about_text)
        
        about_layout.addStretch()  # Push content to top
        
        self.tab_widget.addTab(about_widget, "About")

    def setup_table(self):
        """Sets up the table."""
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Shortcut", "Expansion"])

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