import sys
import threading
from PyQt6.QtWidgets import QApplication

from clipdex_gui.main_window import MainWindow
from clipdex_core.listener import ClipdexListener

# Run the backend listener
def run_backend_listener():
    """
    Starts and keeps the Clipdex keyboard listener running.
    """
    print("Backend listener thread started...")
    clipdex_engine = ClipdexListener()
    clipdex_engine.start()
    clipdex_engine.join() # Wait for the thread to finish
    print("Backend listener thread finished.")

def main():
    """
    The main entry point of the application.
    Starts the GUI and runs the backend in a separate thread.
    """
    # 1. Start the backend listener in a separate daemon thread
    # daemon=True, the main application (GUI) will automatically close this thread when it exits.
    listener_thread = threading.Thread(target=run_backend_listener, daemon=True)
    listener_thread.start()

    # 2. Start the PyQt GUI application
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Start the application loop and wait for the exit code
    sys.exit(app.exec())


if __name__ == "__main__":
    main()