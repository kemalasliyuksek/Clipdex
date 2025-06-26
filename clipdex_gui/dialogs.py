# clipdex_gui/dialogs.py

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QTextEdit,
                             QFormLayout, QDialogButtonBox, QLabel)

class SnippetDialog(QDialog):
    def __init__(self, parent=None, shortcut="", expansion=""):
        super().__init__(parent)
        self.setWindowTitle("Kısayol Ekle/Düzenle")

        self.layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.shortcut_input = QLineEdit(shortcut)
        self.shortcut_input.setPlaceholderText(":kısayol")
        self.expansion_input = QTextEdit(expansion)
        self.expansion_input.setPlaceholderText("Genişletilecek metni buraya yazın.")

        form_layout.addRow(QLabel("Kısayol:"), self.shortcut_input)
        form_layout.addRow(QLabel("Metin:"), self.expansion_input)

        self.layout.addLayout(form_layout)

        # Standart OK ve Cancel butonları
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)

    def get_data(self):
        """Dialogdaki verileri döndürür."""
        shortcut = self.shortcut_input.text().strip()
        # Kısayolun başında ':' yoksa ekle
        if shortcut and not shortcut.startswith(':'):
            shortcut = ':' + shortcut

        return {
            "shortcut": shortcut,
            "expansion": self.expansion_input.toPlainText().strip()
        }