import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
                             QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QHeaderView, QMessageBox,
                             QTabWidget, QLabel, QTextEdit, QLineEdit, QStyledItemDelegate, QStyleOptionViewItem, QStyle,
                             QSystemTrayIcon, QMenu)
from PyQt6.QtGui import QFont, QMouseEvent, QAction, QIcon
from PyQt6.QtCore import QEvent
from PyQt6.QtCore import QModelIndex
from PyQt6.QtCore import Qt
from pathlib import Path
from PyQt6.QtCore import QSize

from clipdex_gui.dialogs import SnippetDialog

from clipdex_core.snippet_manager import SnippetManager

class _HoverDelegate(QStyledItemDelegate):
    """Custom delegate to paint the entire row in selection color when cursor is hovering over it."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._hovered_row = -1  # Current hovered row


    def set_hovered_row(self, row: int):
        if self._hovered_row != row:
            self._hovered_row = row

    # Customize the painting process
    def paint(self, painter, option, index):
        # If this cell is under the cursor, paint it in selection color
        if index.row() == self._hovered_row:
            opt = QStyleOptionViewItem(option)
            # Add State_Selected to apply the selected row style
            opt.state |= QStyle.StateFlag.State_Selected
            super().paint(painter, opt, index)
        else:
            super().paint(painter, option, index)

class HoverTableWidget(QTableWidget):
    """QTableWidget with row hover feature."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # To catch mouse movements
        self.setMouseTracking(True)

        # Setup delegate
        self._delegate = _HoverDelegate(self)
        self.setItemDelegate(self._delegate)

    # Update the row when the cursor moves
    def mouseMoveEvent(self, event):
        hovered_row = self.rowAt(event.pos().y())
        self._delegate.set_hovered_row(hovered_row)
        # Refresh the view
        vp = self.viewport()
        if vp is not None:
            vp.update()
        super().mouseMoveEvent(event)

    # Clear hover when the table is left
    def leaveEvent(self, event):
        self._delegate.set_hovered_row(-1)
        vp = self.viewport()
        if vp is not None:
            vp.update()
        super().leaveEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Apply the proper application icon before anything else
        self._setup_app_icon()
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

        # Setup system tray (goes before installing global event filter so tray is ready)
        self._setup_tray_icon()

        # To catch any click on any widget, install a global event filter
        app_instance = QApplication.instance()
        if app_instance is not None:
            app_instance.installEventFilter(self)

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

        # Label that shows total shortcut count
        self.count_label = QLabel()
        self.count_label.setStyleSheet("color: gray; font-size: 11px; margin: 4px;")
        shortcuts_layout.addWidget(self.count_label)

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
        """Creates the About tab with a modern label-based layout (no text box)."""
        about_widget = QWidget()
        about_layout = QVBoxLayout(about_widget)

        # Header
        title_label = QLabel("Clipdex – Snippet Manager")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 12px;")
        about_layout.addWidget(title_label)

        # Short description
        intro_label = QLabel(
            "Clipdex; frequently used text snippets can be written in seconds with shortcuts. It is a modern <b>text expander</b> application.")
        intro_label.setWordWrap(True)
        intro_label.setStyleSheet("margin: 0 14px 10px 14px; font-size: 13px;")
        about_layout.addWidget(intro_label)

        # Version information
        version_label = QLabel("Version: 1.0.0")
        version_label.setStyleSheet("color: gray; margin-left: 14px; font-size: 12px;")
        about_layout.addWidget(version_label)

        # Usage header
        usage_title = QLabel("Usage")
        usage_title.setStyleSheet("font-weight: 600; margin: 16px 14px 6px 14px; font-size: 14px;")
        about_layout.addWidget(usage_title)

        # Usage list (HTML list)
        usage_label = QLabel(
            "<ul style='margin-left:16px; padding:0 0 0 0;'>"
            "<li>Write a shortcut starting with ':'</li>"
            "<li>Press Space or Enter to expand the text</li>"
            "<li>Use Backspace to undo the last expansion</li>"
            "</ul>")
        usage_label.setWordWrap(True)
        about_layout.addWidget(usage_label)

        # Technology stack information
        tech_label = QLabel("This application is developed using <b>Python</b> &amp; <b>PyQt6</b>.")
        tech_label.setWordWrap(True)
        tech_label.setStyleSheet("margin: 10px 14px; font-size: 12px; color: gray;")
        about_layout.addWidget(tech_label)

        # Additional note
        note_label = QLabel("You can contribute to the project or provide feedback on <a href='https://github.com/kemalasliyuksek/Clipdex'>GitHub</a>.")
        note_label.setOpenExternalLinks(True)
        note_label.setWordWrap(True)
        note_label.setStyleSheet("margin: 4px 14px 10px 14px; font-size: 12px;")
        about_layout.addWidget(note_label)

        # Contact header
        contact_title = QLabel("Contact")
        contact_title.setStyleSheet("font-weight: 600; margin: 16px 14px 6px 14px; font-size: 14px;")
        about_layout.addWidget(contact_title)

        # Contact details list
        contact_html = (
            "<div style='margin-left:14px;'>"
            "<p style='margin:4px 0;font-size:13px;'>👤 Kemal Aslıyüksek</p>"
            "<p style='margin:4px 0;font-size:13px;'>🌐 <a href='https://kemalasliyuksek.com'>kemalasliyuksek.com</a></p>"
            "<p style='margin:4px 0;font-size:13px;'>👾 <a href='https://github.com/kemalasliyuksek'>GitHub</a></p>"
            "<p style='margin:4px 0;font-size:13px;'>💼 <a href='https://www.linkedin.com/in/kemalasliyuksek'>LinkedIn</a></p>"
            "<p style='margin:4px 0;font-size:13px;'>✉️ <a href='mailto:kemal@kemalasliyuksek.com'>kemal@kemalasliyuksek.com</a></p>"
            "<p style='margin:4px 0;font-size:13px;'>📍 Bursa/Turkiye</p>"
            "</div>"
        )
        contact_label = QLabel(contact_html)
        contact_label.setOpenExternalLinks(True)
        contact_label.setWordWrap(True)
        about_layout.addWidget(contact_label)

        about_layout.addStretch()  # Push content to top

        self.tab_widget.addTab(about_widget, "About")

    def setup_table(self):
        """Sets up the table with modern styling."""
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["#", "Shortcut", "Expansion"])

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
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            header.setStretchLastSection(True)

        self.table.setColumnWidth(0, 50)   # Width for the numbering column
        self.table.setColumnWidth(1, 120)  # Shortcut column
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
        for idx, (shortcut, expansion) in enumerate(snippets.items(), start=1):
            # Numbering column
            number_item = QTableWidgetItem(str(idx))
            number_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            shortcut_item = QTableWidgetItem(shortcut)
            expansion_item = QTableWidgetItem(expansion)
            
            # Set text alignment for better readability
            shortcut_item.setTextAlignment(0x0001 | 0x0080)  # Left | VCenter
            expansion_item.setTextAlignment(0x0001 | 0x0080)  # Left | VCenter
            
            self.table.setItem(row, 0, number_item)
            self.table.setItem(row, 1, shortcut_item)
            self.table.setItem(row, 2, expansion_item)
            row += 1

        self.table.setSortingEnabled(True) # Re-enable sorting
        self.table.resizeRowsToContents()  # Auto-resize rows to fit content

        # Update shortcut count label
        self.update_count_label()

    def filter_table(self):
        """Filters the table based on search text."""
        search_text = self.search_box.text().lower()
        
        for row in range(self.table.rowCount()):
            shortcut_item = self.table.item(row, 1)
            expansion_item = self.table.item(row, 2)
            
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

        item_shortcut = self.table.item(current_row, 1)
        item_expansion = self.table.item(current_row, 2)

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

        item_shortcut = self.table.item(current_row, 1)
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

    def update_count_label(self):
        """Updates the label that shows the total number of shortcuts."""
        if hasattr(self, "count_label"):
            total = self.table.rowCount()
            self.count_label.setText(f"Total shortcuts: {total}")

    def eventFilter(self, watched, event):
        """Clear the selection when clicking on Add/Edit/Delete buttons or outside the table."""
        if event.type() == QEvent.Type.MouseButtonPress and isinstance(event, QMouseEvent):
            # Determine the clicked widget based on the global position
            from PyQt6.QtWidgets import QApplication as _QApp
            app = _QApp.instance()
            if app is None:
                return super().eventFilter(watched, event)

            global_pos = event.globalPosition().toPoint()
            clicked_widget = _QApp.widgetAt(global_pos)

            # Protected widget list (table + buttons)
            protected_widgets = (self.table, self.add_btn, self.edit_btn, self.delete_btn)

            def is_descendant_of_any(widget, parents):
                if widget is None:
                    return False
                for p in parents:
                    if widget is p:
                        return True
                    if isinstance(widget, QWidget) and p.isAncestorOf(widget):
                        return True
                return False

            # If the clicked widget is not protected, clear the selection
            if not is_descendant_of_any(clicked_widget, protected_widgets):
                if self.table.selectedItems():
                    self.table.clearSelection()
                    self.table.setCurrentIndex(QModelIndex())
                    self.table.clearFocus()

            # Let the event flow normally
            return super().eventFilter(watched, event)

        return super().eventFilter(watched, event)

    # ---------------- System tray integration ----------------

    def _setup_tray_icon(self):
        """Creates the system tray icon and its context menu."""
        # Ensure system tray is available on the platform
        if not QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = None
            return

        # Prevent the application from quitting when the main window is closed
        QApplication.setQuitOnLastWindowClosed(False)

        # Use the dedicated tray icon for the platform; fall back to window icon if not found
        self.tray_icon = QSystemTrayIcon(self._get_tray_icon(), self)
        self.tray_icon.setToolTip("Clipdex")

        # Context menu for the tray icon
        tray_menu = QMenu()

        action_show = QAction("Show", self)
        action_quit = QAction("Quit", self)

        action_show.triggered.connect(self._restore_from_tray)
        action_quit.triggered.connect(QApplication.quit)

        tray_menu.addAction(action_show)
        tray_menu.addSeparator()
        tray_menu.addAction(action_quit)

        self.tray_icon.setContextMenu(tray_menu)

        # React to single-clicks on the tray icon
        self.tray_icon.activated.connect(self._on_tray_icon_activated)

        self.tray_icon.show()

    def _restore_from_tray(self):
        """Restores (shows) the main window from the system tray."""
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def _on_tray_icon_activated(self, reason):
        """Show the window when the tray icon is clicked once."""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self._restore_from_tray()

    def closeEvent(self, event):
        """Intercept the close event to minimize the app to the system tray instead of quitting."""
        tray = getattr(self, "tray_icon", None)
        if tray is not None and tray.isVisible():
            self.hide()
            # Optional balloon message to notify the user
            tray.showMessage(
                "Clipdex",
                "The application will continue to run in the background. To quit, select 'Quit' from the system tray icon.",
                QSystemTrayIcon.MessageIcon.Information,
                3000,
            )
            event.ignore()
        else:
            super().closeEvent(event)

    # ---------------- Icon helpers ----------------

    def _assets_dir(self) -> Path:
        """Returns the absolute path of the GUI assets directory."""
        return Path(__file__).resolve().parent / "assets"

    def _setup_app_icon(self):
        """Loads and sets the application (window) icon according to the current platform."""
        icon = self._create_app_icon()
        if not icon.isNull():
            self.setWindowIcon(icon)

    def _create_app_icon(self) -> QIcon:
        """Builds a QIcon containing all available resolutions for the current platform."""
        base_dir = self._assets_dir()

        # Windows – use .ico file that already bundles multiple sizes
        if sys.platform.startswith("win"):
            ico_path = base_dir / "icon_package" / "app_icon.ico" if (base_dir / "icon_package" / "app_icon.ico").exists() else base_dir / "app_icon.ico"
            return QIcon(str(ico_path))

        # macOS – use .icns file (also multi-resolution)
        if sys.platform == "darwin":
            icns_path = base_dir / "icon_package" / "app_icon.icns" if (base_dir / "icon_package" / "app_icon.icns").exists() else base_dir / "app_icon.icns"
            return QIcon(str(icns_path))

        # Linux / other – compose icon from the provided PNGs
        icon = QIcon()
        pkg_dir = base_dir / "icon_package"
        for size in [16, 24, 32, 48, 64, 128, 256, 512, 1024]:
            png_path = pkg_dir / f"icon_{size}x{size}.png"
            if png_path.exists():
                icon.addFile(str(png_path), QSize(size, size))
        # Fallback to a single PNG in assets root if multi-resolution set is missing
        if icon.isNull():
            fallback_png = base_dir / "app_icon.png"
            if fallback_png.exists():
                icon = QIcon(str(fallback_png))
        return icon

    def _get_tray_icon(self) -> QIcon:
        """Returns an appropriate QIcon for system tray based on the platform."""
        pkg_dir = self._assets_dir() / "icon_package"

        if sys.platform.startswith("win"):
            path = pkg_dir / "tray_16x16.png"
        elif sys.platform == "darwin":
            path = pkg_dir / "tray_20x20.png"
        else:
            # Prefer 24px for most Linux desktops; will scale automatically on HiDPI.
            path = pkg_dir / "tray_24x24.png"

        return QIcon(str(path)) if path.exists() else self.windowIcon()

# Test the main execution block
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())