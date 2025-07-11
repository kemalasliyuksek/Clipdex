from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QTextEdit,
                             QFormLayout, QDialogButtonBox, QLabel)

class SnippetDialog(QDialog):
    def __init__(self, parent=None, shortcut="", expansion=""):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Snippet")

        self.main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.shortcut_input = QLineEdit(shortcut)
        self.shortcut_input.setPlaceholderText("shortcut")
        self.expansion_input = QTextEdit(expansion)
        self.expansion_input.setPlaceholderText("Enter the text to expand.")

        form_layout.addRow(QLabel("Shortcut:"), self.shortcut_input)
        form_layout.addRow(QLabel("Text:"), self.expansion_input)

        self.main_layout.addLayout(form_layout)

        # QLineEdit style and size
        self.shortcut_input.setFixedHeight(35)
        self.shortcut_input.setStyleSheet(
            """
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
            """
        )

        # QTextEdit style and size
        self.expansion_input.setFixedHeight(150)
        self.expansion_input.setStyleSheet(
            """
            QTextEdit {
                padding: 8px 12px;
                border: 1px solid palette(mid);
                border-radius: 6px;
                background-color: palette(base);
                color: palette(text);
                font-size: 13px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QTextEdit:focus {
                border: 2px solid palette(highlight);
            }
            """
        )

        # Standard OK and Cancel buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Style and size of the buttons (OK/Cancel)
        for btn in self.button_box.buttons():
            btn.setFixedHeight(40)
            btn.setStyleSheet("font-size: 14px; font-weight: bold;")

        self.main_layout.addWidget(self.button_box)

    def get_data(self):
        """Returns the data from the dialog."""
        shortcut = self.shortcut_input.text().strip()

        # If the user accidentally enters one or more ':' characters,
        # clean them up and only save the shortcut name. The listener already
        # handles the first ':' character as the trigger.
        shortcut = shortcut.lstrip(':')

        return {
            "shortcut": shortcut,
            "expansion": self.expansion_input.toPlainText().strip()
        }