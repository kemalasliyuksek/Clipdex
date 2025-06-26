# main.py

import sys
import threading
from PyQt6.QtWidgets import QApplication

from clipdex_gui.main_window import MainWindow
from clipdex_core.listener import ClipdexListener

# Dinleyiciyi çalıştıracak olan fonksiyon
def run_backend_listener():
    """
    Clipdex klavye dinleyici motorunu başlatır ve çalışır durumda tutar.
    """
    print("Backend listener thread'i başlatılıyor...")
    clipdex_engine = ClipdexListener()
    clipdex_engine.start()
    clipdex_engine.join() # Thread'in bitmesini bekle
    print("Backend listener thread'i durdu.")

def main():
    """
    Uygulamanın ana giriş noktası.
    GUI'yi başlatır ve backend'i ayrı bir thread'de çalıştırır.
    """
    # 1. Backend dinleyiciyi ayrı bir daemon thread'de başlat
    # daemon=True, ana uygulama (GUI) kapandığında bu thread'in de otomatik kapanmasını sağlar.
    listener_thread = threading.Thread(target=run_backend_listener, daemon=True)
    listener_thread.start()

    # 2. PyQt GUI uygulamasını başlat
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Uygulama döngüsünü başlat ve çıkış kodunu bekle
    sys.exit(app.exec())


if __name__ == "__main__":
    main()