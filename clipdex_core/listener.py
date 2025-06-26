import time
from pynput import keyboard as pynput_keyboard
import keyboard as system_keyboard
from .snippet_manager import SnippetManager
import os
from typing import Optional

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

        # Track the last modified time of the snippet file
        self._snippet_file_mtime: Optional[float] = self._get_snippet_file_mtime()

        # Prepare the pynput listener
        self.listener = pynput_keyboard.Listener(on_press=self.on_press)

    def start(self):
        """Starts the listener."""
        print("Clipdex engine running...")
        self.listener.start()

    def join(self):
        """Waits for the listener thread to finish."""
        self.listener.join()

    def on_press(self, key):
        """Function triggered on every key press."""
        # Update the snippet list on every key press
        self._refresh_snippets_if_needed()

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

    # ------------------------------------------------------------------
    # Helper Methods
    # ------------------------------------------------------------------

    def _get_snippet_file_mtime(self) -> float:
        """Returns the last modified time of the snippet file."""
        if os.path.exists(self.snippet_manager.filepath):
            return os.path.getmtime(self.snippet_manager.filepath)
        return 0.0

    def _refresh_snippets_if_needed(self):
        """Reloads the snippet list if the file has been modified."""
        try:
            current_mtime = self._get_snippet_file_mtime()
            if current_mtime != self._snippet_file_mtime:
                self.snippets = self.snippet_manager.load_snippets()
                self._snippet_file_mtime = current_mtime
                print("Snippet list updated.")
        except Exception as e:
            # If there's an error reading the file, don't crash the engine
            print(f"Snippet update error: {e}")