import sys
import threading
import platform
from PyQt6.QtWidgets import QApplication, QMessageBox

from clipdex_gui.main_window import MainWindow
from clipdex_core.listener import ClipdexListener

# Run the backend listener
def run_backend_listener():
    """
    Starts and keeps the Clipdex keyboard listener running.
    """
    print("Backend listener thread started...")
    try:
        clipdex_engine = ClipdexListener()
        clipdex_engine.start()
        clipdex_engine.join() # Wait for the thread to finish
        print("Backend listener thread finished.")
    except Exception as e:
        print(f"Listener error: {e}")
        if platform.system() == "Darwin":
            print("Check Accessibility permissions on macOS!")

def show_macos_permission_dialog():
    """Show a dialog explaining MacOS permissions."""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setWindowTitle("macOS Permissions")
    msg.setText("Accessibility permissions are required for Clipdex to work.")
    msg.setInformativeText(
        "1. System Preferences > Security & Privacy > Privacy > Accessibility\n"
        "2. Click the '+' button and add the Clipdex application\n"
        "3. Check the box next to Clipdex\n"
        "4. Restart the application"
    )
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()

def main():
    """
    The main entry point of the application.
    Starts the GUI and runs the backend in a separate thread.
    """
    # Check if we're on MacOS and show permission info if needed
    if platform.system() == "Darwin":
        print("macOS detected - Checking permissions...")
    
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