# clipdex_gui/main_window.py

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
                             QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QHeaderView)
from PyQt6.QtCore import Qt

from clipdex_gui.dialogs import SnippetDialog
from PyQt6.QtWidgets import QMessageBox # Bu satırı ekleyin

# Çekirdek mantığımızdan SnippetManager'ı import edelim
from clipdex_core.snippet_manager import SnippetManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clipdex - Snippet Manager")
        self.setGeometry(300, 300, 800, 500)

        # SnippetManager'ı başlatalım
        self.snippet_manager = SnippetManager()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Ana layout
        self.layout = QVBoxLayout(self.central_widget)

        # Kısayol tablosunu oluşturalım
        self.table = QTableWidget()
        self.setup_table()
        self.layout.addWidget(self.table)

        # Butonları yerleştireceğimiz yatay layout
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("Yeni Ekle")
        self.edit_btn = QPushButton("Seçileni Düzenle")
        self.delete_btn = QPushButton("Seçileni Sil")

        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)
        self.layout.addLayout(button_layout)

        # Verileri tabloya yükle
        self.populate_table()

        # __init__ metodunun sonuna ekleyin
        self.add_btn.clicked.connect(self.add_snippet)
        self.edit_btn.clicked.connect(self.edit_snippet)
        self.delete_btn.clicked.connect(self.delete_snippet)

    def setup_table(self):
        """Tablonun temel ayarlarını yapar."""
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Kısayol", "Genişletilecek Metin"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0, 200) # Kısayol sütunu için başlangıç genişliği
        self.table.setSortingEnabled(True) # Sıralamayı aktif et

    def populate_table(self):
        """snippets.json'dan verileri okur ve tabloyu doldurur."""
        self.table.setSortingEnabled(False) # Güncelleme sırasında sıralamayı kapat

        snippets = self.snippet_manager.load_snippets()
        self.table.setRowCount(len(snippets))

        row = 0
        for shortcut, expansion in snippets.items():
            self.table.setItem(row, 0, QTableWidgetItem(shortcut))
            self.table.setItem(row, 1, QTableWidgetItem(expansion))
            row += 1

        self.table.setSortingEnabled(True) # Sıralamayı tekrar aktif et

    def add_snippet(self):
        """Yeni kısayol ekleme penceresini açar."""
        dialog = SnippetDialog(self)
        if dialog.exec():  # .exec() dialogu açar ve kullanıcı OK'a basarsa True döner
            data = dialog.get_data()
            if not data["shortcut"] or not data["expansion"]:
                QMessageBox.warning(self, "Uyarı", "Kısayol ve metin alanları boş bırakılamaz.")
                return

            snippets = self.snippet_manager.load_snippets()
            snippets[data["shortcut"]] = data["expansion"]
            self.snippet_manager.save_snippets(snippets)
            self.populate_table()  # Tabloyu yenile

    def edit_snippet(self):
        """Seçili kısayolu düzenleme penceresini açar."""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen düzenlemek için bir kısayol seçin.")
            return

        old_shortcut = self.table.item(current_row, 0).text()
        expansion = self.table.item(current_row, 1).text()

        dialog = SnippetDialog(self, shortcut=old_shortcut, expansion=expansion)
        if dialog.exec():
            data = dialog.get_data()
            if not data["shortcut"] or not data["expansion"]:
                QMessageBox.warning(self, "Uyarı", "Kısayol ve metin alanları boş bırakılamaz.")
                return

            snippets = self.snippet_manager.load_snippets()
            # Eski kısayolu sil (eğer değiştirildiyse)
            if old_shortcut in snippets:
                del snippets[old_shortcut]

            snippets[data["shortcut"]] = data["expansion"]
            self.snippet_manager.save_snippets(snippets)
            self.populate_table()

    def delete_snippet(self):
        """Seçili kısayolu siler."""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek için bir kısayol seçin.")
            return

        shortcut = self.table.item(current_row, 0).text()

        reply = QMessageBox.question(self, "Silme Onayı",
                                     f"'{shortcut}' kısayolunu silmek istediğinizden emin misiniz?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            snippets = self.snippet_manager.load_snippets()
            if shortcut in snippets:
                del snippets[shortcut]
                self.snippet_manager.save_snippets(snippets)
                self.populate_table()

# Test etmek için ana çalıştırma bloğu
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())