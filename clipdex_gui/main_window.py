import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
                             QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QHeaderView, QMessageBox,
                             QTabWidget, QLabel, QTextEdit, QLineEdit, QStyledItemDelegate, QStyleOptionViewItem, QStyle)
from PyQt6.QtGui import QFont

from clipdex_gui.dialogs import SnippetDialog

from clipdex_core.snippet_manager import SnippetManager

# ---------------------------------------------------------------------------
# Hover destekli tablo sınıfları
# ---------------------------------------------------------------------------

class _HoverDelegate(QStyledItemDelegate):
    """Satır üzerinde imleç varken tüm satırı seçim renginde boyamak için özel delegate."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._hovered_row = -1  # Geçerli hover satırı

    # Haricî erişim için setter
    def set_hovered_row(self, row: int):
        if self._hovered_row != row:
            self._hovered_row = row

    # Boyama işlemini özelleştir
    def paint(self, painter, option, index):
        # Eğer bu hücre imleç altındaki satıra aitse, seçili gibi boya
        if index.row() == self._hovered_row:
            opt = QStyleOptionViewItem(option)
            # State_Selected ekleyerek seçili satır tarzını uygula
            opt.state |= QStyle.StateFlag.State_Selected
            super().paint(painter, opt, index)
        else:
            super().paint(painter, option, index)

class HoverTableWidget(QTableWidget):
    """Satır hover özelliği eklenmiş QTableWidget."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Mouse hareketlerini yakalayabilmek için
        self.setMouseTracking(True)

        # Delegate kurulum
        self._delegate = _HoverDelegate(self)
        self.setItemDelegate(self._delegate)

    # İmleç hareketi sırasında satırı güncelle
    def mouseMoveEvent(self, event):
        hovered_row = self.rowAt(event.pos().y())
        self._delegate.set_hovered_row(hovered_row)
        # Görünümü yenile
        vp = self.viewport()
        if vp is not None:
            vp.update()
        super().mouseMoveEvent(event)

    # Tablo dışına çıkınca hover sıfırla
    def leaveEvent(self, event):
        self._delegate.set_hovered_row(-1)
        vp = self.viewport()
        if vp is not None:
            vp.update()
        super().leaveEvent(event)

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

        # Create search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search shortcuts and expansions...")
        self.search_box.setFixedHeight(35)
        self.search_box.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid palette(mid);
                border-radius: 6px;
                background-color: palette(base);
                color: palette(text);
                font-size: 13px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLineEdit:focus {
                border: 2px solid palette(highlight);
            }
        """)
        shortcuts_layout.addWidget(self.search_box)

        # Create the table
        self.table = HoverTableWidget()
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

        self.add_btn.setStyleSheet("font-size: 15px; font-weight: bold;")
        self.edit_btn.setStyleSheet("font-size: 15px; font-weight: bold;")
        self.delete_btn.setStyleSheet("font-size: 15px; font-weight: bold;")

        # Add the buttons to the layout
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)
        shortcuts_layout.addLayout(button_layout)

        # Test area
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
        
        # Connect search box to filter function
        self.search_box.textChanged.connect(self.filter_table)

        # Connection: update font when selection changes
        self.table.itemSelectionChanged.connect(self.update_selected_font)

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
        """Sets up the table with modern styling."""
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Shortcut", "Expansion"])

        # Modern table styling with system theme support
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: palette(mid);
                background-color: palette(base);
                alternate-background-color: palette(alternate-base);
                selection-background-color: palette(highlight);
                selection-color: palette(highlighted-text);
                border: 1px solid palette(mid);
                border-radius: 6px;
                font-size: 13px;
                font-family: 'Segoe UI', Arial, sans-serif;
                outline: none;
            }
            QTableWidget::item {
                padding: 8px 12px;
                border: none;
                color: palette(text);
                min-height: 20px;
                text-align: left;
            }
            QTableWidget::item:selected {
                background-color: palette(highlight);
                color: palette(highlighted-text);
                font: bold 16px;
            }
            QTableWidget::item:selected:alternate {
                background-color: palette(highlight);
                color: palette(highlighted-text);
                font: bold 16px;
            }
            QTableWidget::item:hover {
                background-color: palette(midlight);
            }
            QTableWidget::item:focus {
                background-color: palette(highlight);
                color: palette(highlighted-text);
            }
            QTableWidget::item:focus:alternate {
                background-color: palette(highlight);
                color: palette(highlighted-text);
            }
            QHeaderView::section {
                background-color: palette(button);
                color: palette(button-text);
                padding: 8px 12px;
                border: none;
                border-bottom: 1px solid palette(mid);
                font-weight: 600;
                font-size: 12px;
                text-align: left;
                min-height: 25px;
            }
            QHeaderView::section:hover {
                background-color: palette(midlight);
            }
            QTableWidget::item:alternate {
                background-color: palette(alternate-base);
            }
            QTableWidget::item:selected:!focus {
                background-color: palette(highlight);
                color: palette(highlighted-text);
                font: bold 16px;
            }
            QTableWidget::item:alternate:selected:!focus {
                background-color: palette(highlight);  
                color: palette(highlighted-text);
                font-weight: bold;
            }
        """)

        # Enable alternating row colors
        self.table.setAlternatingRowColors(True)
        
        # Set row height for better readability
        vertical_header = self.table.verticalHeader()
        if vertical_header is not None:
            vertical_header.setDefaultSectionSize(50)  # Increased height for better content visibility
            vertical_header.setVisible(False)  # Hide row numbers

        header = self.table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            header.setStretchLastSection(True)

        self.table.setColumnWidth(0, 200)  # Initial width for the shortcut column
        self.table.setSortingEnabled(True)  # Enable sorting
        
        # Set selection behavior
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        # Force selection highlighting
        self.table.setFocusPolicy(self.table.focusPolicy())

    def populate_table(self):
        """Reads the data from snippets.json and populates the table."""
        self.table.setSortingEnabled(False) # Disable sorting during updates

        snippets = self.snippet_manager.load_snippets()
        self.table.setRowCount(len(snippets))

        row = 0
        for shortcut, expansion in snippets.items():
            shortcut_item = QTableWidgetItem(shortcut)
            expansion_item = QTableWidgetItem(expansion)
            
            # Set text alignment for better readability
            shortcut_item.setTextAlignment(0x0001 | 0x0080)  # Left | VCenter
            expansion_item.setTextAlignment(0x0001 | 0x0080)  # Left | VCenter
            
            self.table.setItem(row, 0, shortcut_item)
            self.table.setItem(row, 1, expansion_item)
            row += 1

        self.table.setSortingEnabled(True) # Re-enable sorting
        self.table.resizeRowsToContents()  # Auto-resize rows to fit content

    def filter_table(self):
        """Filters the table based on search text."""
        search_text = self.search_box.text().lower()
        
        for row in range(self.table.rowCount()):
            shortcut_item = self.table.item(row, 0)
            expansion_item = self.table.item(row, 1)
            
            # Check if search text exists in either shortcut or expansion
            shortcut_text = shortcut_item.text().lower() if shortcut_item else ""
            expansion_text = expansion_item.text().lower() if expansion_item else ""
            
            # Show row if search text is found in either column or if search is empty
            should_show = (search_text == "" or 
                          search_text in shortcut_text or 
                          search_text in expansion_text)
            
            self.table.setRowHidden(row, not should_show)

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

    def update_selected_font(self):
        """Update the font of the selected row to bold"""
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item is None:
                    continue
                font = item.font()
                font.setBold(item.isSelected())
                item.setFont(font)

# Test the main execution block
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())