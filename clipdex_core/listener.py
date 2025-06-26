import time
from pynput import keyboard as pynput_keyboard
import keyboard as system_keyboard
from .snippet_manager import SnippetManager  # Relative import

class ClipdexListener:
    """
    Listens for system-wide keyboard events and performs text expansion.
    """
    def __init__(self):
        self.snippet_manager = SnippetManager()
        self.snippets = self.snippet_manager.load_snippets()

        # Variables to track the current state
        self.current_shortcut = ""
        self.is_listening = False

        # Prepare the pynput listener for startup
        self.listener = pynput_keyboard.Listener(on_press=self.on_press)

    def start(self):
        """Starts the listener."""
        print("Clipdex engine running... Stop with (Ctrl+C).")
        self.listener.start()

    def join(self):
        """Waits for the listener thread to finish."""
        self.listener.join()

    def on_press(self, key):
        """Function triggered on every key press."""
        try:
            # ':' character starts listening
            if hasattr(key, 'char') and key.char == ':':
                self.is_listening = True
                self.current_shortcut = ""
                # print("Listening started...")  # For debugging
                return

            if self.is_listening:
                # Space or Enter ends the shortcut
                if key == pynput_keyboard.Key.space or key == pynput_keyboard.Key.enter:
                    if self.current_shortcut in self.snippets:
                        # print(f"Shortcut found: {self.current_shortcut}")  # For debugging

                        # 1. Delete the typed shortcut
                        # The shortcut itself + the trigger ':' + the terminator ' '
                        backspace_count = len(self.current_shortcut) + 2
                        for _ in range(backspace_count):
                            system_keyboard.press_and_release('backspace')
                            time.sleep(0.01)  # Prevent keypress overlaps

                        # 2. Write the expanded text
                        expanded_text = self.snippets[self.current_shortcut]
                        system_keyboard.write(expanded_text)

                    # Reset state
                    self.is_listening = False
                    self.current_shortcut = ""

                # Backspace removes a character
                elif key == pynput_keyboard.Key.backspace:
                    self.current_shortcut = self.current_shortcut[:-1]

                # Other characters are added to the shortcut
                elif hasattr(key, 'char') and key.char:
                    self.current_shortcut += key.char

        except Exception as e:
            # Catch possible errors and prevent the listener from crashing
            print(f"An error occurred: {e}")
            self.is_listening = False
            self.current_shortcut = ""